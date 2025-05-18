import os
import logging
import subprocess

import p_general.interprete as it
import p_general.memoria as sv

logging.basicConfig(level=logging.DEBUG)


#Ruta base relativa a pfinal2.py
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

#Ruta a los archivos dentro de la carpetea imágenes
RUTA_SERVIDORES = os.path.join(BASE_DIR, "imgs", "fichero.trg")
RUTA_BALANCEADOR = os.path.join(BASE_DIR, "imgs", "fichero.trg")
RUTA_DATABASE = os.path.join(BASE_DIR, "imgs", "fichero.trg")

#función que permite usar las rutas
def get_ruta(ruta):
    if ruta == "sv": return RUTA_SERVIDORES
    elif ruta == "lb": return RUTA_BALANCEADOR
    elif ruta == "db": return RUTA_DATABASE
    else: return "/mnt/vnx/repo/arso/ubuntu2004.tar.gz"

#Verificamos si el alias de la imagen es correcto.
#Devuelve el valor del alias correcto
def verificar_alias(alias, 
                    finger="554c4f7c1ffe", 
                    impo="/mnt/vnx/repo/arso/ubuntu2004.tar.gz"):
    
    # Verificamos si la imagen con el alias ya existe
    resultado = it.ejecutar_str("lxc image list --format csv", capture=True, tex=True)
    salida = resultado.stdout.strip().split('\n')
    
    # Creamos un diccionario donde la llave es el fingerprint y el valor es alias
    data = {}
    for linea in salida:
        columnas = linea.split(',')
        if len(columnas) > 1:
            alias_encontrado, fingerprint = columnas[0], columnas[1]
            data[fingerprint] = alias_encontrado

    # Solución 1: Fuerza bruta
    
    if finger in data.keys(): return data.get(finger)
    
    #Solución situacional
    if alias in data.values(): return alias

    # Solución 2: Fuerza bruta pero solo si es necesario  
    
    if alias not in data.values():
        try:
            it.ejecutar_str(f"lxc image import {impo} --alias {alias}", 
                            capture=True, 
                            tex=True, 
                            chec=True)
            true_alias = alias
        except Exception as e:
            print("Hora de matar")
            
            for imagen in data.values():
                it.ejecutar_str(f"lxc image delete {imagen}")

            it.ejecutar_str(f"lxc image import {impo} --alias {alias}", 
                            capture=True, 
                            tex=True, 
                            chec=True)
            true_alias = alias
    
    return true_alias

#Crear contenedor
def crear_cont(name = "vm", 
               alias = "maquina_buntu",
               finger="554c4f7c1ffe", 
               impo="/mnt/vnx/repo/arso/ubuntu2004.tar.gz",
               init = True):
    true_alias = verificar_alias(alias=alias, finger=finger, impo=impo)
    if init: it.ejecutar_str(f"lxc launch {true_alias} {name}")
    else: it.ejecutar_str(f"lxc init {true_alias} {name}")

#Crear varios contenedores
def crear_varios_cont(name = "vm", 
                      num = "1",
                      desde=0, 
                      alias="maquina_buntu", 
                      finger="554c4f7c1ffe" , 
                      impo="/mnt/vnx/repo/arso/ubuntu2004.tar.gz", 
                      init=True):
    for i in range(int(num)):
        crear_cont(name = name+str(i+1+desde), alias=alias, finger=finger, impo=impo, init=init)
        
#Borrar un contenedor en específico
def delete_contenedor(contenedor):

    #Comprobamos si el contenedor existe
    if sv.exist_data(contenedor) == False:
        logging.error(f"El contenedor {contenedor} no existe")
        return
    #Comprobamos si el contenedor está encendido
    if sv.check_status(contenedor=contenedor) == "RUNNING": it.ejecutar_str(f"lxc stop {contenedor} --force")
    it.ejecutar_str(f"lxc delete {contenedor}")

#Iniciar contenedor
def iniciar_contenedor(name, exec=True):

    #Comprobamos si el contenedor existe 
    if not sv.exist_data(name):
        logging.error(f"Error: El contenedor {name} no existe")
        return

    #Iniciamos contenedor
    if sv.check_status(contenedor=name) == "STOPPED": it.ejecutar_str(f"lxc start {name}")
    
    #Abrimos terminal del contenedor en caso de no estar en un test
    if exec:
        orden = f"lxc exec {name} bash"
        subprocess.Popen(["xterm", "-e", orden])

#Iniciar todos los contenedores
def iniciar_todo_contenedor(execute_bash = True):
    lista = sv.read_data()
    for contenedor in lista:
        iniciar_contenedor(contenedor, exec=execute_bash)#Quitar el exec luego 

# #función optimizada con menos llamadas a memoria
# def iniciar_varios_contenedores(names = [''], exec = True):
#     memoria = sv.read_data()
#     for contenedor in memoria:
#         if (contenedor in names) and (sv.check_status(contenedor=contenedor) == "STOPPED"):
#             logging.info(f"iniciando {contenedor}")
#             it.ejecutar_str(f"lxc start {contenedor}")
#             #abrimos terminal del contenedor
#             if exec == True: it.ejecutar_str(f'xterm-e "lxc exec {contenedor} bash"')

#Detener contenedor
def detener_contenedor(name):
    if not sv.exist_data(name):
        logging.error(f"Error: El contenedor {name} no existe")
        return
    
    if sv.check_status(contenedor=name) == "RUNNING": it.ejecutar_str(f"lxc stop {name} --force")
    
#Detener todos los contenedores del sistema. No solo los del ecosistema
def detener_todo_contenedor():
    it.ejecutar_str("lxc stop --all")



