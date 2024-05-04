# TC3002B_Reto

Desarrollo de aplicaciones avanzadas de ciencias computacionales (Gpo 201)  
Cristian Leilael Rico Espinosa A01707023    
Fabián Enrique Avilés Cortés A01367678

## Contexto
Herramientas para detectar infracciones a los derechos de autor. Con el internet, la copia y distribución global de medios digitales nos lleva a mejorar la forma en la que protegemos los derechos de autor. El desafío consiste en desarrollar herramientas computacionales que detecten infracciones de derechos de autor en varios archivos de código en “C” y “Java”. Para nuestro caso en particular enfocamos las soluciones a unicamente archivos de código en "Java".

### Dataset
El dataset utilizado es el propocionado por [ConPlag](https://zenodo.org/records/7332491#.ZG4rDNLMKXL). 

## Solución 1 Comparación de similitud con AST
Este código carga archivos Java, los procesa para eliminar información no relevante, calcula la similitud entre ellos utilizando medidas como TF-IDF y similitud de cosenos, y finalmente presenta los resultados, incluidas las similitudes detectadas y un análisis estadístico de los tipos de datos utilizados en los archivos. Funciona de la siguiente manera:

1. Importación de Librerías: El codigo hace uso de las librerias `os`, `re`, `numpy`, `javalang`, `sklearn` y `pandas`.

2. Lectura de Archivos en Dataset: La función `limpiar_archivo_java(archivo)`, toma una carpeta con todos los archivos .java añadidos, para hacer el preprocesado de los archivos, en esta parte se eliminan los `imports` y `lineas en blanco`.

3. Generación de AST: El contenido de los archivos limpios se tokeniza con `javalang.tokenizer`, para despues hacer un parseo de los archivos con la función `javalang.parser`, con esto se generan los AST con la función `parser.parser_member_declaration`.

4. Conteo de tipos de datos totales en AST: Con la función `contar_tipos_de_datos(ast_trees)`, se recorren los nodos del arbol y genera cuantas veces ese tipo de nodo esta presente por archivo.

5. Conteo de tipos de datos por archivo: Tomando como entrada el conteo de tipos de datos en los AST, se genera un conteo por archivo con la función `contar_tipos_de_datos_por_archivo(ast_trees)`, lo cual nos regresa lo siguiente para cada archivo:
```Archivo: ca0c55ad.java
	ClassDeclaration: 1
	MethodDeclaration: 1
	FormalParameter: 1
	ReferenceType: 3
	LocalVariableDeclaration: 8
	VariableDeclarator: 13
	ClassCreator: 1
	MemberReference: 73
	BasicType: 14
	MethodInvocation: 5
	ForStatement: 5
	ForControl: 5
	VariableDeclaration: 5
	Literal: 21
	BinaryOperation: 23
	BlockStatement: 7
	ArrayCreator: 2
	StatementExpression: 13
	Assignment: 14
	ArraySelector: 21
	IfStatement: 2
```

6. Generación de matrices de conteo: Estos datos los agregamos a una matriz por archivo unico que almacena los conteos por cada tipo. Esto se ve de la siguiente manera:
 ```[[ 0  2  0 ...  5 13  0]
 [ 0  1  0 ...  2 14  1]
 [ 0  0  0 ...  2 14  0]
 ```
Seguido de se normaliza el contenido de las matrices de conteo, para poder llevar a cabo un analisis de similitud mas preciso.

7. Similitud de Coseno: Con las matrices de conteo normalizadas se hace un calculo de similitud entre los vectores en la matris, para posteriormente establecer un umbral de `.97`, para guardar esos archivos como plagiados.
8. Resultados Finales de la solución con AST: Con los archivos guardados como plagio se carga una lista que contiene todos los archivos que son verdaderamente plagiados, para así verificar cuales fueron verdaderos positivos y cuales fueron falsos negativos, con esto se encontro lo siguiente:
```Pares detectados como plagio en mostrados 10
Total de archivos en la comparación: 62
Total de pares plagiados verdaeros: 251
Pares plagiados encontrados verdaderos: 5
Accuracy: 0.50
```
## Solución 2 Comparación de similitud coomparando los archivos convirtiendolos a texto
Esta solución realiza un análisis de similitud entre archivos Java para detectar posibles casos de plagio, utilizando TF-IDF y similitud de coseno como métricas, y luego evalúa la efectividad del análisis comparando los resultados con casos de plagio conocidos.

1. Importaciones de librerias: Para el uso adecuado de esta solución se hace uso de `os`, `re`, `numpy`, `matplot`, `seaborn` y `sklearn`.
2. Preprocesamiento del codigo: La función `preprocesar_codigo(archivo)` toma la carpeta con todos los archivos .java añadidos, para hacer una limpieza de los archivos, en esta parte se eliminan los `comentarios`, `lineas en blanco` e `imports`.
3. Diccionario de codigo preprocesado: Guardado de los codigos ya limpiados y los almacena en un diccionario en formato de texto plano.
4. Vectorización de textos con TF-IDF: Se convierte el texto preprocesado en una matriz TF-IDF, que representa la importancia de cada palabra en cada documento en función de su frecuencia en el archivo.
5. Cálculo de similitud coseno: Calcula la similitud de coseno entre cada par de archivos basada en la matriz TF-IDF.
6. Creación de la matriz de similitud: Crea una matriz cuadrada que almacena las similitudes calculadas entre cada par de archivos.
7. Visualización del heatmap: Utiliza matplotlib y seaborn para visualizar la matriz de similitud como un heatmap, lo que proporciona una representación visual de las similitudes entre los archivos.
8. Guardado de similitudes significativas: Guarda en `mostrados` las similitudes de coseno entre cada par de archivos que tienen una similitud mayor o igual a 0.85.
9. Resultados Finales: Con los archivos guardados como plagio se carga una lista que contiene todos los archivos que son verdaderamente plagiados, para así verificar cuales fueron verdaderos positivos y cuales fueron falsos negativos, con esto se encontro lo siguiente:
```
Total de archivos en la comparación: 340
Total de pares plagiados verdaderos: 251
Pares plagiados encontrados verdaderos: 18
Accuracy: 0.90
```
## Solución 3 Comparación de similitud y definiendo pertenencia con Fuzzy Logic
Esta solución realiza la comparación de archivos de código fuente para detectar posibles casos de plagio utilizando técnicas de similitud de texto y reglas difusas.

1. Importaciones de librerias: Se importan los módulos necesarios para el análisis, siendo estos `os`, `nltk`, `numpy`, `TfidfVectorizer` y `sklearn`.
2. Lectura de archivos: Lee todos los archivos .java encontrados en una carpeta específica para hacer la tokenización de los archivos.
3. Tokenización del código: Define una función `tokenizar_archivo` para tokenizar un archivo de código fuente.
4. Vectorización TF-IDF: Convierte los archivos tokenizados en texto plano y construye un vectorizador TF-IDF para calcular la similitud entre los archivos.
5. Cálculo de similitud: Utiliza las funciones `similitud_coseno` y `similitud_jaccard` para calcular la similitud entre los archivos.
6. Determinación del grado de pertenencia al plagio: Define una función `grado_pertenencia` que determina el grado de pertenencia al plagio basado en ciertas reglas difusas.
7. Comparación de archivos y detección de plagio: Compara todos los pares de archivos y calcula la similitud entre ellos. Luego, determina si hay una alta similitud y, por lo tanto, un posible caso de plagio.
8. Resultados Finales: Con los archivos etiquetados como pertenencia al plagio ALTA se carga una lista que contiene todos los archivos que son verdaderamente plagiados, para así verificar cuales fueron verdaderos positivos y cuales fueron falsos negativos, con esto se encontro lo siguiente:

Pares detectados con pertenencia alta: 36
Total de pares plagiados verdaderos: 251
Pares plagiados encontrados verdaderos: 13
Accuracy: 0.36
