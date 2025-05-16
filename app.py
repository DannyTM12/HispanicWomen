from flask import Flask, render_template, request, redirect, url_for, jsonify
from scripts.connections import connection_example, ingresar_login, obtener_componentes_caja, validar_caja

from clases.cls_webdriver import WebDriverManager

app = Flask(__name__)

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

            return validar_caja(driver, sucursal, caja, pin)

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
    app.run(port="9000",host="0.0.0.0",debug=True)