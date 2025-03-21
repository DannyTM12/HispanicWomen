from flask import Flask

app = Flask(__name__)

@app.route('/')
def root():
    return 'Bien!'

if __name__ == '__main__':
    app.run(port="9000",host="0.0.0.0",debug=True)