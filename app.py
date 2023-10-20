#Esta libreria nos permite el desarrollo web en Python
from flask import Flask
#Importamos la clase views
from views import views

#Determinamos la ubicacion de los archivos estaticos y plantillas
app = Flask(__name__)
#Las rutas en views estaran accesibles con el prefijo /, desde la URL
#blueprint nos permite organizar las rutas, vistas y otros aspectos
app.register_blueprint(views, url_prefix='/')
#Establecemos una clave para proteger al usuario
app.secret_key = "secret_key_stored_in_env_var"

#Verificamos si se ejecuta el script
if __name__ == '__main__':
    app.run(debug=True)

