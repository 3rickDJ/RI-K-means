import pandas as pd
import numpy as np


def getresult():
    full_table = pd.read_csv('query_matrix.csv', index_col=0)
    v_table = np.array(full_table.iloc[:,1:])
    v_query = v_table[-1]
    #Calcular las distancias
    dot_prod = np.dot(v_table, v_query)

    # scalar product between a vector and a list of vectors
    v_query_norm = np.linalg.norm(v_query)
    v_table_norm = np.linalg.norm(v_table, axis=1)
    v_prod_norm = v_query_norm * v_table_norm

    #coeficient dot prod over norm prod
    coeficient = (dot_prod / v_prod_norm)
    # arcosine of coeficient
    angle = np.arccos(coeficient)
    
    full_table['angle'] = angle
    sorted = full_table.sort_values(by=['angle'], ascending=True)
    return list(sorted['name'])[1:-1]