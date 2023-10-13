#Importamos la clase para realizar el scraping
import json
from soup import scrape_web_page
#Ahora realizamos el procedimiento para el crawler
import requests
from bs4 import BeautifulSoup
#Libreria para admninistrar expresiones regulares


def is_valid_link(href):
    # Lista de extensiones de archivo que queremos evitar
    invalid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.zip', '.rar', '.rst', '.tar', '.gz', '.whl', '.md']
    for ext in invalid_extensions:
        if href.endswith(ext):
            return False
    return True

def get_links(url, max_depth, depth=1):
    if depth > max_depth:
        return []
    #Obtenemos el contenido de la página
    response = requests.get(url)  
    #Si el código de estado es 200, es decir, si se pudo acceder a la página
    if response.status_code == 200:
        #Creamos el objeto soup
        soup = BeautifulSoup(response.content, 'html.parser')
        #Obtenemos todos los enlaces de la página
        links = soup.find_all('a')
        #Creamos una lista vacía para guardar los enlaces
        links_list = []
        #Recorremos los enlaces
        for link in links:
            #Obtenemos el atributo href de cada enlace
            href = link.get('href')
            #Si el enlace comienza con http y es válido, lo agregamos a la lista
            if href and href.startswith('http') and is_valid_link(href):
                #Si el enlace no está en la lista de enlaces
                if href not in links_list:
                    #Agregamos el enlace a la lista
                    links_list.append(href)
                    #Hacemos que la función se llame a sí misma y agregamos los enlaces que retorne a la lista
                    depth += 1
                    links_list.extend(get_links(href, max_depth, depth+1))
        #Retornamos la lista de enlaces
        return links_list
    #Si no se pudo acceder a la página
    else:
        #Retornamos 
        return []

#Le pedimos al usuario que ingrese el enlace inici  al y el numero maximo de enlaces
url = input("Ingrese el enlace inicial: ")
max_depth = int(input("Ingrese el número máximo de enlaces: "))
#Llamamos a la función get_links para obtener los enlaces
links = get_links(url,max_depth)

#Lista para almacenar los datos
corpus_data = []
#Con los links ahora se puede hacer scraping a cada uno de ellos
for link in links:
    print(f"Scrapeando: {link}")
    data = scrape_web_page(link)
    dic = {'url': link, 'data': data}	
    if link not in corpus_data:
        corpus_data.append(dic)
        
# Guardar los datos en un archivo JSON
#Contador para nombrar los archivos
contador = 0
#Recorremos la lista de datos
for data in corpus_data:
    with open(str(contador)+".json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    contador += 1

#Creamos una lista para almacenar el texto de cada página
corpus = list()
for data in corpus_data:
    corpus.append(data['data'])

#Guardamos todos los datos en un archivo txt
with open('Corpus.txt', 'w', encoding='utf-8') as f:
    for data in corpus:
        if data != None:
            f.write(data + '\n\n')

print("Scraping completado. Los datos han sido guardados en 'Corpus.txt'")    