import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import p_general.cache as cache
import p_general.memoria as memo

import p_ordenes.createmod as ord_create
import p_ordenes.deletemod as ord_del

def repair(test = False):
    #intentamos obtener la cabecera de la red
    #intentamos leer de caché el número de servidores
    try:
        n_serv = int(cache.leer_cache()[0])
        ip_head = memo.get_ip_header()
    except ValueError as e:
        print(f"Error durante la obtención de datos: {e}")
        sys.exit(1)

    #En caso de test solo queremos ver si consigue bien los datos para el create
    if test: return [n_serv, ip_head]  

    #borramos todo 
    ord_del.delete()
    #creamos todo de nuevo
    ord_create.create(n_servs=n_serv, ip_header=ip_head) 
