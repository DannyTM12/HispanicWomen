from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from scripts.connections import connection_example, ingresar_login, obtener_componentes_caja, validar_caja, liberar_caja

from clases.cls_webdriver import WebDriverManager

from models import Perfil
from models import db

# importar blueprints
from endpoints.auth import auth_route

app = Flask(__name__)
app.config['SECRET_KEY'] = 'proyecto_de_mierda' 

# registrar blueprints
app.register_blueprint(auth_route)

# ------------------- Base de Datos ------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# Inicializa la instancia db con la aplicación Flask
db.init_app(app)

# --------------------- Aplicacion -------------------

@app.route('/')
def root():
    return render_template("index.html")

@app.route('/prueba')
def prueba():
    return connection_example('Lamine Yamal')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # iniciamos el driver
        driver = WebDriverManager.get_driver()

        if driver:
            if ingresar_login(driver, username, password):
                return redirect(url_for('ingresar_caja'))
            else:
                WebDriverManager.close_driver()
                return "Credenciales incorrectas."
        else:
            # si no se pudo iniciar el driver
            return "Hubo un error al iniciar el driver."


    return render_template("acceso/login.html")

@app.route('/caja', methods=["GET","POST"])
def ingresar_caja():

    driver = WebDriverManager.get_driver()

    if driver:

        if request.method == "POST":
            # si se presiona submit 
            
            # obtenemos sucursal
            sucursal = request.form.get("selectorSucursal")
            # obtenemos caja
            caja = request.form.get("selectorCaja")
            # obtenemos pin
            pin = request.form.get("inputPin")

            # se obtiene un resultado y un mensaje
            respuesta = validar_caja(driver, sucursal, caja, pin)

            if respuesta["resultado"] == True:
                # driver.get("https://mujerhispana.maspunto.online/logout")
                # WebDriverManager.close_driver()
                # return respuesta["mensaje"]
                return liberar_caja(driver)
            else:
                # driver.get("https://mujerhispana.maspunto.online/logout")
                # WebDriverManager.close_driver()
                return respuesta["mensaje"]

        valorSelectores = obtener_componentes_caja(driver)

        if valorSelectores:
            return render_template("acceso/ingresar_caja.html", selectores=valorSelectores)
        else:
            WebDriverManager.close_driver()
            return "No hay opciones de caja disponibles."
    else:
        WebDriverManager.close_driver()
        return "Hubo un error al obtener driver."

if __name__ == '__main__':

    with app.app_context():
        db.create_all()
        print("Tablas de la base de datos creadas o ya existentes.")

        if not Perfil.query.first(): 
            perfil_admin = Perfil(nombre='Admin', descripcion='Administrador del sistema')
            perfil_analista = Perfil(nombre='Analista', descripcion='Interactua con dashboards y exporta extracciones')
            db.session.add_all([perfil_admin, perfil_analista])
            db.session.commit()
            print("Perfiles iniciales creados.")

    app.run(port="9000",host="0.0.0.0",debug=True)