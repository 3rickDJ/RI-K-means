import numpy as np
import pandas as pd
import process_text
import re
#Librerias para crear el dendograma y metodo ward
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster


#Hacer de la consulta un vector
def vector_consulta(consulta, corpus_stems):
    tokens = re.split(r"[^a-z0-9]+", consulta)
    query_data = process_text.ProcessData('query', tokens)
    vector_query = []
    for stem in corpus_stems:
        if stem in query_data.stems:
            vector_query.append(1)
        else:
            vector_query.append(0)
    return np.array(vector_query)

#Realizar metodo ward y dendograma
def ward(analisis_datos):
    clusterting_jerarquico = linkage(analisis_datos, 'ward')
    dendrograma = sch.dendrogram(clusterting_jerarquico)
    plt.axhline(y=27, color='r', linestyle='--')
    plt.savefig('dendrograma.jpg')  # Guardar el dendrograma como JPG
    plt.savefig('static/dendrograma.jpg')  # Guardar el dendrograma como JPG
    #plt.show()
    #Obtenemos los clusters
    clusters = fcluster(clusterting_jerarquico, t=27, criterion='distance')
    return clusters

#Funcion para obtener los documentos que pertenecen al cluster de la consulta
def documentos(boolean_matrix):
    num_cluster = boolean_matrix.iloc[-1,-1] #Obtener el numero de cluster de la consulta
    cluster_query = boolean_matrix[boolean_matrix['Clusters'] == num_cluster] #De chill
    names = cluster_query.iloc[:-1,0].values #
    return names

#Funcion para ser llamada desde SistemaDeRecuperacion.py
def get_result(query_raw: str, boolean_matrix: pd.DataFrame) -> list:
    # from pudb import set_trace; set_trace()
    #### hacer vector query
    corpus_stems = boolean_matrix.columns[1:]
    q = vector_consulta(query_raw, corpus_stems)
    #Agreagamos el vector de la consulta a la matriz booleana
    consulta_df = pd.DataFrame([q], columns=corpus_stems, index=[boolean_matrix.index.max() + 1])# Crear un DataFrame para la consulta
    consulta_df['name']='query'
    # Agregar la consulta al conjunto de documentos
    boolean_matrix = pd.concat([boolean_matrix, consulta_df])
    #Hacemos el dendograma pasando los valores de la matriz booleana
    analisis_datos = boolean_matrix.iloc[:, 1:].values
    #Clusters con el metodo ward
    clusters = ward(analisis_datos)
    #Agregamos los clusters a la matriz booleana
    boolean_matrix['Clusters'] = clusters
    #Ahora comparamos los clusters y guardamos los documentos que son iguales
    lista_documentos = documentos(boolean_matrix)
    #Imprimimos los documentos que son iguales
    return list(lista_documentos)


def main():
    boolean_matrix = pd.read_csv('tf.csv')
    consulta_raw = 'In 1879, Albert Einstein was born in Ulm, Germany. He completed his Ph.D. at the University of Zurich by 1909. His 1905 paper explaining the photoelectric effect, the basis of electronics, earned him the Nobel Prize in 1921. His first paper on Special Relativity Theory, also published in 1905, changed the world.'
    corpus_stems = boolean_matrix.columns[1:]
    #Llamamos a la funcion vector_consulta
    q = vector_consulta(consulta_raw, corpus_stems)

    #Agreagamos el vector de la consulta a la matriz booleana
    consulta_df = pd.DataFrame([q], columns=corpus_stems, index=[boolean_matrix.index.max() + 1])# Crear un DataFrame para la consulta
    consulta_df['name']='query'
    # Agregar la consulta al conjunto de documentos
    boolean_matrix = pd.concat([boolean_matrix, consulta_df])

    #Hacemos el dendograma pasando los valores de la matriz booleana
    analisis_datos = boolean_matrix.iloc[:, 1:].values
    #Clusters con el metodo ward
    clusters = ward(analisis_datos)
    #Agregamos los clusters a la matriz booleana
    boolean_matrix['Clusters'] = clusters
    #Ahora comparamos los clusters y guardamos los documentos que son iguales
    lista_documentos = documentos(boolean_matrix)
    #Imprimimos los documentos que son iguales
    print(lista_documentos)


if __name__ == '__main__':
    main()
