import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

comms ={
    "add": "Definido como: python pfinal.py add <opt: number>. Añade al entorno el número indicado de servidores, si no se indica, crea 1 por defecto.",
    "create": "Definido como: python pfinal.py create <opt: num servidores> <opt: cabecera ip>. Crea el número de servidores definido por el usuario, o 2 por defecto. Si no se especifica, la cabecera IP será 134.3 ",
    "delete": "Definido como: python pfinal.py delete <opt: servidor>. Borra todo el entorno o un servidor en específico si se indica.",
    "help": "Definido como: python pfinal.py help. Muestra las órdenes posibles.",
    "list": "Definido como: python pfinal.py list. Lista la información, se puede especificar mediante input si se quiere info detallada de alguno",
    "start": "Definido como: python pfinal.py start <opt: servidor>. Arranca una máquina si se especifica, o todas las máquinas por defecto.",
    "stop": "Definido como: python pfinal.py stop <opt: servidor>. Detiene una máquina si se especifica, o todas las máquinas por defecto."

}

def get_help():
    print("Órdenes disponibles: ")
    for comm, desc in comms.items():
        print(f"- {comm} - {desc}")

if __name__ == "__main__":
    get_help()