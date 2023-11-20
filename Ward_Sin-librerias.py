#Ward sin librerias
import numpy as np
import pandas as pd
import process_text
import re
#Librerias para crear el dendograma y metodo ward
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc
from scipy.cluster.hierarchy import dendrogram, linkage, ward

#Hacer la consulta un vector de distancia steams de la matriz booleana
def vector_consulta(consulta, corpus_stems):
    import re
    import process_text
    tokens = re.split(r"[^a-z0-9]+", consulta)
    query_data = process_text.ProcessData('query', tokens)
    vector_query = []
    for stem in corpus_stems:
        if stem in query_data.stems:
            vector_query.append(1)
        else:
            vector_query.append(0)        
    return np.array(vector_query)

#Funcion para calcular la distancia euclidiana de la matriz booleana
def distancia_euclidiana(boolean_matrix):
    # Calcular la matriz de distancia utilizando la distancia euclidiana
    dist_matrix = np.zeros((len(boolean_matrix), len(boolean_matrix)))
    for i in range(len(boolean_matrix)):
        for j in range(len(boolean_matrix)):
            dist_matrix[i, j] = np.sqrt(np.sum((boolean_matrix.iloc[i, 1:] - boolean_matrix.iloc[j, 1:]) ** 2))
    return dist_matrix

#Graficamos el dendograma
def graficaresultado(boolean_matrix, dist_matrix):
    # Calcular el enlace utilizando el método de Ward
    Z = linkage(dist_matrix, method='ward')
    # Crear un dendrograma
    plt.figure(figsize=(12, 6))
    dendrogram(Z, labels=boolean_matrix.index, leaf_rotation=90)
    plt.axhline(y=100,  color='r', linestyle='--')
    plt.show

# Función para el método de Ward
def ward(dist_matrix, n):
    clusters = [[i] for i in range(n)]
    while len(clusters) > 1:
        min_dist = float('inf')
        merge_i, merge_j = -1, -1
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                avg_dist = np.mean(dist_matrix[clusters[i]][:, clusters[j]])
                if avg_dist < min_dist:
                    min_dist = avg_dist
                    merge_i, merge_j = i, j
        merged_cluster = clusters[merge_i] + clusters[merge_j]
        clusters.pop(merge_j)
        clusters[merge_i] = merged_cluster
    return clusters[0]

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
    #Calculamos la distancia euclidiana
    dist_matrix = distancia_euclidiana(boolean_matrix)
    #Graficamos el dendograma
    graficaresultado(boolean_matrix, dist_matrix)    
    # Obtener los clusters utilizando el método de Ward
    num_docs = len(boolean_matrix)
    clusters = ward(dist_matrix, num_docs)
    # Imprimir los documentos en cada cluster
    for i, cluster in enumerate(clusters):
        print(f'Cluster {i + 1}: {cluster}')
    
if __name__ == '__main__':
    main()