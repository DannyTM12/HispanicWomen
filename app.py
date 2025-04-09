from flask import Flask
from example import connection_example

app = Flask(__name__)

@app.route('/')
def root():
    return 'Bien!'

@app.route('/prueba')
def prueba():
    return connection_example('Lamine Yamal')

if __name__ == '__main__':
    app.run(port="9000",host="0.0.0.0",debug=True)