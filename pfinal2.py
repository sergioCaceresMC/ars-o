#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import logging

from p_ordenes.createmod import create
from p_ordenes.deletemod import delete
from p_ordenes.stopmod import stop
from p_ordenes.startmod import start
from p_ordenes.listmod import lista_info
from p_ordenes.helpmod import get_help
from p_ordenes.repairmod import repair
from p_ordenes.addmod import add
from p_ordenes.configmod import configurar

from p_general import validaciones as val

logger = logging.getLogger(__name__)

def main():
    l = sys.argv
    
    #Esto meter a log info 
    logger.info(print(l))

    #comando: python3 pfinal1.py <orden> <parámetros>

    try:
        val.validate_p1_input(l)
    except ValueError as e:
        print(f"Error durante la validación: {e}")
        sys.exit(1)
    
    orden = l[1]

    if  orden == "create":
        try:
            val.validate_create(l)
        except ValueError as e:
            print(f"Error durante la validación: {e}")
            sys.exit(1)
            
        if(len(l) > 3):
            serv_n = int(sys.argv[2])
            ip_header = sys.argv[3]
            print(serv_n)
            create(n_servs=serv_n,ip_header=ip_header)
        elif(len(l) == 3):
            serv_n = int(sys.argv[2])
            create(n_servs=serv_n)
        else:
            create() 
    
    elif orden == "delete":
        try:
            val.validate_delete(l)
        except ValueError as e:
            print(f"Error durante la validación: {e}")
            sys.exit(1)

        if(len(l) > 2):
            serv_name = sys.argv[2]
            delete(sv_name=serv_name)
        else:
            delete()        
    
    elif orden == "list":
        try:
            val.validate_list(l)
        except ValueError as e:
            print(f"Error durante la validación: {e}")
            sys.exit(1)
        lista_info()

    elif orden == "stop":
        try:
            val.validate_stop(l)
        except ValueError as e:
            print(f"Error durante la validación: {e}")
            sys.exit(1)

        if(len(l) > 2):
            serv_name = sys.argv[2]
            stop(sv_name=serv_name)
        else:
            stop()        
    
    elif orden == "start":
        try:
            val.validate_start(l)
        except ValueError as e:
            print(f"Error durante la validación: {e}")
            sys.exit(1)

        if(len(l) > 2):
            serv_name = sys.argv[2]
            start(vm = serv_name)
        else:
            start()

    elif orden == "help":
        try:
            val.validate_help(l)
        except ValueError as e:
            print(f"Error durante la validación: {e}")
            sys.exit(1)
        get_help()

    elif orden == "repair":
        try:
            val.validate_repair(l)
        except ValueError as e:
            print(f"Error durante la validación: {e}")
            sys.exit(1)
        repair()

    elif orden == "add":
        try:
            val.validate_add(l)
        except ValueError as e:
            print(f"Error durante la validación: {e}")
            sys.exit(1)
        if(len(l) > 2):
            serv_name = sys.argv[2]
            add(numero = serv_name)
        else:
            add()
    elif orden == "config":
        try:
            val.validate_config(l)
        except ValueError as e:
            print(f"Error durante la validación: {e}")
            sys.exit(1)
        configurar()

if __name__ == "__main__":
    main()