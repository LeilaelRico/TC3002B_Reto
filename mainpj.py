import os
import re
from jparser import parse


def limpiar_archivo_java(archivo):
    with open(archivo, 'r') as file:
        contenido = file.read()

    # Eliminar comentarios de una línea
    contenido = re.sub(r'//.*', '', contenido)

    # Eliminar comentarios de múltiples líneas
    contenido = re.sub(r'/\*(.|\n)*?\*/', '', contenido)

    # Eliminar líneas de importación de bibliotecas
    contenido = re.sub(r'import\s+.*?;', '', contenido)

    # Eliminar líneas en blanco adicionales
    contenido = re.sub(r'\n\s*\n', '\n', contenido)

    return contenido

def cargar_archivos_java(folder_path):
    file_contents = {}
    archivos_java = [archivo for archivo in os.listdir(folder_path) if archivo.endswith('.java')]

    for archivo in archivos_java:
        ruta_archivo = os.path.join(folder_path, archivo)
        contenido_limpio = limpiar_archivo_java(ruta_archivo)
        file_contents[archivo] = contenido_limpio

    return file_contents

# Directorio que contiene los archivos Java
folder_path = ".\\CFiles\\java\\train"
file_contents = cargar_archivos_java(folder_path)

# Mostrar el contenido de los archivos cargados
for nombre_archivo, contenido_archivo in file_contents.items():
    print(f"Archivo: {nombre_archivo}")
    print(contenido_archivo)
    print("------------------------------------")

for nombre_archivo, contenido_archivo in file_contents.items():
    ast = parse(contenido_archivo)
