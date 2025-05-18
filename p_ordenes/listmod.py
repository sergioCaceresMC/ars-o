import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import p_general.memoria  as memo

logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.WARNING)

def lista_info():
    
    # Lista de la informacion de los contenedores
    memo.lista_info_all()

    # Si el usuario quiere, proporcionamos tambien el network info 
    quiere_info = input("¿Desea conocer también información más en profundidad de alguno? (y/N): ")

    if quiere_info == "y":

    #Contenedores creados
        lista_nombres = memo.read_data()

        #LOGGER INFO 
        logger.info(f"Contenedores: {lista_nombres}")

        quiere_uno = input("Indique aquí de cual de los listados: ")
        
        if quiere_uno != "" and (quiere_uno in lista_nombres):
            memo.lista_info_indiv_extended(quiere_uno)
        else:
            # ERROR LOG   
            logger.error("El contenedor especificado está mal escrito o no se encuentra en el entorno")
