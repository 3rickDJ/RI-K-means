import requests
from bs4 import BeautifulSoup
import re
#Funcion para realizar el scraping, pasandole como parametro la url
def scrape_web_page(url):
    #Obtenemos el contenido de la página
    response = requests.get(url)
    #Si el código de estado es 200, es decir, si se pudo acceder a la página
    if response.status_code == 200:
        #Creamos el objeto soup con el contenido de la página
        soup = BeautifulSoup(response.content, 'html.parser')
        #Obtenemos el texto de la página
        pagina_txt = soup.body.get_text()
        #Eliminamos los saltos de línea y los espacios en blanco al inicio y al final
        pagina_txt = re.sub(r'[^a-zA-Z0-9]+', ' ', pagina_txt)
        #Retornamos el texto de la página
        return pagina_txt
    else:
        #Si no se pudo acceder a la página, retornamos None
        return None
