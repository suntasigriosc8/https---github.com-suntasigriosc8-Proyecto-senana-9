from flask import Flask, render_template
import sqlite3
DATABASE = 'database/inventario.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/usuarios/<nombre>')
def usuarios(nombre):
    return f"hola, {nombre}!"

if __name__ == '__main__':
    app.run(debug=True)