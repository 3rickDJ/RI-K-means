import pandas as pd
import numpy as np
import process_text
import re

def get_pj_qj(boolean_matrix: pd.DataFrame)-> tuple:
    row_size = boolean_matrix.shape[1]
    pj = np.full((row_size), 0.5)
    qj = np.array(boolean_matrix.sum(axis=0) / row_size)
    return pj, qj

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

def get_sem_table(consulta_vector, boolean_matrix):
    q = consulta_vector
    pj, qj = get_pj_qj(boolean_matrix)
    semejanza = ( (q * boolean_matrix) *  np.log10((  pj*(1-qj)  )/ (  qj*(1-pj)  )) ).sum(axis=1)
    return semejanza


def get_result(query_raw: str, boolean_matrix: pd.DataFrame) -> list:
    #### hacer vector query
    corpus_stems = boolean_matrix.columns[1:]
    q = vector_consulta(query_raw, corpus_stems)
    #### calcular semejanza
    values = np.array(boolean_matrix.iloc[:,1:])
    semejanza_lista = get_sem_table(q, values)
    #### ordenar nombre y valores
    resultado = boolean_matrix[['name']].copy()
    resultado['semejanza'] = semejanza_lista
    ordenados = resultado.sort_values(by=['semejanza'], ascending=False)
    return list(ordenados['name'])


def main():
    boolean_matrix = pd.read_csv('tf.csv')
    import pudb; pudb.set_trace()
    consulta_raw = 'In 1879, Albert Einstein was born in Ulm, Germany. He completed his Ph.D. at the University of Zurich by 1909. His 1905 paper explaining the photoelectric effect, the basis of electronics, earned him the Nobel Prize in 1921. His first paper on Special Relativity Theory, also published in 1905, changed the world.'
    # consulta_raw2 = "The Wizard of Menlo Park (now Edison, New Jersey) by a newspaper reporter"
    resultado = get_result( consulta_raw, boolean_matrix )
    print(resultado)
    assert isinstance(resultado, list)
    assert len(resultado) > 0

if __name__ == '__main__':
    main()
