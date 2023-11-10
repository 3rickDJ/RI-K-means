import numpy as np
import pandas as pd
import process_text
import re
#Librerias para crear el dendograma y metodo ward
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc
from scipy.cluster.hierarchy import dendrogram, linkage, ward


#Funcion para hacer de nuestra consulta un vector con tamañao igual al de la matriz booleana
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

#Funcion para calcular el metodo ward
def metodo_ward(boolean_matrix: pd.DataFrame):
   cluestring=linkage(boolean_matrix,method='ward')
   dendrogram=shc.dendrogram(cluestring)
   plt.title('Dendograma')
    
#Mostrar los documentos donde esta la consulta anidada
def get_result(query_raw: str, boolean_matrix: pd.DataFrame) -> list:
    #### hacer vector query
    corpus_stems = boolean_matrix.columns[1:]
    q = vector_consulta(query_raw, corpus_stems)
    #Realizar el metodo ward
    metodo_ward(boolean_matrix)
    #Determinar los documentos donde esta la consulta anidada
    values = np.array(boolean_matrix.iloc[:,1:])


def main():
    boolean_matrix = pd.read_csv('tf.csv')
    import pudb; pudb.set_trace()
    consulta_raw = 'In 1879, Albert Einstein was born in Ulm, Germany. He completed his Ph.D. at the University of Zurich by 1909. His 1905 paper explaining the photoelectric effect, the basis of electronics, earned him the Nobel Prize in 1921. His first paper on Special Relativity Theory, also published in 1905, changed the world.'
    
    '''
    print(resultado)
    assert isinstance(resultado, list)
    assert len(resultado) > 0
    '''

if __name__ == '__main__':
    main()
