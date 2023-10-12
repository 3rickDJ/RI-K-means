from bs4 import BeautifulSoup
# html_doc = None
with open('pagina.html', 'r') as f:
    html_doc = f.read()
soup = BeautifulSoup(html_doc, 'html.parser')
print(soup.prettify())
print("-"*80)
pagina_txt = soup.get_text()
pagina_txt = '\n'.join([ll.rstrip() for ll in pagina_txt.splitlines() if ll.strip()])
with open('pagina.txt', 'w') as f:
    f.write(pagina_txt)
