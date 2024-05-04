from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import nltk
import plyj.parser as plyj
from nltk.tokenize import word_tokenize
import numpy as np

nltk.download('punkt')

# Función para tokenizar un archivo


def tokenizar_archivo(archivo):
    with open(archivo, 'r') as file:
        codigo = file.read()
        tokens = word_tokenize(codigo)
    return tokens


# Carpeta donde se encuentran los códigos
carpeta_codigos = ".\\conplag\\programs"

# Leer todos los códigos en la carpeta
# Usamos un diccionario para almacenar los tokens por nombre de archivo
codigos_tokenizados = {}
for filename in os.listdir(carpeta_codigos):
    filepath = os.path.join(carpeta_codigos, filename)
    if os.path.isfile(filepath):
        tokens = tokenizar_archivo(filepath)
        codigos_tokenizados[filename] = tokens

# Mostrar los tokens por nombre de archivo
# for nombre_archivo, tokens in codigos_tokenizados.items():
#     print(f"Tokens del archivo '{nombre_archivo}':\n{tokens}\n")


# Convertir todos los códigos tokenizados a texto plano para TF-IDF y Markovify
codigos_planos = [' '.join(codigo) for codigo in codigos_tokenizados.values()]

# Construir un vectorizador TF-IDF
vectorizador_tfidf = TfidfVectorizer()
tfidf_matrix = vectorizador_tfidf.fit_transform(codigos_planos)

# Función para calcular la similitud de coseno entre dos vectores de frecuencia de términos (TF-IDF)


def similitud_coseno(vector1, vector2):
    return cosine_similarity(vector1.reshape(1, -1), vector2.reshape(1, -1))[0][0]

# Función para calcular la similitud de Jaccard entre dos conjuntos de tokens


def similitud_jaccard(tokens1, tokens2):
    set1 = set(tokens1)
    set2 = set(tokens2)
    return len(set1.intersection(set2)) / len(set1.union(set2))


data = []

for nombre_archivo1, codigo_tokenizado1 in codigos_tokenizados.items():
    for nombre_archivo2, codigo_tokenizado2 in codigos_tokenizados.items():
        if nombre_archivo1 != nombre_archivo2:
            sim_jaccard = similitud_jaccard(
                codigo_tokenizado1, codigo_tokenizado2)
            if sim_jaccard >= 0.5:
                codigo_plano1 = ' '.join(codigo_tokenizado1)
                codigo_plano2 = ' '.join(codigo_tokenizado2)
                tfidf_codigo1 = vectorizador_tfidf.transform([codigo_plano1])
                tfidf_codigo2 = vectorizador_tfidf.transform([codigo_plano2])
                sim_coseno = similitud_coseno(tfidf_codigo1, tfidf_codigo2)
                # Agregar nombres de archivos a la lista data
                data.append([nombre_archivo1, nombre_archivo2,
                            sim_jaccard, sim_coseno])
                print(f"Comparando código '{
                      nombre_archivo1}' con código '{nombre_archivo2}':")
                print(f"Similitud de coseno: {round(sim_coseno, 4)}")
                print(f"Similitud de Jaccard: {round(sim_jaccard, 4)}\n")


# Función para determinar el grado de pertenencia al plagio
def grado_pertenencia(sim_jaccard, sim_coseno):
    # Establecer las reglas difusas
    if sim_jaccard >= 0.5 and sim_coseno >= 0.5:
        return "------ ALTA"
    elif (sim_jaccard >= 0.5 and sim_coseno < 0.5) or (sim_coseno >= 0.5 and sim_jaccard < 0.5):
        return "---- MEDIA"
    else:
        return None  # Retornar None si el grado de pertenencia es menor a 0.5 en alguna similitud


for nombre_archivo1, nombre_archivo2, sim_jaccard, sim_coseno in data:
    # Computar el grado de pertenencia al plagio
    pertenencia = grado_pertenencia(sim_jaccard, sim_coseno)

    # Imprimir el grado de pertenencia al plagio junto con los nombres de los archivos
    if pertenencia is not None:  # Imprimir solo si el grado de pertenencia no es None
        print(f"Comparando código '{
              nombre_archivo1}' con código '{nombre_archivo2}':")
        print("Similitud Jaccard:", round(sim_jaccard, 4))
        print("Similitud Coseno:", round(sim_coseno, 4))
        print("Grado de pertenencia al plagio:", pertenencia)

# Comprobación

# Leer el archivo jpairs.txt y almacenar los pares de archivos plagiados
pares_plagiados = set()
with open("jpairs.txt", "r") as f:
    for line in f:
        archivo1, archivo2 = line.strip().split("\t")
        pares_plagiados.add((archivo1, archivo2))

# Almacenar los pares detectados como plagiados durante la comparación
pares_detectados = set()
for nombre_archivo1, nombre_archivo2, _, _ in data:
    if nombre_archivo1 != nombre_archivo2:  # No comparar un archivo consigo mismo
        # Ordenar los nombres de archivo para evitar duplicados (por ejemplo, si se comparó A con B, no comparar B con A)
        par = (nombre_archivo1, nombre_archivo2) if nombre_archivo1 < nombre_archivo2 else (
            nombre_archivo2, nombre_archivo1)
        pares_detectados.add(par)

# Calcular el número total de pares plagiados
total_plagiados = len(pares_plagiados)

total = 0  # Inicializamos total como 0

for nombre_archivo1, nombre_archivo2, sim_jaccard, sim_coseno in data:
    # Computar el grado de pertenencia al plagio
    pertenencia = grado_pertenencia(sim_jaccard, sim_coseno)

    # Si la pertenencia es "ALTA", incrementamos total
    if pertenencia == "------ ALTA":
        total += 1
print("Pares detectados con pertenencia alta", total)
# Calcular el número de pares plagiados encontrados en la comparación
encontrados = len(pares_detectados.intersection(pares_plagiados))

# Calcular el accuracy
accuracy = encontrados / total if total > 0 else 0

print(f"Total de pares plagiados en el conjunto de datos: {total_plagiados}")
print(f"Pares plagiados encontrados durante la comparación: {encontrados}")
print(f"Accuracy: {accuracy:.2f}")
