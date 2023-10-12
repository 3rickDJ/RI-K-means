#Importamos la clase para realizar el scraping
from soup import scrape_web_page
#Ahora realizamos el procedimiento para el crawler
import requests
from bs4 import BeautifulSoup

#Función para obtener los enlaces de una página
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
            #Si el enlace comienza con http
            if href and href.startswith('http'):
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



#Le pedimos al usuario que ingrese el enlace inicial y el numero maximo de enlaces
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
    if data:
        corpus_data.append(data)
        
# Guardar los datos en un archivo
with open('Corpus.txt', 'w', encoding='utf-8') as f:
    for data in corpus_data:
        f.write(data + '\n\n')  # Agrega una línea en blanco entre los datos de cada página
#Imprimimos un mensaje de éxito
print("Scraping completado. Los datos han sido guardados en 'Corpus.txt'")    
