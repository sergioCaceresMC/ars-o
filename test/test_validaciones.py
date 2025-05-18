import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from p_general import contenedores as ct
from p_general import interprete as it
from p_general import memoria as mem
from p_general import validaciones as val



# Pruebas unitarias referentes a la creación, eliminación, inicio, detener contenedores
class TestValidaciones(unittest.TestCase):
    
    def test_01_ordenes_validas(self):
        
        val.validate_p1_input(["pfinal1.py", "create", "2"])
        val.validate_p1_input(["pfinal1.py", "create", "2", "134.1"])
        val.validate_p1_input(["pfinal1.py", "create"])
        val.validate_p1_input(["pfinal1.py", "add"])
        val.validate_p1_input(["pfinal1.py", "add", "1"])
        val.validate_p1_input(["pfinal1.py", "delete"])
        val.validate_p1_input(["pfinal1.py", "delete", "s1"])
        val.validate_p1_input(["pfinal1.py", "start"])
        val.validate_p1_input(["pfinal1.py", "start", "s1"])
        val.validate_p1_input(["pfinal1.py", "stop"])
        val.validate_p1_input(["pfinal1.py", "stop", "s1"])

        with self.assertRaises(Exception):
            val.validate_p1_input(["pfinal1.py"])
            val.validate_p1_input(["pfinal1.py", "comandoInexistente"])

    def test_02_create(self):
        val.validate_create(["pfinal1.py", "create", "2"])
        val.validate_create(["pfinal1.py", "create"])
        val.validate_create(["pfinal1.py", "create", "2", "10.0"])

        with self.assertRaises(Exception):
            val.validate_create(["pfinal1.py", "create", "10"])
            val.validate_create(["pfinal1.py", "create", "1", "parametroExtra"])

    def test_03_add(self):
        val.validate_add(["pfinal1.py", "add", "2"])
        val.validate_add(["pfinal1.py", "add"])

        with self.assertRaises(Exception):
            val.validate_add(["pfinal1.py", "add", "1", "parametroExtra"])

    def test_04_delete(self):
        val.validate_delete(["pfinal1.py", "delete"])
        val.validate_delete(["pfinal1.py", "delete", "s2"])
    
        with self.assertRaises(Exception):
            val.validate_delete(["pfinal1.py", "delete", "s1", "parametroExtra"])

    def test_05_help(self):
        pass

    def test_06_start(self):
        val.validate_start(["pfinal1.py", "delete"])
        val.validate_start(["pfinal1.py", "delete", "s2"])

        with self.assertRaises(Exception):
            val.validate_start(["pfinal1.py", "delete", "s1", "parametroExtra"])

    def test_07_stop(self):
        val.validate_stop(["pfinal1.py", "stop"])
        val.validate_stop(["pfinal1.py", "stop", "s2"])

        with self.assertRaises(Exception):
            val.validate_stop(["pfinal1.py", "stop", "s1", "parametroExtra"])

    def test_08_list(self):
        val.validate_list(["pfinal1.py", "list"])

        with self.assertRaises(Exception):
            val.validate_list(["pfinal1.py", "list", "parametroExtra"])

    def test_09_repair(self):
        val.validate_repair(["pfinal1.py", "repair"])

        with self.assertRaises(Exception):
            val.validate_repair(["pfinal1.py", "repair", "parametroExtra"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
   