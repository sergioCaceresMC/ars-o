import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import p_general.contenedores as ct
import p_general.configuraciones as conf
import p_general.cache as cache
import p_general.memoria as memo


def add(numero = "1"):

    n_contedores = int(numero)
    ip_head = memo.get_ip_header()

    #Crea los contenedores pedidos continuando con la numeración 
    new_data = int(cache.leer_cache()[0])

    #configurar maquinas contenedores
    contador = 1
    cont_actual = 1
    while(contador <= n_contedores):
        if memo.exist_data(f"s{cont_actual}"):
            cont_actual += 1
            continue
        sv = "s"+str(cont_actual)
        ct.crear_cont(sv, init=False, alias="servidorBaseImgSJ2025", finger="7b17617fc8e1113c40b535ddfcaa8812bcb25b5baafb57b922499d2483ebdeb4")
        ad = f"{ip_head}.0.1"+str(cont_actual)
        logging.info(f"configurando: {sv} - {ad}")
        conf.configurar_comunicacion(contenedor=sv,eth="eth0",lxdbr="lxdbr0",address=ad, init=False)
        contador += 1
        new_data += 1
        cont_actual += 1
    
    cache.guardar_cache(str(new_data))
    
