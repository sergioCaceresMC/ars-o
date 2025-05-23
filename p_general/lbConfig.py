import subprocess
import logging
import sys
import os 
import time
from jinja2 import Template

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import p_general.interprete as it
import p_general.memoria as mem
import p_general.cache as cache

#Ruta base relativa a pfinal2.py
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

#Ruta a los archivos dentro de la carpetea imágenes
RUTA_HAPROXY_CONF = os.path.join(BASE_DIR, "transferencias", "haproxy.cfg.j2")
RUTA_HAPROXY_CONF_PUSH = os.path.join(BASE_DIR, "transferencias", "haproxy.cfg")
RUTA_HAPROXY_HOST = os.path.join(BASE_DIR, "transferencias", "hosts.j2")
RUTA_HAPROXY_HOST_PUSH = os.path.join(BASE_DIR, "transferencias", "hosts")

#insatala haproxy en el balanceador
def instalar_proxy(sv):
    if mem.check_status(sv) == "STOPPED": it.ejecutar_str(f"lxc start {sv}")
    logging.info(f"instalando haproxy en {sv}")

    it.ejecutar_str(f"lxc exec {sv} -- apt update")
    it.ejecutar_str(f"lxc exec {sv} -- apt install haproxy -y")
    
    modify_haproxy_docs(get_data_to_proxy())
    logging.info("configurando haproxy")
    push_to_lb(sv)

'''
#Prueba
servidores = [
    {"mv_name": "s1", "name": "webserver1", "ip": "10.0.0.11", "port": 8001},
    {"mv_name": "s2", "name": "webserver2", "ip": "10.0.0.12", "port": 8001},
    {"mv_name": "s3", "name": "webserver3", "ip": "10.0.0.13", "port": 8001},
]
'''
def add_servers(servidores = [], mv_name="", webserver_name="", ip="", port="8001"):
    servidores.append({"mv_name": mv_name, "name": webserver_name, "ip": ip, "port": port})

def get_data_to_proxy():
    logging.info("creando el archivo de haproxy.cfg")
    #obtenemos la cabecera ip del ecosistema
    ip_head = mem.get_ip_header()
    #obtenemos el número de servidores que hay
    n_servs = int(cache.leer_cache()[0])
    #Para cada servidor que existe lo agregamos al proxy
    servidor_a_comprobar_si_existe = 1
    contador = 1

    s = [] #array con diccionarios de los servidores y sus ip

    while contador <= n_servs:
        if mem.exist_data(f"s{servidor_a_comprobar_si_existe}") and servidor_a_comprobar_si_existe != 20:
            #si el servidor existe entonces agregamos la dirección a las direcciones del proxy
            add_servers(servidores=s, mv_name=f"s{servidor_a_comprobar_si_existe}", 
                        webserver_name=f"webserver{contador}",
                        ip=f"{ip_head}.0.1{servidor_a_comprobar_si_existe}")
            contador += 1
            #print(servidor_a_comprobar_si_existe)
        servidor_a_comprobar_si_existe +=1
    return s
        

def modify_haproxy_docs(servidores):
    #====== Crear el hproxy ==========#
    #Leer la plantilla
    with open(RUTA_HAPROXY_CONF) as f:
        template = Template(f.read())

    #Renderizar
    config = template.render(servers=servidores)

    #Guardar archivo final
    with open(RUTA_HAPROXY_CONF_PUSH, "w") as f:
        f.write(config)

    #====== Crear el host ==========#
    #Leer la plantilla
    with open(RUTA_HAPROXY_HOST) as f:
        template = Template(f.read())

    #Renderizar
    config = template.render(servers=servidores)

    #Guardar archivo final
    with open(RUTA_HAPROXY_HOST_PUSH, "w") as f:
        f.write(config)

#Envia los archivos al contenedor que actua como balanceador
def push_to_lb(sv):
    cmd1 = f"lxc exec {sv} -- bash -c 'cd /etc && mv hosts hosts-old'"
    subprocess.run(cmd1, shell=True, text=True, capture_output=True)
    cmd2 = f"lxc exec {sv} -- bash -c 'cd /etc/haproxy && mv haproxy.cfg haproxy-old.cfg'"
    subprocess.run(cmd2, shell=True, text=True, capture_output=True)
    cmd3 = f"lxc file push {RUTA_HAPROXY_CONF_PUSH} {sv}/etc/haproxy/"
    subprocess.run(cmd3, shell=True, text=True, capture_output=True)
    cmd4 = f"lxc file push {RUTA_HAPROXY_HOST_PUSH} {sv}/etc/"
    subprocess.run(cmd4, shell=True, text=True, capture_output=True)
    
'''
if __name__ == "__main__":

    push_to_lb("lb")
'''