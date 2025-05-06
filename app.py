from flask import Flask, render_template, request
from scripts.connections import connection_example, connection_login

app = Flask(__name__)

@app.route('/')
def root():
    return 'Bien!'

@app.route('/prueba')
def prueba():
    return connection_example('Lamine Yamal')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        return connection_login(username,password)

    return render_template("login.html")

if __name__ == '__main__':
    app.run(port="9000",host="0.0.0.0",debug=True)