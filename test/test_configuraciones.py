import unittest
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from p_general import contenedores as ct
from p_general import interprete as it
from p_general import configuraciones as conf
from p_general import memoria as memo


# Pruebas unitarias referentes a la creación, eliminación, y configuraciones de las redes
class TestConfiguracion(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.contenedor = "contenedorPruebaConfig"
        cls.contenedor2 = "contenedorPruebaConfig2"
        ct.crear_cont(cls.contenedor, init=False) 
        ct.crear_cont(cls.contenedor2, init=False)
        #ct.iniciar_contenedor(cls.contenedor, exec=False)
        #ct.iniciar_contenedor(cls.contenedor2, exec=False) 

    @classmethod
    def tearDownClass(cls):
      ct.delete_contenedor(cls.contenedor)
      ct.delete_contenedor(cls.contenedor2)
      it.ejecutar_str("lxc network delete lxdbr12efg04")
      pass

    def test_01_crear_bridges(self):
        conf.crear_bridge(lxdbr="lxdbr12efg04", ipv4address="10.0.1.1")
        conf.crear_bridge(lxdbr="lxdbr0", ipv4address="10.0.0.1")

        resp = it.ejecutar_str("lxc network get lxdbr12efg04 ipv4.address", capture=True)
        resp = resp.stdout.decode("utf-8").strip()
        
        resp2 = it.ejecutar_str("lxc network get lxdbr0 ipv4.address", capture=True)
        resp2 = resp2.stdout.decode("utf-8").strip()
        
        self.assertEqual(resp, "10.0.1.1/24") 
        self.assertEqual(resp2, "10.0.0.1/24") 

    def test_02_configurar_comunicacion(self):
        conf.configurar_comunicacion(contenedor=self.contenedor,address=f"10.0.0.10", eth="eth0", lxdbr="lxdbr0", init=False)
        conf.configurar_comunicacion(contenedor=self.contenedor,address=f"10.0.1.10", eth="eth1", lxdbr="lxdbr12efg04")
        
        conf.configurar_comunicacion(contenedor=self.contenedor2,address=f"10.0.1.11", eth="eth0", lxdbr="lxdbr12efg04")

        resp = it.ejecutar_str(f"lxc info {self.contenedor}", capture=True)
        resp = resp.stdout.decode("utf-8")
        self.assertIn("eth1", resp)

    def test_03_configurar_eth_de_contenedor(self):
        conf.configurar_yaml_por_sustitucion(cont=self.contenedor, eth=["eth0","eth1"])

        time.sleep(5)

        interfaces_memo = memo.check_networks(self.contenedor)
        self.assertIn("10.0.0.10", interfaces_memo)
        self.assertIn("10.0.1.11", interfaces_memo)

    def test_04_eliminar_network(self):
        conf.delete_network("lxdbr12efg04")
        
        result = it.ejecutar_str("lxc network list --format csv", capture=True, tex=True, chec=True)
        lineas = result.stdout.strip().splitlines()
        redes = [linea.split(',')[0] for linea in lineas]

        self.assertNotIn("lxdbr12efg04", redes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
    '''
    suite = unittest.TestSuite()
    suite.addTest(TestConfiguracion("test_03_configurar_eth_de_contenedor"))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    '''