import subprocess
import logging
import time

import p_general.interprete as it
import p_general.memoria as mem
import p_general.cache as cache
import p_general.contenedores as ct
import p_general.archivos as arch

#insatala node y la aplicación web
def instalar_node(sv):
    logging.info(f"instalando node en {sv}")
    if mem.check_status(sv) == "STOPPED": it.ejecutar_str(f"lxc start {sv}")
    it.ejecutar_str(f"lxc exec {sv} -- apt update")

    #transferir install
    it.ejecutar_str(f"lxc file push {arch.RUTA_NODE_INSTALL} {sv}/root/install.sh")
    time.sleep(3)
    it.ejecutar_str(f"lxc exec {sv} -- chmod +x install.sh")

    #transferir la aplicación
    it.ejecutar_str(f"lxc file push -r {arch.RUTA_APP} {sv}/root/")
    time.sleep(3)
    #Descomprimir la aplicación
    it.ejecutar_str(f" lxc exec {sv} -- tar-oxvf app.tar.gz")
    time.sleep(5)
    
    #Instalar la aplicación
    it.ejecutar_str(f"lxc exec {sv} -- ./install.sh")
    time.sleep(5)
    
    it.ejecutar_str(f"lxc restart {sv}")

#insatala haproxy en el balanceador
def instalar_proxy(sv):
    logging.info(f"instalando haproxy en {sv}")
    if mem.check_status(sv) == "STOPPED": it.ejecutar_str(f"lxc start {sv}")
    it.ejecutar_str(f"lxc exec {sv} -- apt update")
    it.ejecutar_str(f"lxc exec {sv} -- apt install haproxy -y")
    logging.info("configurando haproxy")
    #transferir_archivos_proxy(sv)

#Transfiere los archivos configurados al balanceador
def transferir_archivos_proxy(cont):
    print(f"transfiriendo archivos en {cont}")
    it.ejecutar_str(f'lxc exec {cont} -- bash -c "cd /etc && mv hosts hosts-old"')
    it.ejecutar_str(f"lxc file push {arch.RUTA_HAPROXY_HOST_PUSH} {cont}/var/www/html/")
    time.sleep(3)
    it.ejecutar_str(f'lxc exec {cont} -- bash -c "cd /etc/haproxy && haproxy.cfg haproxy-old.cfg"')
    it.ejecutar_str(f"lxc file push {arch.RUTA_HAPROXY_CONF_PUSH} {cont}/var/www/html/")
    time.sleep(3)
    it.ejecutar_str(f"lxc restart {cont}")

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
            if name == alias_encontrado: 
                if not force: return True

    #Si la imágen existe o estamos en modo forzado, 
    #vamos a borrar las imágenes y crearemos la imagen correspondiente
    if force:
        for imagen in data.values():
            it.ejecutar_str(f"lxc image delete {imagen}")
    ct.crear_cont("contTemporal")
    instalar_node("contTemporal")
    crear_imagen_de_cont("contTemporal")

if __name__ == "__main__":
    create_img_servers()