import p_general.interprete as it

#ruta de guardado de cache
cache_url = "./cache.txt"

#Salvar datos en un archivo que se ubica en la carpeta donde se ejecuta la terminal. 
#No donde está el programa.
def guardar_cache(data = "",t="w"):
    with open(cache_url, t) as fich:
        if data != "":
            fich.write(data+"\n")
        fich.close()

#Eliminar las lineas vacías del cache ***
def limpiar_cache():
    datos_limpios = "\n".join(leer_cache())
    guardar_cache(datos_limpios,"w")

#Lee el valor en cache. devuelve un string
def leer_cache():
    fich = open(cache_url, mode='r+', encoding='UTF-8')
    data =  []
    while True:
        line = fich.readline()
        if not line:
            break
        l = line.replace('\n', '')
        if l != '':
            data.append(l)
    fich.close()
    return data

#reemplazar datos ***
def reemplazar_cache(data, new_data):
    with open(cache_url, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    with open(cache_url, 'w', encoding='utf-8') as file:
        for line in lines:
            if data in line:
                file.write(line.replace(data, new_data) )
            else:
                file.write(line)
