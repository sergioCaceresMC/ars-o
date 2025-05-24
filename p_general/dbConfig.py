import subprocess
import logging
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import p_general.interprete as it
import p_general.contenedores as ct
import p_general.memoria as mem


Ip = "134.3.0.20"

def crear_db():
   # TODO: HACER COMO EN CONFIGURACIONES DE METER LOS PARÁM, SOBRETODO PARA DIR IPV4 -- HASTA AQUI FUNCIONA BIEN
    ct.crear_cont("db", init=False)
    it.ejecutar_str(f"lxc network attach lxdbr0 db eth0")
    it.ejecutar_str(f"lxc config device set db eth0 ipv4.address {Ip}")
    it.ejecutar_str(f'lxc start db')
 
def instal_mongoDB():
    
    if mem.check_status("db") == "STOPPED": it.ejecutar_str(f"lxc start db")
    # Instlación de la aplicación de la base de datos mongoDB
    it.ejecutar_str(f"lxc exec db -- apt update")
    it.ejecutar_str(f"lxc exec db -- apt install -y mongodb")
    subprocess.run(["lxc", "exec", "db", "--", "bash", "-c",f"sed -i 's/^bind_ip = 127.0.0.1/bind_ip = 127.0.0.1,{mem.get_ip_header()}.0.20/' /etc/mongodb.conf"])
    
    #it.ejecutar_str(f"lxc exec db -- bash -c 'sed -i 's/^bind_ip = 127.0.0.1/bind_ip = 127.0.0.1,134.3.0.20/' /etc/mongodb.conf'")# ESTA LÑINEA DA ERROR X UNEXPECTED EOF Y UNEXPECTED END OF FILE  
    it.ejecutar_str(f"lxc restart db")

# espera a que el contenedor tenga red para poder hacer el install bien, si no da error
def wait_network(ct_name, timeout=60, interval=3):
    init_time = time.time()
    while True:
        try:
            result = subprocess.run(
                ["lxc", "exec", ct_name, "--", "ping", "-c", "1", "-W", "1", "8.8.8.8"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            net_result = result.stdout or ""
        except Exception as e:
            net_result = ""

        if "1 received" in net_result or "bytes from" in net_result:
            return True

        if time.time() - init_time > timeout:
            return False

        time.sleep(interval)


if __name__ == "__main__":
    crear_db()
    wait_network("db")
    instal_mongoDB()

