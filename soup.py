from bs4 import BeautifulSoup
import re
# html_doc = None
with open('pagina.html', 'r') as f:
    html_doc = f.read()
soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup.prettify())
print("-"*80)
# title, desc = soup.head.title.get_text(), soup.head.meta.get('charset')
pagina_txt = soup.body.get_text()
pagina_txt = re.sub(r'[^a-zA-Z0-9]+', ' ', pagina_txt)
# pagina_txt = '\n'.join([ll.rstrip() for ll in pagina_txt.splitlines() if ll.strip()])
with open('pagina2.txt', 'w') as f:
    f.write(pagina_txt)
