import sys
import os
import logging
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import p_general.contenedores as ct
import p_general.lbConfig as lbconf
import p_general.svConfig as svconf
import p_general.dbConfig as dbconf

def configurar():
    dbconf.crear_db()
    dbconf.wait_network("db")
    dbconf.instal_mongoDB()
    lbconf.instalar_proxy("lb")