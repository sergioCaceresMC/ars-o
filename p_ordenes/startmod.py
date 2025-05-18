import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import p_general.contenedores as ct

#El comando start recibe el contenedor a inicializar,
#si no inicializa todos por defecto
#El parámetro bash_test se usa en las pruebas unitarias
def start(vm=None, bash_test=True):
    if (vm is None): 
        ct.iniciar_todo_contenedor(execute_bash=bash_test)
    else:
        ct.iniciar_contenedor(name=vm, exec=bash_test)
