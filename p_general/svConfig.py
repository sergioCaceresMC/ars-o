import sys
import os
import subprocess
import logging
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import p_general.interprete as it
import p_general.memoria as mem
import p_general.contenedores as ct
import p_general.archivos as arch
import p_general.configuraciones as conf



#Ruta base relativa a pfinal2.py
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RUTA_NODE_INSTALL = os.path.join(BASE_DIR, "transferencias", "install.sh")
RUTA_APP = os.path.join(BASE_DIR, "transferencias", "app")

#insatala node y la aplicación web
def instalar_node(sv):
    logging.info(f"instalando node en {sv}")
    if mem.check_status(sv) == "STOPPED": it.ejecutar_str(f"lxc start {sv}")

    #transferir install
    logging.info(f"transfiriendo archivos a {sv}")
    it.ejecutar_str(f"lxc file push {RUTA_NODE_INSTALL} {sv}/root/install.sh")
    time.sleep(3)
    logging.info(f"cambiando permisos de install {sv}")
    it.ejecutar_str(f"lxc exec {sv} -- chmod +x install.sh")
    time.sleep(3)
    #transferir la aplicación
    logging.info(f"transfiriendo archivos app a {sv}")
    it.ejecutar_str(f"lxc file push --recursive {RUTA_APP} {sv}/root/")
    time.sleep(5)
    
    #Instalar la aplicación
    logging.info(f"ejecutando install {sv}")
    it.ejecutar_str(f"lxc exec {sv} -- ./install.sh")
    time.sleep(5)
    
    it.ejecutar_str(f"lxc restart {sv}")


#Crea la imagen de un contenedor y le asigna un nombre
def crear_imagen_de_cont(sv, name = "servidorBaseImgSJ2025"):
    ct.detener_contenedor(sv)
    it.ejecutar_str(f"lxc publish {sv} --alias {name}")

#Crear la imagen base del servidor
def create_img_servers(name = "servidorBaseImgSJ2025", force = False):

    #Primero comprobamos si la imágen ya existe
    # Verificamos si la imagen con el alias ya existe
    resultado = it.ejecutar_str("lxc image list --format csv", capture=True, tex=True)
    salida = resultado.stdout.strip().split('\n')
    encontrado = False

    # Creamos un diccionario donde la llave es el fingerprint y el valor es alias
    data = {}
    for linea in salida:
        columnas = linea.split(',')
        if len(columnas) > 1:
            alias_encontrado, fingerprint = columnas[0], columnas[1]
            data[fingerprint] = alias_encontrado

    if force:
        for imagen in data.keys():
            it.ejecutar_str(f"lxc image delete {imagen}")
    
    ct.delete_contenedor("contTemporal")
    ct.crear_cont("contTemporal", init= True)
    instalar_node("contTemporal")
    crear_imagen_de_cont("contTemporal")


if __name__ == "__main__":
    pass