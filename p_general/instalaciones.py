import sys
import os
import subprocess
import logging
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import p_general.interprete as it
import p_general.memoria as mem
import p_general.cache as cache
import p_general.contenedores as ct
import p_general.archivos as arch
import p_general.configuraciones as conf

#insatala node y la aplicación web
def instalar_node(sv):
    logging.info(f"instalando node en {sv}")
   # if mem.check_status(sv) == "STOPPED": it.ejecutar_str(f"lxc start {sv}")

    #transferir install
    logging.info(f"transfiriendo archivos a {sv}")
    it.ejecutar_str(f"lxc file push {arch.RUTA_NODE_INSTALL} {sv}/root/install.sh")
   #lxc file push ./transferencias/install.sh contTemporal2/root/install.sh 
    time.sleep(3)
    logging.info(f"cambiando permisos de install {sv}")
    it.ejecutar_str(f"lxc exec {sv} -- chmod +x install.sh")
    time.sleep(3)
    #transferir la aplicación
    logging.info(f"transfiriendo archivos app a {sv}")
    it.ejecutar_str(f"lxc file push --recursive {arch.RUTA_APP} {sv}/root/")
    time.sleep(5)
    
    #Instalar la aplicación
    logging.info(f"ejecutando install {sv}")
    it.ejecutar_str(f"lxc exec {sv} -- ./install.sh")
    time.sleep(5)
    
    it.ejecutar_str(f"lxc restart {sv}")

#insatala haproxy en el balanceador
def instalar_proxy(sv):
    logging.info(f"instalando haproxy en {sv}")
    if mem.check_status(sv) == "STOPPED": it.ejecutar_str(f"lxc start {sv}")
    it.ejecutar_str(f"lxc exec {sv} -- apt update")
    time.sleep(10)
    it.ejecutar_str(f"lxc exec {sv} -- apt install haproxy -y")
    time.sleep(10)
    logging.info("configurando haproxy")
    #transferir_archivos_proxy(sv)

# NO SÉ SI MONGO SE ESTÁ LOGRANDO COMUNICAR. PUEDE HABER ERRORES AL MODIFICAR EL MONGO.CONFG (linea 63)

#insatala mongo
def instalar_mongo(sv):
    logging.info(f"instalando mongo en {sv}")
    it.ejecutar_str(f"lxc start {sv}")
    time.sleep(10)
    it.ejecutar_str(f"lxc exec {sv} -- apt update")
    time.sleep(2)
    it.ejecutar_str(f"lxc exec {sv} -- apt install -y mongodb")
    time.sleep(3)
    logging.info(f"cambiando archivo mongo en {sv}")
    it.ejecutar_str(f"lxc exec {sv} -- bash -c 'sed -i \"s/^bind_ip = 127.0.0.1/bind_ip = 127.0.0.1,134.3.0.20/\" /etc/mongodb.conf'")
    time.sleep(3)
    it.ejecutar_str(f"lxc restart {sv}")

## LA FUNCION TRANSFERIR ARCHIVOS PROXY NO LOS TRANSFIERE ## 

#Transfiere los archivos configurados al balanceador
def transferir_archivos_proxy(cont):
    cmd1 = f"""lxc exec {cont} -- bash -c "cd /etc && mv hosts hosts-old" """
    cmd2 = f"""lxc exec {cont} -- bash -c "cd /etc/haproxy && mv haproxy.cfg haproxy-old.cfg" """

    it.ejecutar_str(cmd1)
    it.ejecutar_str(f"lxc file push {arch.RUTA_HAPROXY_HOST_PUSH} {cont}/var/www/html/")
    time.sleep(3)
    it.ejecutar_str(cmd2)
    it.ejecutar_str(f"lxc file push ./transferencias/haproxy.cfg {cont}/etc/haproxy/")
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

    #Si la imágen existe o estamos en modo forzado, 
    #vamos a borrar las imágenes y crearemos la imagen correspondiente
    if force:
        for imagen in data.keys():
            it.ejecutar_str(f"lxc image delete {imagen}")

    logging.info("creando lxdbr0")
    conf.crear_bridge(lxdbr="lxdbr0", ipv4address=f"134.3.0.1")
    
    ct.crear_cont("contTemporal", init= False)
   # ct.crear_cont("db", init= False)
    
    conf.configurar_comunicacion(contenedor="contTemporal",eth="eth0",lxdbr="lxdbr0",address="134.3.0.11",init=True)
   # conf.configurar_comunicacion(contenedor="db",eth="eth0",lxdbr="lxdbr0",address="134.3.0.20",init=True)
    
   # instalar_mongo("db")
    instalar_node("contTemporal")
    it.ejecutar_str("lxc exec contTemporal -- forever start app/rest_server.js") #<--- Esta línea da un error o al menos no funciona
    crear_imagen_de_cont("contTemporal")

if __name__ == "__main__":
    transferir_archivos_proxy("lb")