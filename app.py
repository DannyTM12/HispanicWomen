from flask import Flask, render_template, request, redirect, url_for
from scripts.connections import iniciar_driver, connection_example, ingresar_login, obtener_componentes_caja
app = Flask(__name__)

# webdriver de la aplicacion
app_driver = None

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
        app_driver, mensajes = iniciar_driver()

        if app_driver:
            if ingresar_login(username,password):
                return redirect(url_for('ingresar_caja'))
            else:
                app_driver.quit()
                return "Credenciales incorrectas."
        else:
            # si no se pudo iniciar el driver
            return mensajes


    return render_template("login.html")

@app.route('/caja', methods=["GET","POST"])
def ingresar_caja():



    return "ingresar caja"

if __name__ == '__main__':
    app.run(port="9000",host="0.0.0.0",debug=True)