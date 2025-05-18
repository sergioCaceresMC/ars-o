import sys
import os
import logging 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import p_general.contenedores  as ct
import p_general.interprete as it
import p_general.memoria as memo
import p_general.cache as cache
import p_general.configuraciones as conf

#logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.WARNING)

def lista_contenedores_filtrada():
    #Obtenemos los nombres de los contenedores inicializados
    result = it.ejecutar_str("lxc list --format csv", capture=True, tex=True)
    lines = result.stdout.splitlines()

    lista_nombres = [] 
    for line in lines:
        lista_nombres.append(line.split(',')[0])
    
    lista_filtrada = []
    for elem in lista_nombres:
        if len(elem)>1 and elem[0] == "s":
            lista_filtrada.append(elem)
        else:
        #LOGGER DEBUG -- NO PARA EL USUARIO 
            logging.debug(f"Este contenedor no es un servidor del escenario: {elem}")

    return lista_filtrada

def delete(sv_name=None):
   
    list_servidores = lista_contenedores_filtrada()
        
    if(sv_name):
        #Si se especifica, se borra el servidor indicado 

        if (sv_name in list_servidores):
            ct.delete_contenedor(sv_name)
            new_data = int(cache.leer_cache()[0]) - 1
            cache.guardar_cache(str(new_data))
        else:
           #ERROR/WARNING? EN LOGGER 
            logging.warning(f"El servidor que se desea borrar no existe o no tiene la notación correcta: {sv_name}")

    else:
        #Borra todos los servidores en función al numero en cache
        if len(list_servidores) != int(cache.leer_cache()[0]):
            #Warning de logger: 
            logging.warning(
                "FALLO DE CONSISTENCIA: No coincide el caché con los servidores," 
                "esto implica que hay servidores con nombre mal definido." 
                "Se procederá a borrar aquellos que comiencen con s:")

        for elem in list_servidores:
            ct.delete_contenedor(elem)
        
        #Guardamos un 0 en el caché 
        cache.guardar_cache("0")

        #Borra el cliente 
        ct.delete_contenedor("cl")

        #Borrar el balanceador de carga
        ct.delete_contenedor("lb")

        # Borra los bridges
        conf.delete_network("lxdbr1")


