import sys
import logging

#Ordenes de entrada definidas:
list_args = ["create","start","list","delete","stop","add","help","repair"]

#Comprobamos que el valor de la orden introducida sea correcto
def validate_p1_input(argum):
    if argum[1] not in list_args or len(argum)==1:
        logging.debug(
            f'''
            Actualmente, las acciones definidas no contienen la que llamas en validación,
            evaluar si no es correcto
            '''
        )
        raise ValueError(
            f'''
            Accion incorrecta o no definida, has introducido: {argum[1]}.
            Llama a help si quieres ver las acciones posibles
            '''
        )

def validate_create(argum):

    # Comprobamos que el numero de parametros de la orden sea correcta 
    if len(argum) not in [2,3,4]:
        raise ValueError(
            f'''
            Numero incorrecto de parametros. Se han introducido {len(argum)}
            parametros, y deberia haber 2, 3 o 4
            '''
        )

    if len(argum) == 2: 
        logging.warning(
            f'''
            no se han definido el numero de servidores, ni IP. 
            Se crearan 2 por defecto con cabecera 134.3.
            '''
        )

    elif 1<=int(argum[2])<=5: 
        logging.info("El numero de servidores a crear es un numero correcto") 
        
    else: 
        raise ValueError(
            f'''
            Valor de numero de servidores incorrecto, debe estar contenido entre 1 y 5
            o no definirse. Se indicó como valor: { argum[2]}
            '''
        ) 

    if  len(argum) > 3 and argum[3] != '':
        vals_num_ip = argum[3].split(".")

        if len(vals_num_ip) != 2:
            raise ValueError(f"Cabecera de ip mal definida, esta debe ser de la forma pt1.pt2: {argum[3]}")

        for elem in vals_num_ip:
            if not elem.isdigit():
                raise ValueError(f"Se ha especificado una cabecera de ip que no es numerica completa: {argum[3]}")

        logging.debug("Valor de cabecera correcto")

def validate_delete(argum):
    if len(argum) not in [2,3]:
        raise ValueError(
            f'''
            Numero incorrecto de parametros. Se han introducido {len(argum)}
            parametros, y deberia haber 2 o 3
            '''
        )

    if len(argum) == 2: 
        borrar_todo = input(
            f'''
            No has definido un servidor en concreto, esto hará que se borre todo el escenario.
            ¿Estás seguro? (Y,n):
            '''
            )
        if borrar_todo.lower != "y":
            sys.exit

def validate_list(argum):
    if len(argum) != 2:
        raise ValueError(
            f'''
            Numero incorrecto de parametros. Se han introducido {len(argum)}
            parametros, y list solo soporta 2.
            '''
        )

def validate_delete(argum):
    if len(argum) not in [2,3]:
        raise ValueError(
            f'''
            Numero incorrecto de parametros. Se han introducido {len(argum)}
            parametros, y deberia haber 2 o 3
            '''
        )

# NO SE VALIDA EL NOMBRE DEL SERVIDOR A PARAR, ESO LO HACE DIRECTAMENTE EL CODIGO DE STOP, ESTO SOLO VERIFICA QUE SE HAN INTRODUCIDO UNOS PARÁMETROS QUE NO ACARREAN ERRORES  
def validate_stop(argum):
    if len(argum) not in [2,3]:
        raise ValueError(
            f'''
            Numero incorrecto de parametros. Se han introducido {len(argum)}
            parametros, y deberia haber 2 o 3
            '''
        )

# NO SE VALIDA EL NOMBRE DEL SERVIDOR A PARAR, ESO LO HACE DIRECTAMENTE EL CODIGO DE START, ESTO SOLO VERIFICA QUE SE HAN INTRODUCIDO UNOS PARÁMETROS QUE NO ACARREAN ERRORES  
def validate_start(argum):
    if len(argum) not in [2,3]:
        raise ValueError(
            f'''
            Numero incorrecto de parametros. Se han introducido {len(argum)}
            parametros, y deberia haber 2 o 3
            '''
        )

def validate_help(argum):
    if len(argum) != 2:
        raise ValueError(
            f'''
            Numero incorrecto de parametros. Se han introducido {len(argum)}
            parametros, y help solo soporta 2.
            '''
        )

def validate_add(argum):
    if len(argum) not in [2,3]:
        raise ValueError(
            f'''
            Numero incorrecto de parametros. Se han introducido {len(argum)}
            parametros, y deberia haber 2 o 3
            '''
        )

def validate_repair(argum):
    if len(argum) != 2:
        raise ValueError(
            f'''
            Numero incorrecto de parametros. Se han introducido {len(argum)}
            parametros, y repair solo soporta 2.
            '''
        )
