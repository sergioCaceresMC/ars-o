import logging
import re

import p_general.interprete as it

#leer los contenedores existentes
def read_data():
    result = it.ejecutar_str("lxc list --format csv", capture =True, tex=True)
    salida = result.stdout.strip().split('\n')
    data = [linea.split(',')[0] for linea in salida]
    return data

#comprobar que existe el dato. devuelve boolean
def exist_data(data):
    lines = read_data()

    for line in lines:
        if data == line:
            return True
    return False   

#cuenta el número de contenedores que son del tipo servidor. Devuelve int ***
def count_servers():
    data = read_data()
    cont = 0
    for element in data:
        if (not "lb" in element and not "cl" in element):
            cont += 1
    return cont

#Devuelve el estado del contenedor. Por ejemplo: "STOPPED", "RUNNING"
#Si el contenedor no se encuentra devuelve NONE
def check_status(contenedor):
    salida = it.ejecutar_str(f"lxc list --format csv", capture=True, tex=True).stdout.strip().split('\n')
    result = []
    for linea in salida:
        if(contenedor in linea):
            result = linea.split(',')
    if len(result) >= 1: 
        return result[1]
    else:
        logging.error("El contenedor no se ha encontrado")
        return None

#Comprobar si una network existe. Se usa en los test
def check_networks(contenedor):
    resultado = it.ejecutar_str(f"lxc list {contenedor} --format csv",
            capture=True, tex=True, chec=True)
    
    lineas = resultado.stdout.strip().splitlines()

    interfaces_encontradas = set()

    for linea in lineas:
        partes = linea.split(',')
        if len(partes) > 2:
            ips = partes[2]
            #extraer interfaces entre paréntesis
            interfaces = [ip.split('(')[-1].replace(')', '').replace('"', '') for ip in ips.split()]
            interfaces_encontradas.update(interfaces)
    return interfaces_encontradas

#Obtiene la cabecera ip del ecosistema siempre que exista al menos un contenedor configurado
#(Tiene orden de prioridad s1 ... lb, cl)
def get_ip_header():
    vm = ""
    for contenedor in read_data():
        if contenedor in ["s1","s2","s3","s4","s5","lb","cl"]:
            vm = contenedor 
    networks = check_networks(vm)
    for item in networks:
        if re.match(r"^\d+\.\d+\.\d+\.\d+$", item):
            parts = item.split(".")
            return f"{parts[0]}.{parts[1]}"
    return "134.3"

#listar la informacion de los contenedores
def lista_info_all():
    it.ejecutar_str("lxc list")

#listar la informacion de un contenedor
def lista_info_indiv_extended(name):
    it.ejecutar_str(f"lxc info {name}")
 