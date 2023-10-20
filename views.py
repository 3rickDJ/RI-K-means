#Blueprint para organizar las rutas, render.. para renderizar plantillas HTML, request para solicitudes de clientes, redirect para redirigir al cliente con URL,
#url_for genera URLs sin actualizarlas manualmente en el codigo, session almacena informacion de usuario de una solicitud a otra (cookies)
from flask import Blueprint, render_template, request, redirect, url_for, session
from matrix import SistemaDeRecuperacion
views = Blueprint('views', __name__)
# Instancia del modelo
model = SistemaDeRecuperacion()

@views.route('/')
#Si el usuario visita la URL principal entonces
def index():
    #Verificamos si la ruta esta presente en la sesion
    if 'path' in session:
        path = session['path']
    #Si no esta entonces no se le asigna
    else:
        path = None
    if 'k' in session:
        k = session['k']
    else:
        k = None
    #Si el contenido esta almacenada en la sesion
    if 'result' in session:
        result = session['result']
    #Si no entonces no se asigna
    else:
        result = None
    #Renderizamos la plantilla index.html con su ruta y contenido
    return render_template('index.html', path=path, result=result, k=k)

# Si el usuario quiere cambiar de directorio entonces accedemos a la funcion
#@views.route('/load_corpus', methods=['POST'])
#def manage_request():
#    #Obtenemos el valor de la direccion que dio el usuario
#    path = request.form['path']
#    #Construimos la ruta completa concatenando el valor del 'path' con el prefijo 'static/'
#    complete_path = 'static/' + path
#    #Cargamos el corpus utilizando el metodo 'load_corpus'
#    model.load_corpus(complete_path)
#    #Alamcenamos el valor del camino en la sesion, para recordar la ultima ruta cargada por el usuario
#    session['path'] = path
#    #Redirigimos a el usuario a lña pagina principal despues de cargar con el corpus actualizado
#    return redirect(url_for('views.index'))

#Ahora cuando el usuario quiera realizar una busqueda en los corpus (es decir una consulta)
@views.route('/search', methods=['POST'])
def search():
    #Obtenemos el valor de la consulta
    query = request.form['query']
    k = request.form['k']
    #Con el metodo query de BooleanModel realizamos la busqueda en el corpus y lo guardamos en result
    result = model.query(query, int(k))
    #Almacenamos el resultado de la busqueda en la sesion
    session['result'] = result
    #Redirigmos al usuario con los resultados de la busqueda puesta por el usuario
    return redirect(url_for('views.index'))
