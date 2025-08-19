from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/usuarios/<nombre>')
def usuarios(nombre):
    return f"hola, {nombre}!"

if __name__ == '__main__':
    app.run(debug=True)
