import unittest
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from p_general import contenedores as ct
from p_general import memoria as mem
from p_general import cache as cache

from p_ordenes import createmod as ord_create
from p_ordenes import stopmod as ord_stop
from p_ordenes import startmod as ord_start
from p_ordenes import deletemod as ord_delete
from p_ordenes import repairmod as ord_repair
from p_ordenes import addmod as ord_add



# Pruebas unitarias referentes a las ordenes del programa
class TestOrdenes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vms_esperadas = ["s1", "s2", "s3", "lb", "cl"]
        cls.vm_esperadaNueva = "s4"
        cls.vms_esperadaNuevas = ["s5","s6"]
        ord_create.create(n_servs=3)
        cls.contenedor = "contenedorPruebaOrdenes"
        ct.crear_cont(cls.contenedor) 
        cls.cache_value = int(cache.leer_cache()[0])
        ord_start.start(bash_test=False)

    @classmethod
    def tearDownClass(cls):
        ct.delete_contenedor(cls.contenedor)
        for cont in cls.vms_esperadas:
            ct.delete_contenedor(cont)
        #ct.delete_varios_contenedores(cls.vms_esperadas)

    def test_01_create_contenedores(self):

        #testear que existen los servidores correctos
        vms = mem.read_data()

        for name in self.vms_esperadas:
            with self.subTest(vm=name):
                self.assertIn(name, vms)

    def test_02_create_networks_servidores(self):
        #testear que contienen la red bien configurada
        networks_esperadas = {
            "s1": "134.3.0.11",
            "s2": "134.3.0.12",
            "s3": "134.3.0.13"
        }

        for vm, ip in networks_esperadas.items():
            with self.subTest(vm=vm):
                s_red = mem.check_networks(vm)
                self.assertIn("eth0", s_red)
                self.assertIn(ip, s_red)

    def test_03_create_networks_balanceador(self):
        
        time.sleep(10)

        interfaces_memo = mem.check_networks("lb")
        #print(interfaces_memo)
        self.assertIn("eth1", interfaces_memo)

    def test_04_create_networks_cliente(self):

        s_red = mem.check_networks("cl")
        self.assertIn("eth0", s_red)
        self.assertIn("134.3.1.15", s_red)

    def test_05_stop(self):
        #Iniciar contenedores 
        for cont in self.vms_esperadas:
            ct.iniciar_contenedor(cont, False)

        ord_stop.stop()

        #Testear que todas las máquinas estén apagadas
        for name in self.vms_esperadas:
            with self.subTest(vm=name):
                estado = mem.check_status(name)
                self.assertIn(estado, "STOPPED")
    
    def test_06_start(self):
        #Detener los contenedores para la prueba 
        for cont in self.vms_esperadas:
            ct.detener_contenedor(cont)

        #Iniciamos pero sin que abra el bash 
        ord_start.start(bash_test=False)

        #testear que todas las máquinas estén encendidas
        for name in self.vms_esperadas:
            with self.subTest(vm=name):
                estado = mem.check_status(name)
                self.assertIn(estado, "RUNNING")

    def test_07_stop_one(self):
        if mem.check_status(self.vms_esperadas[0]) == "STOPPED": ct.iniciar_contenedor(self.vms_esperadas[0],exec=False)
        ord_stop.stop(self.vms_esperadas[0])

    def test_08_start_one(self):
        if mem.check_status(self.vms_esperadas[0]) == "RUNNING": ct.detener_contenedor(self.vms_esperadas[0])
        ord_start.start(self.vms_esperadas[0], bash_test=False)
    
    def test_09_repair(self):
        self.assertEqual(ord_repair.repair(test = True), [self.cache_value, "134.3"])

    def test_10_add_one(self):
        cache_guardado = int(cache.leer_cache()[0])
        ord_add.add()
        self.assertTrue(mem.exist_data(self.vm_esperadaNueva))
        cache_final = int(cache.leer_cache()[0])
        self.assertTrue((cache_final-cache_guardado)==1)
    
    def test_11_add_many(self):
        cache_guardado = int(cache.leer_cache()[0])
        ord_add.add(numero=2)
        self.assertTrue(mem.exist_data(self.vms_esperadaNuevas[0]))
        self.assertTrue(mem.exist_data(self.vms_esperadaNuevas[1]))
        cache_final = int(cache.leer_cache()[0])
        self.assertTrue((cache_final-cache_guardado)==2)
    
    def test_12_delete_one_server(self):
        cache_guardado = int(cache.leer_cache()[0])
        ord_delete.delete(self.vms_esperadas[0])
        self.assertFalse(mem.exist_data(self.vms_esperadas[0]))
        cache_final = int(cache.leer_cache()[0])
        self.assertTrue((cache_guardado-cache_final)==1)

    
    def test_13_delete_all(self):
        ord_delete.delete()
        vms = mem.read_data()
        for name in self.vms_esperadas:
            with self.subTest(vm=name):
                self.assertNotIn(name, vms)
        cache_final = int(cache.leer_cache()[0])
        self.assertTrue(cache_final==0)
        #Comprobar que no borra contenedores de otros ecosistemas 
        self.assertTrue(mem.exist_data(self.contenedor)) 
    

if __name__ == "__main__":
    unittest.main(verbosity=2)
    
    '''
    suite = unittest.TestSuite()
    suite.addTest(TestOrdenes("test_03_create_networks_balanceador"))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    '''