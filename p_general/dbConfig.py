import subprocess
import logging
import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import p_general.interprete as it
import contenedores as ct


Ip = "134.3.0.20"

def crear_db():
   # TODO: HACER COMO EN CONFIGURACIONES DE METER LOS PARÁM, SOBRETODO PARA DIR IPV4 -- HASTA AQUI FUNCIONA BIEN
    it.ejecutar_str(f"lxc init ubuntu2004 db")
    it.ejecutar_str(f"lxc network attach lxdbr0 db eth0")
    it.ejecutar_str(f"lxc config device set db eth0 ipv4.address {Ip}")
    it.ejecutar_str(f'lxc start db')

def instal_mongoDB():
    
    # Instlación de la aplicación de la base de datos mongoDB
    it.ejecutar_str(f"lxc exec db -- apt update")
    it.ejecutar_str(f"lxc exec db -- apt install -y mongodb")
    subprocess.run(["lxc", "exec", "db", "--", "bash", "-c","sed -i 's/^bind_ip = 127.0.0.1/bind_ip = 127.0.0.1,134.3.0.20/' /etc/mongodb.conf"])
    
    #it.ejecutar_str(f"lxc exec db -- bash -c 'sed -i 's/^bind_ip = 127.0.0.1/bind_ip = 127.0.0.1,134.3.0.20/' /etc/mongodb.conf'")# ESTA LÑINEA DA ERROR X UNEXPECTED EOF Y UNEXPECTED END OF FILE  
    it.ejecutar_str(f"lxc restart db")


if __name__ == "__main__":
    instal_mongoDB()