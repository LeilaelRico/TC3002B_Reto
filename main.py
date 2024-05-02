from scipy.spatial.distance import cosine
import numpy as np
import os
import re
import javalang


def limpiar_archivo_java(archivo):
    with open(archivo, 'r') as file:
        contenido = file.read()

    # Eliminar sangría y saltos de línea
    contenido = re.sub(r'\n\s*', '\n', contenido)

    # Eliminar comentarios de una línea
    contenido = re.sub(r'//.*', '', contenido)

    # Eliminar comentarios de múltiples líneas
    contenido = re.sub(r'/\*(.|\n)*?\*/', '', contenido)

    # Eliminar líneas de importación de bibliotecas
    contenido = re.sub(r'import\s+.*?;', '', contenido)

    # Eliminar líneas en blanco adicionales
    contenido = re.sub(r'\n\s*\n', '\n', contenido)

    return contenido


carpeta = ".\\CFiles\\java\\train"
archivos_java = [archivo for archivo in os.listdir(
    carpeta) if archivo.endswith('.java')]

ast_trees = {}

for archivo in archivos_java:
    ruta_archivo = os.path.join(carpeta, archivo)
    contenido_limpio = limpiar_archivo_java(ruta_archivo)
    tokens = javalang.tokenizer.tokenize(contenido_limpio)

    try:
        parser = javalang.parser.Parser(tokens)
        ast_tree = parser.parse_member_declaration()
        # Guardar el AST en un diccionario con el nombre del archivo como clave
        ast_trees[archivo] = ast_tree
    except javalang.parser.JavaSyntaxError as e:
        print("Error de sintaxis en", archivo, ":", e)