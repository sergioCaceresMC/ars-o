import subprocess
import logging
import json
import time

import p_general.interprete as it

#Crea un bridge con las configuraciones dadas. Si ya está creado solo lo reconfigura 
def crear_bridge(lxdbr, 
                 ipv4nat="true", ipv4address="", 
                 ipv6nat="false", ipv6address="none", 
                 dnsmode="none", dnsdomain="lxd"):
    #creamos el bridge
    it.ejecutar_str(f"lxc network create {lxdbr}")

    #configuramos el ipv4
    it.ejecutar_str(f"lxc network set {lxdbr} ipv4.nat {ipv4nat}")
    it.ejecutar_str(f"lxc network set {lxdbr} ipv4.address {ipv4address}/24")

    #desactivamos el ipv6
    it.ejecutar_str(f"lxc network set {lxdbr} ipv6.nat {ipv6nat}")
    it.ejecutar_str(f"lxc network set {lxdbr} ipv6.address {ipv6address}")
    
    #Configura el dominio de DNS
    it.ejecutar_str(f"lxc network set {lxdbr} dns.domain {dnsdomain}")
    it.ejecutar_str(f"lxc network set {lxdbr} dns.mode {dnsmode}")

#Asigna una interfaz determinada a un contenedor existente. Por defecto lo arranca al terminar (init)
def configurar_comunicacion(contenedor, eth, address, lxdbr, init = True):
    #paramos el contenedor
    it.ejecutar_str(f"lxc stop {contenedor}")

    #configurar la comunicación del contenedor
    it.ejecutar_str(f"lxc network attach {lxdbr} {contenedor} {eth}")
    logging.info(f"network agregada correctamente: {lxdbr}, {contenedor}")
    it.ejecutar_str(f"lxc config device set {contenedor} {eth} ipv4.address {address}")
    logging.info(f"contenedor agregado correctamente: {address}, {contenedor}")
    
    #iniciamos el contenedor en caso de ser requerido
    if init: it.ejecutar_str(f"lxc start {contenedor}")

#Reescribe el yaml del contenedor por uno donde estén marcadas las eth dadas
def configurar_yaml_por_sustitucion(cont, eth=["eth0","eth1"]):
    eths = ""

    #Añadimos todos los eth del array para unirlo luego al comando que lo envía al YAML 
    for e in eth:
        eths += f'''
        {e}:
          dhcp4: true'''

    #Creamos un comando que se encarga de reescribir el contenido del YAML 
    command = f'''
cat <<EOF | lxc exec {cont} -- tee /etc/netplan/50-cloud-init.yaml
network:
    version: 2
    ethernets:{eths}
EOF
'''
    #Ejecutamos el comando 
    subprocess.run(command, shell=True, executable="/bin/bash", check=False, text=True)

    #el subprocess parece que se ejecuta de manera asincrona por lo que sea. 
    #El sleep es para evitar interferencias
    time.sleep(5) 

    logging.info(f"YAML de {cont} configurado. Se ha añadido {eth}")
    
    #Reiniciamos el contenedor 
    it.ejecutar_str(f"lxc exec {cont} -- shutdown -r now")
    logging.info(f"Rearrancando {cont} configurado.")

#Borra un network y desconecta los contenedores que la usan
def delete_network(network="lxdbr1"):

    #Obtenemos todos los contenedores en formato json 
    #para poder acceder a los nombres de forma más sencilla que con read_data() 
    contenedores = obtener_contenedores()

    #buscamos todos los contenedores que están en la red 
    for contenedor in contenedores:
        nombre = contenedor["name"]
        config = it.ejecutar_str(f"lxc config show {nombre} --expanded", 
                                 capture=True, tex=True, chec=True).stdout
        if not config: continue
        for linea in config.splitlines():
            if f"network: {network}" in linea or f"name: {network}" in linea:
                logging.info(f"desconectando red {network} del contenedor {nombre}")
        
                #Eliminamos las interfaces de red asociadas
                eliminar_interfaces_con_network(nombre, network)
                
    #Eliminamos el network 
    it.ejecutar_str(f"lxc network delete {network}")

#Dado un contenedor y una network 
def eliminar_interfaces_con_network(contenedor, network):
    salida = it.ejecutar_str(f"lxc config device list {contenedor}",
                             capture=True, tex=True, chec=True).stdout
    if not salida:
        return
    contenedores = salida.strip().splitlines()

    for cont in contenedores:
        #Obtener información del contenedor
        info = it.ejecutar_str(f"lxc config device show {contenedor}",
                                capture=True, tex=True, chec=True).stdout

        #Si el network está en la info del contenedor lo quitamos
        if info and network in info:
            it.ejecutar_str(f"lxc config device remove {contenedor} {cont}")

#Similar a read_data al módulo de memoria 
#pero devuelve en formato json en lugar de un arreglo 
#solo con los nombres de los contenedores existentes
def obtener_contenedores():
    salida = it.ejecutar_str("lxc list --format json", 
                             capture=True, tex=True, chec=True).stdout
    return json.loads(salida)