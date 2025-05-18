import os
from jinja2 import Template

import p_general.interprete as it


#Ruta base relativa a pfinal2.py
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

#Ruta a los archivos dentro de la carpetea imágenes
RUTA_HAPROXY_CONF = os.path.join(BASE_DIR, "transferencias", "haproxy.cfg.j2")
RUTA_HAPROXY_CONF_PUSH = os.path.join(BASE_DIR, "transferencias", "haproxy.cfg")
RUTA_HAPROXY_HOST = os.path.join(BASE_DIR, "transferencias", "hosts.j2")
RUTA_HAPROXY_HOST_PUSH = os.path.join(BASE_DIR, "transferencias", "hosts")
RUTA_NODE_INSTALL = os.path.join(BASE_DIR, "transferencias", "install.sh")
RUTA_APP = os.path.join(BASE_DIR, "transferencias", "app.tar.gz")



#Crea y rellena correctamente el archivo del balanceador
'''
Ejemplo de entrada:
servidores = [
    {"mv_name": "s1", "name": "webserver1", "ip": "10.0.0.11", "port": 8001},
    {"mv_name": "s2", "name": "webserver2", "ip": "10.0.0.12", "port": 8001},
    {"mv_name": "s3", "name": "webserver3", "ip": "10.0.0.13", "port": 8001},
]
'''
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
def push_to_lb():
    pass

'''
if __name__ == "__main__":
    #Prueba
    servidores = [
        {"mv_name": "s1", "name": "webserver1", "ip": "10.0.0.11", "port": 8001},
        {"mv_name": "s2", "name": "webserver2", "ip": "10.0.0.12", "port": 8001},
        {"mv_name": "s3", "name": "webserver3", "ip": "10.0.0.13", "port": 8001},
    ]
    modify_haproxy_docs(servidores)
'''
