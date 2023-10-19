#Librerias necesarias para el funcionamiento del programa
import process_text #Clase de procesamiento de texto para los stems, stopwords y tokens
import json #Libreria para el manejo de archivos json
import pandas as pd #Libreria para el manejo de datos
import re #Libreria para expresiones regulares
import math #Libreria para operaciones matematicas
import subprocess #Libreria para ejecutar comandos en la terminal
from collections import Counter #Libreria para contar elementos de una lista

#Funcion para cargar los datos generados por quote_spider.py
def load_data():
    with open('quotes.json') as f:
        data = json.load(f)

    corpus = []
    for i in data:
        process_data = process_text.ProcessData(i['url'], i['content'])
        corpus.append(process_data)
    return corpus
#Funcion para guardar los tokens del corpus
def save_corpus_tokens(corpus):
    corpus_tokens = [d.tokens for d in corpus] #Lista de tokens de cada documento
    flat_tokens = set([ token for tokens in corpus_tokens for token in tokens ]) #Lista de tokens sin repetir
    with open('corpus_tokens.txt', 'w') as f:
            f.write(' '.join(flat_tokens))
    return flat_tokens
#Funcion para guardar las stopwords del corpus
def save_corpus_terms(corpus, flat_tokens):
    corpus_terms = [d.terms for d in corpus]
    terms = set([ term for terms in corpus_terms for term in terms ])
    with open('corpus_terms.txt', 'w') as f:
            f.write(' '.join(terms))
    return terms
#Funcion para guardar los stems del corpus
def save_corpus_stems(corpus, flat_tokens):
    corpus_stems = [d.stems for d in corpus]
    stems = list(set([ stem for stems in corpus_stems for stem in stems ]))
    with open('corpus_stems.txt', 'w') as f:
            f.write(' '.join(stems))
    return stems


# Función para calcular la matriz de frecuencia de términos (TF)
def calculate_tf(corpus, stems_corpus):
    tf_matrix = []
    for d in corpus:
        term_freq = Counter(d.stems)
        row = [term_freq.get(s, 0) for s in stems_corpus]
        tf_matrix.append(row)
    return tf_matrix

#Funcion para realizar la matriz tf-idf y guardar la matriz 
def save_matrix_tf_idf(tf_matrix, stems_corpus):
    tf_df = pd.DataFrame(tf_matrix, columns=stems_corpus)
    N = len(tf_matrix)  # Número de documentos
    # Calcular IDF
    idf = tf_df.astype(bool).sum(axis=0).apply(lambda x: math.log(N / (1 + x)))
    # Calcular TF-IDF
    tf_idf = tf_df * idf.values
    return tf_idf, idf


#Convertimos nuestra consulta en un vector
def convert_query_to_vector(query, stems_corpus, idf):
    row = dict()
    for s in query.stems:
        if s in stems_corpus:
            row[s] = 1

    row = pd.DataFrame([row], columns=stems_corpus).fillna(0).apply(lambda x: x * idf, axis = 1)
    return row
#Prueba para ejecutar el programa de crawler en la funcion main
def Process_Script():
    try:
        # Llama al comando utilizando subprocess
        subprocess.run(["scrapy", "crawl", "quotes", "-O", "quotes.json"], check=True)
        print("Scraper ejecutado exitosamente.")
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar el scraper:", e)

#Funcion principal
def main():
    #Llamamos al proceso
    Process_Script()
    corpus = load_data() #Cargamos los datos
    tokens = save_corpus_tokens(corpus) #Guardamos los tokens
    terms = save_corpus_terms(corpus, tokens) #Guardamos los stopwords
    stems = save_corpus_stems(corpus, tokens) #Guardamos los stems
    
    #Esta matriz sirve para contar las veces que aparece cada termino en cada documento
    matrix = calculate_tf(corpus, stems) 
    #Matriz tf-idf
    tf_idf, idf = save_matrix_tf_idf(matrix, stems) 
    
    #Guardamos la matriz tf-idf en un archivo csv
    tf_idf.to_csv('tf_idf.csv', index=False)
    print(tf_idf)
    
    k = 3   #Numero de clusters
    query = "I have not failed. I've just found 10,000 ways that won't work.".lower().strip()
    query = re.split(r"[^a-z0-9]+", query) 
    # import dbg
    #import pudb; pudb.set_trace()
    query = process_text.ProcessData('query', query) #Procesamos la consulta aplicando stopwords y stems
    query_vector = convert_query_to_vector(query, stems, idf) #Obtenemos un vector de la consulta
    tf_idf_query = pd.concat([tf_idf, query_vector], ignore_index=True) #Concatenamos la matriz tf-idf con el vector de la consulta
    #Sobreescribimos la matriz tf-idf en un archivo csv
    tf_idf_query.to_csv('tf_idf.csv', index=False)
    print(tf_idf_query)

    print("🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥")

if __name__ == "__main__":
    main() 