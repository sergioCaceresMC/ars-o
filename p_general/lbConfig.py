import subprocess
import logging
import sys
import os 
import time
from jinja2 import Template

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import p_general.interprete as it
import contenedores as ct
import memoria as mem

#Ruta base relativa a pfinal2.py
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

#Ruta a los archivos dentro de la carpetea imágenes
RUTA_HAPROXY_CONF = os.path.join(BASE_DIR, "transferencias", "haproxy.cfg.j2")
RUTA_HAPROXY_CONF_PUSH = os.path.join(BASE_DIR, "transferencias", "haproxy.cfg")
RUTA_HAPROXY_HOST = os.path.join(BASE_DIR, "transferencias", "hosts.j2")
RUTA_HAPROXY_HOST_PUSH = os.path.join(BASE_DIR, "transferencias", "hosts")

#servidores variable temporal
SERVIDORES = []

#insatala haproxy en el balanceador
def instalar_proxy(sv):
    if mem.check_status(sv) == "STOPPED": it.ejecutar_str(f"lxc start {sv}")
    logging.info(f"instalando haproxy en {sv}")

    it.ejecutar_str(f"lxc exec {sv} -- apt update")
    it.ejecutar_str(f"lxc exec {sv} -- apt install haproxy -y")
    
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
def add_servers(mv_name, webserver_name, ip, port):
    SERVIDORES.append({"mv_name": mv_name, "name": webserver_name, "ip": ip, "port": port})

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
    cmd1 = f"""lxc exec {sv} -- bash -c "cd /etc && mv hosts hosts-old" """
    cmd2 = f"""lxc exec {sv} -- bash -c "cd /etc/haproxy && mv haproxy.cfg haproxy-old.cfg" """

    it.ejecutar_str(cmd1)
    it.ejecutar_str(cmd2)
    it.ejecutar_popen(f"lxc file push {RUTA_HAPROXY_CONF_PUSH} {sv}/var/www/html/")
    it.ejecutar_popen(f"lxc file push {RUTA_HAPROXY_HOST_PUSH} {sv}/etc/haproxy/")


if __name__ == "__main__":

    instalar_proxy("lb")