import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from p_general import contenedores as ct
from p_general.interprete import ejecutar_str as ejec
from p_general import memoria as mem



# Pruebas unitarias referentes a la creación, eliminación, inicio, detener contenedores
class TestContenedores(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #creamos un contenedor de prueba
        cls.contenedor = "pruebaContenedor" 
        alias = ct.verificar_alias("maquina_ubuntu")
        ejec(f"lxc launch {alias} {cls.contenedor}")
        ejec(f"lxc stop {cls.contenedor} --force")

    @classmethod
    def tearDownClass(cls):
        #eliminar los contenedores de prueba 
        if mem.check_status(cls.contenedor) == "RUNNING": ejec(f"lxc stop {cls.contenedor} --force")
        ejec(f"lxc delete {cls.contenedor}")

        if mem.exist_data("contenedorPruebaTest1"):
            ejec(f"lxc stop contenedorPruebaTest1 --force")
            ejec(f"lxc delete contenedorPruebaTest1")

        if mem.exist_data("variosContenedoresPrueba1"):
            ejec(f"lxc stop variosContenedoresPrueba1 --force")
            ejec(f"lxc delete variosContenedoresPrueba1")
        
        if mem.exist_data("variosContenedoresPrueba2"):
            ejec(f"lxc stop variosContenedoresPrueba2 --force")
            ejec(f"lxc delete variosContenedoresPrueba2")

    def test_01_crear_contenedor(self):
        ct.crear_cont("contenedorPruebaTest1")
        self.assertTrue(mem.exist_data("contenedorPruebaTest1"))

    def test_02_eliminar_contenedor(self):
        ct.delete_contenedor("contenedorPruebaTest1")
        self.assertFalse(mem.exist_data("contenedorPruebaTest1"))

    def test_03_crear_varios_contenedores(self):
        ct.crear_varios_cont("variosContenedoresPrueba", "2")
        self.assertTrue(mem.exist_data("variosContenedoresPrueba1"))
        self.assertTrue(mem.exist_data("variosContenedoresPrueba2"))

    def test_04_iniciar_contenedor(self):
        ct.iniciar_contenedor(self.contenedor, exec=False)
        self.assertCountEqual(mem.check_status(self.contenedor), "RUNNING")

    def test_05_iniciar_contenedor_inexistente(self):
        with self.assertLogs(level='ERROR') as cm:
            ct.iniciar_contenedor("contenedorInexistente", exec=False)
        self.assertIn("El contenedor contenedorInexistente no existe", cm.output[0])

    def test_06_detener_contenedor(self):
        ct.detener_contenedor(self.contenedor)
        self.assertCountEqual(mem.check_status(self.contenedor), "STOPPED")

    def test_07_detener_contenedor_inexistente(self):
        with self.assertLogs(level='ERROR') as cm:
            ct.detener_contenedor("contenedorInexistente")
        self.assertIn("El contenedor contenedorInexistente no existe", cm.output[0])

    def test_08_eliminar_varios_contenedores(self):
        contenedores = ["variosContenedoresPrueba1", "variosContenedoresPrueba2"]
        if mem.check_status(contenedores[0]) == "STOPPED": ejec(f"lxc start {contenedores[0]}")
        ct.delete_varios_contenedores(contenedores)

        self.assertFalse(mem.exist_data(contenedores[0]))
        self.assertFalse(mem.exist_data(contenedores[1]))

if __name__ == "__main__":
    unittest.main(verbosity=2)
   
    '''''
    suite = unittest.TestSuite()
    suite.addTest(TestContenedores("test_04_iniciar_contenedor"))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    '''


