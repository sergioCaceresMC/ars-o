import unittest
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import p_general.contenedores as ct
import p_general.interprete  as it
import p_general.memoria as mem
import p_general.configuraciones as conf

#Pruebas unitarias referentes a la busqueda de contenedores existentes en memoria, 
#comprobación de estado, ip, etc
class TestMemoria(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #creamos un contenedor de prueba
        cls.contenedores = ["pruebaMemoria1","pruebaMemoria2","lb"]  
        alias = ct.verificar_alias("maquina_ubuntu")
        it.ejecutar_str(f"lxc init {alias} {cls.contenedores[0]}")
        it.ejecutar_str(f"lxc init {alias} {cls.contenedores[1]}")
        it.ejecutar_str(f"lxc init {alias} {cls.contenedores[2]}")
        conf.crear_bridge(lxdbr="lxdbr0", ipv4address="10.0.0.1")
        conf.configurar_comunicacion(contenedor=cls.contenedores[0],address=f"10.0.0.120", eth="eth0", lxdbr="lxdbr0")
        conf.configurar_comunicacion(contenedor=cls.contenedores[1],address=f"10.0.0.123", eth="eth0", lxdbr="lxdbr0")
        conf.configurar_comunicacion(contenedor=cls.contenedores[2],address=f"10.0.0.121", eth="eth0", lxdbr="lxdbr0")
    
    @classmethod
    def tearDownClass(cls):
        #Eliminar los contenedores de prueba manualmente
        it.ejecutar_str(f"lxc stop {cls.contenedores[0]} --force")
        it.ejecutar_str(f"lxc stop {cls.contenedores[1]} --force")
        it.ejecutar_str(f"lxc stop {cls.contenedores[2]} --force")
        it.ejecutar_str(f"lxc delete {cls.contenedores[0]}")
        it.ejecutar_str(f"lxc delete {cls.contenedores[1]}")
        it.ejecutar_str(f"lxc delete {cls.contenedores[2]}")

    def test_01_read_data(self):
        contenedores = mem.read_data()
        self.assertIn(self.contenedores[0], contenedores)
        self.assertIn(self.contenedores[1], contenedores)
        self.assertIn(self.contenedores[2], contenedores)
    
    def test_02_exist_data(self):
        self.assertTrue(mem.exist_data(self.contenedores[0]))
        self.assertTrue(mem.exist_data(self.contenedores[1]))
        self.assertTrue(mem.exist_data(self.contenedores[2]))
        self.assertFalse(mem.exist_data("EsteContenedorNoExiste"))

    def test_03_check_status(self):
        self.assertEqual(mem.check_status(self.contenedores[0]), "RUNNING")
        it.ejecutar_str(f"lxc stop {self.contenedores[0]} --force")
        self.assertEqual(mem.check_status(self.contenedores[0]), "STOPPED")

    def test_04_check_networks(self):

        interfaces_memo = mem.check_networks(self.contenedores[1])

        #Verificar el método 
        resultado = it.ejecutar_str(f"lxc list {self.contenedores[1]} --format csv",
            capture=True, tex=True, chec=True)
        
        lineas = resultado.stdout.strip().splitlines()

        interfaces_encontradas = set()

        for linea in lineas:
            partes = linea.split(',')
            if len(partes) > 2:
                ips = partes[2]
                #extraer interfaces entre paréntesis
                interfaces = [ip.split('(')[-1].replace(')', '') for ip in ips.split()]
                interfaces_encontradas.update(interfaces)
        self.assertEqual(interfaces_memo, interfaces_encontradas)

    def test_05_get_ipp_header(self):
        time.sleep(3)
        self.assertEqual(mem.get_ip_header(), "10.0")

if __name__ == "__main__":
    unittest.main(verbosity=2)