import os
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Función para preprocesar el código Java


def preprocesar_codigo(archivo):
    with open(archivo, "r", encoding="utf-8") as f:
        codigo = f.read()

    # Eliminar comentarios (// y /* */)
    codigo = re.sub(r'//.*?\n', '', codigo)
    codigo = re.sub(r'/\*.*?\*/', '', codigo, flags=re.DOTALL)

    # Eliminar saltos de línea e imports
    codigo = re.sub(r'[\n\t]', ' ', codigo)
    codigo = re.sub(r'import\s+.*?;', '', codigo)

    return codigo


# Directorio que contiene los archivos .java
directorio = ".\\conplag\\programs"

# Diccionario para almacenar el código preprocesado
codigo_preprocesado = {}

# Leer cada archivo .java en el directorio y preprocesar el código
for archivo in os.listdir(directorio):
    if archivo.endswith(".java"):
        ruta_completa = os.path.join(directorio, archivo)
        codigo = preprocesar_codigo(ruta_completa)
        codigo_preprocesado[archivo] = codigo

# Vectorizar los textos utilizando TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(codigo_preprocesado.values())

# Calcular la similitud de coseno entre cada par de archivos
similitudes = cosine_similarity(X)

# Crear matriz de similitud
n_archivos = len(codigo_preprocesado)
matriz_similitud = np.zeros((n_archivos, n_archivos))
for i, archivo1 in enumerate(codigo_preprocesado.keys()):
    for j, archivo2 in enumerate(codigo_preprocesado.keys()):
        if i < j:
            similitud = similitudes[i, j]
            matriz_similitud[i, j] = similitud
            matriz_similitud[j, i] = similitud

# Establecer los valores de la diagonal de la matriz de similitud a 1
# np.fill_diagonal(matriz_similitud, 1)

# Mostrar heatmap con resultados de comparación
# plt.figure(figsize=(42, 40))
# sns.heatmap(matriz_similitud, annot=True, xticklabels=codigo_preprocesado.keys(), yticklabels=codigo_preprocesado.keys(), cmap="YlGnBu")
# plt.title("Matriz de Similitud entre Archivos Java")
# plt.xlabel("Archivos")
# plt.ylabel("Archivos")
# plt.xticks(rotation=45, ha="right")
# plt.yticks(rotation=0)
# plt.tight_layout()
# plt.show()

# Conjunto para almacenar pares de archivos ya mostrados
mostrados = set()

# Imprimir la similitud entre cada par de archivos
for i, archivo1 in enumerate(codigo_preprocesado.keys()):
    for j, archivo2 in enumerate(codigo_preprocesado.keys()):
        if i < j:
            similitud = similitudes[i, j]
            if similitud >= 0.85 and (archivo1, archivo2) not in mostrados and (archivo2, archivo1) not in mostrados:
                print(f"Similitud de coseno entre {archivo1} y {archivo2}: {round(similitud, 2)}")
                mostrados.add((archivo1, archivo2))

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
    if par in mostrados or (par[1], par[0]) in mostrados:
        encontrados += 1

# Calcular el accuracy
# plagiados_reales = encontrados / total_plagiados if total_plagiados > 0 else 0
total = len(mostrados)
print("Pares detectados como plagio en mostrados", total)
accuracy = encontrados / total

print(f"Total de archivos en la comparación: {len(codigo_preprocesado)}")
print(f"Total de pares plagiados: {total_plagiados}")
print(f"Pares plagiados encontrados: {encontrados}")
print(f"Accuracy: {accuracy:.2f}")
