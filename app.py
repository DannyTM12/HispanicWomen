from flask import Flask, render_template, request
from scripts.connections import connection_example, ingresar_login
app = Flask(__name__)

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

        credencialesValidas,driver = ingresar_login(username,password)

        if credencialesValidas:
            driver.quit()
            return "Sesion iniciada con exito!"
        else:
            return "Credenciales incorrectas."


    return render_template("login.html")

if __name__ == '__main__':
    app.run(port="9000",host="0.0.0.0",debug=True)