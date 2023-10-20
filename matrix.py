import pandas as pd
import numpy as np
import matplotlib as plt
import re
import process_text

#Cargar la matriz tf-idf
df = pd.read_csv('tf.csv')
N = df.shape[0] # N
stems = df.columns[1:] #Terminos EXCEPTO el nombre del documento
results = pd.DataFrame([], columns=df.columns) #Dataframe para guardar los resultados

#Funcion para determinar si un termino esta presente en un documento
def is_present(column, number=0): 
    return (column > number).sum() #Si la frecuencia es mayor a 0, entonces esta presente

n_k = df.drop(columns='name').apply(is_present) #Numero de documentos en los que aparece cada termino

id_k = np.log2(N/n_k) #Aplicamos la funcion para calcular el idf
tf_idf = df[stems].mul(id_k, axis=1) #Multiplicamos la matriz tf por el idf

#Consulta del usuario
query = 'It is our choices, Harry, that show what we truly are, far more than our abilities'
query = re.split(r"[^a-z0-9]+", query) #Tokenizamos la consulta
query = process_text.ProcessData('query', query) #Procesamos la consulta aplicando stopwords y stems
#Obtenemos un vector de la consulta
new_row = {key: [ query.frequency.get(key, 0) ] for key in df.columns[1:]} 
new_row['name'] = 'query' #Agregamos el nombre del documento
new_row = pd.DataFrame(new_row) #Convertimos el diccionario en un dataframe
new_row = new_row[stems].mul(id_k, axis=1) #Multiplicamos la matriz tf por el idf
pd.concat([tf_idf, new_row]) #Concatenamos la matriz tf-idf con el vector de la consulta