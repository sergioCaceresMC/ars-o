import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import p_general.contenedores  as ct
import p_general.memoria as memo

logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.WARNING)

def stop(sv_name=None):

    if (sv_name):

        if memo.read_data().__contains__(sv_name) == False:
            #TODO : LOGGING ERROR"
            logger.error(f"El contenedor {sv_name} no se encuentra en la lista")
            return
        else:
            logger.info(f"Parando el contenedor {sv_name} ")
            ct.detener_contenedor(sv_name)

    else:

        #Logging info 
        logger.info("Procediendo a parar todos los contenedores")
        ct.detener_todo_contenedor()



