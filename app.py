from flask import Flask, render_template, request, redirect, url_for, jsonify
from scripts.connections import connection_example, ingresar_login, obtener_componentes_caja

from cls_webdriver import WebDriverManager

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


    return render_template("login.html")

@app.route('/caja', methods=["GET","POST"])
def ingresar_caja():

    driver = WebDriverManager.get_driver()

    if driver:
        valorSelectores = obtener_componentes_caja(driver)

        if valorSelectores:
            WebDriverManager.close_driver()
            return jsonify(valorSelectores)
        else:
            return "No se encontro modal."
    else:
        WebDriverManager.close_driver()
        return "Hubo un error al obtener driver."

if __name__ == '__main__':
    app.run(port="9000",host="0.0.0.0",debug=True)