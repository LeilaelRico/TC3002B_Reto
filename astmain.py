import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
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

    # # Eliminar comentarios de una línea
    # contenido = re.sub(r'//.*', '', contenido)

    # # Eliminar comentarios de múltiples líneas
    # contenido = re.sub(r'/\*(.|\n)*?\*/', '', contenido)

    # Eliminar líneas de importación de bibliotecas
    contenido = re.sub(r'import\s+.*?;', '', contenido)

    # Eliminar líneas en blanco adicionales
    contenido = re.sub(r'\n\s*\n', '\n', contenido)

    return contenido


carpeta = ".\\conplag\\test"
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

# Conteo de datos totales


def contar_tipos_de_datos(ast_trees):
    tipos_de_datos = {}

    for archivo, ast_tree in ast_trees.items():
        # Recorrer el árbol sintáctico abstracto
        for _, node in ast_tree:
            # Obtener el tipo de nodo
            tipo = type(node).__name__
            # Incrementar el contador para este tipo de dato
            tipos_de_datos[tipo] = tipos_de_datos.get(tipo, 0) + 1

    return tipos_de_datos


# Obtener el conteo de tipos de datos
conteo_tipos_de_datos = contar_tipos_de_datos(ast_trees)

# Mostrar los resultados
# for tipo, conteo in conteo_tipos_de_datos.items():
#     print(f"{tipo}: {conteo}")


def contar_tipos_de_datos_por_archivo(ast_trees):
    conteo_por_archivo = {}

    for archivo, ast_tree in ast_trees.items():
        conteo_tipos_de_datos = {}
        # Recorrer el árbol sintáctico abstracto
        for _, node in ast_tree:
            # Obtener el tipo de nodo
            tipo = type(node).__name__
            # Incrementar el contador para este tipo de dato
            conteo_tipos_de_datos[tipo] = conteo_tipos_de_datos.get(
                tipo, 0) + 1

        # Guardar el conteo para este archivo
        conteo_por_archivo[archivo] = conteo_tipos_de_datos

    return conteo_por_archivo


# Obtener el conteo de tipos de datos por archivo
conteo_tipos_de_datos_por_archivo = contar_tipos_de_datos_por_archivo(
    ast_trees)

# Mostrar los resultados
# for archivo, conteo_tipos in conteo_tipos_de_datos_por_archivo.items():
#     print(f"Archivo: {archivo}")
#     for tipo, conteo in conteo_tipos.items():
#         print(f"\t{tipo}: {conteo}")


# Obtener las claves únicas de los tipos de datos
tipos_de_datos_unicos = set()
for conteo_tipos in conteo_tipos_de_datos_por_archivo.values():
    tipos_de_datos_unicos.update(conteo_tipos.keys())

# Ordenar los tipos de datos únicos alfabéticamente
tipos_de_datos_unicos = sorted(tipos_de_datos_unicos)

# Crear una matriz para almacenar los conteos
matriz_conteos = np.zeros(
    (len(conteo_tipos_de_datos_por_archivo), len(tipos_de_datos_unicos)), dtype=int)

# Llenar la matriz con los conteos
for i, (archivo, conteo_tipos) in enumerate(conteo_tipos_de_datos_por_archivo.items()):
    for j, tipo_dato in enumerate(tipos_de_datos_unicos):
        matriz_conteos[i, j] = conteo_tipos.get(tipo_dato, 0)

# Mostrar la matriz
# print("Matriz de conteos:")
# print(matriz_conteos)


# Obtener las claves únicas de los tipos de datos
tipos_de_datos_unicos = set()
for conteo_tipos in conteo_tipos_de_datos_por_archivo.values():
    tipos_de_datos_unicos.update(conteo_tipos.keys())

# Ordenar los tipos de datos únicos alfabéticamente
tipos_de_datos_unicos = sorted(tipos_de_datos_unicos)

# Crear una matriz para almacenar los conteos
matriz_conteos = np.zeros(
    (len(conteo_tipos_de_datos_por_archivo), len(tipos_de_datos_unicos)), dtype=int)

# Llenar la matriz con los conteos
for i, (archivo, conteo_tipos) in enumerate(conteo_tipos_de_datos_por_archivo.items()):
    for j, tipo_dato in enumerate(tipos_de_datos_unicos):
        matriz_conteos[i, j] = conteo_tipos.get(tipo_dato, 0)

# Para la normalización, se consideró hacerlo de 2 formas:

# Normalización por filas
matriz_normalizada_filas = matriz_conteos / \
    matriz_conteos.sum(axis=1, keepdims=True)

# Normalización por columnas
matriz_normalizada_columnas = matriz_conteos / \
    matriz_conteos.sum(axis=0, keepdims=True)

# Mostrar la matriz normalizada por filas
# print("Matriz normalizada por filas:")
# print(matriz_normalizada_filas)

# Mostrar la matriz normalizada por columnas
# print("\nMatriz normalizada por columnas:")
# print(matriz_normalizada_columnas)


#  Calcular la similitud de cosenos entre las filas de la matriz de conteos
similitud_cos = cosine_similarity(matriz_normalizada_columnas)

#  Mostrar la matriz de similitud de cosenos
# print("Matriz de similitud de cosenos:")
# print(similitud_cos)


# Obtener los nombres de los archivos
nombres_archivos = list(conteo_tipos_de_datos_por_archivo.keys())

# Crear un DataFrame con la matriz de similitud de cosenos
df_similitud_cos = pd.DataFrame(
    similitud_cos, index=nombres_archivos, columns=nombres_archivos)

# Mostrar el DataFrame
print("Matriz de similitud de cosenos:")
print(df_similitud_cos)

# Definir el umbral de similitud
umbral_similitud = 0.97

# Filtrar los pares de archivos con similitud mayor o igual al umbral
pares_similitud_alta = df_similitud_cos[df_similitud_cos >= umbral_similitud].stack(
).reset_index()
pares_similitud_alta.columns = ['Archivo 1', 'Archivo 2', 'Similitud']

# Filtrar los pares de archivos que no son el mismo archivo
pares_similitud_alta = pares_similitud_alta[pares_similitud_alta['Archivo 1']
                                            != pares_similitud_alta['Archivo 2']]

# Mostrar los pares de archivos con similitud alta
print("Archivos similares:")
# Conjunto para almacenar los pares de archivos ya mostrados
archivos_mostrados = set()
for _, row in pares_similitud_alta.iterrows():
    archivo1 = row['Archivo 1']
    archivo2 = row['Archivo 2']
    similitud = row['Similitud']
    # Verificar si el par de archivos ya ha sido mostrado
    if (archivo1, archivo2) not in archivos_mostrados and (archivo2, archivo1) not in archivos_mostrados:
        print(f"{archivo1} - {archivo2}: Similitud = {round(similitud, 4)}")
        archivos_mostrados.add((archivo1, archivo2))

# Comprobación

# Leer el archivo jpairs.txt y almacenar los pares de archivos plagiados
pares_plagiados = set()
with open("jpairs.txt", "r") as f:
    for line in f:
        archivo1, archivo2 = line.strip().split("\t")
        pares_plagiados.add((archivo1, archivo2))

archivos_unicos = set()
for par in pares_plagiados:
    archivos_unicos.add(par[0])
    archivos_unicos.add(par[1])
total_archivos = len(archivos_unicos)

# Calcular el número total de pares plagiados
total_plagiados = len(pares_plagiados)

# Calcular el número de pares plagiados encontrados en la comparación
encontrados = 0
for par in pares_plagiados:
    if par in archivos_mostrados or (par[1], par[0]) in archivos_mostrados:
        encontrados += 1

# Calcular el accuracy
# plagiados_reales = encontrados / total_plagiados if total_plagiados > 0 else 0
total = len(archivos_mostrados)
print("Pares detectados como plagio en mostrados", total)
accuracy = encontrados / total

print(f"Total de archivos en la comparación: {len(nombres_archivos)}")
print(f"Total de pares plagiados: {total_plagiados}")
print(f"Pares plagiados encontrados: {encontrados}")
print(f"Accuracy: {accuracy:.2f}")
