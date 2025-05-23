import sys
import os
import logging
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import p_general.contenedores as ct
import p_general.configuraciones as conf
import p_general.cache as cache

import p_ordenes.deletemod as ord_del
import p_ordenes.stopmod as ord_sto

def create(n_servs=2, ip_header="134.3"):
    # Genera el archivo de cache 
    cache.guardar_cache(data=str(n_servs))
    
    try:
        # Creamos los contenedores
        logging.info("creando s")
        ct.crear_varios_cont(name="s",num=n_servs, init=False, 
                             alias="servidorBaseImgSJ2025", 
                             finger="7b17617fc8e1113c40b535ddfcaa8812bcb25b5baafb57b922499d2483ebdeb4")
        
        # Creamos el balanceador
        logging.info("creando balanceador")
        ct.crear_cont(name="lb", init=False)

        # Creamos el cliente
        logging.info("creando cl")
        ct.crear_cont(name="cl", init=False)

        # Creamos base de datos
        logging.info("creando db")
        ct.crear_cont(name="db", init=False)
        
        # Crear el lxdbr0
        logging.info("creando lxdbr0")
        conf.crear_bridge(lxdbr="lxdbr0", ipv4address=f"{ip_header}.0.1")
        
        # Crear el lxdbr0
        logging.info("creando lxdbr1")
        conf.crear_bridge(lxdbr="lxdbr1", ipv4address=f"{ip_header}.1.1")
        
        # Configurar maquinas contenedores
        for i in range(int(n_servs)):
            sv = "s"+str(i+1)
            ad = f"{ip_header}.0.1"+str(i+1)
            logging.info(f"Configurando: {sv} - {ad}")
            conf.configurar_comunicacion(contenedor=sv,eth="eth0",lxdbr="lxdbr0",address=ad,init=False)

        # Configurar cliente
        logging.info("configurando cliente")
        conf.configurar_comunicacion(contenedor="cl",address=f"{ip_header}.1.15", eth="eth0", lxdbr="lxdbr1", init=False)

        # Configurar balanceador
        logging.info("configurando balanceador")
        conf.configurar_comunicacion(contenedor="lb",address=f"{ip_header}.0.10", eth="eth0", lxdbr="lxdbr0", init=False)
        conf.configurar_comunicacion(contenedor="lb",address=f"{ip_header}.1.10", eth="eth1", lxdbr="lxdbr1")
        
        # Configurar base de datos
        conf.configurar_comunicacion(contenedor="db",eth="eth0",lxdbr="lxdbr0",address=f"{ip_header}.0.20",init=False)

        time.sleep(2) # Por algún motivo sin esta pausa no funciona 

        logging.debug("configurando YAML balanceador")
        conf.configurar_yaml_por_sustitucion("lb",eth=["eth0","eth1"])

        logging.info("Ecosistema creado con éxito. Ejecute start para iniciarlo.")


    except ValueError as e:
        logging.error(e)
        logging.error("Fallo catastrófico en algun punto. se borrará el ecosistema para poder intentarlo de nuevo")
        ord_del.delete()