from flask import Flask, render_template, request, redirect, url_for
from inventario import Inventario, Producto
import sqlite3
DATABASE = 'database/inventario.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
inv = Inventario()

@app.route("/")
def index():
    return redirect(url_for('productos'))

@app.route("/productos")
def productos():
    items = inv.mostrar_todos()
    return render_template("productos.html", productos=items)

@app.route("/about")
def about():
    return render_template("about.html")

# API simple para agregar producto desde formulario (si se desea)
@app.route("/productos/agregar", methods=["POST"])
def agregar_producto():
    data = request.form
    try:
        producto = Producto(int(data["id"]), data["nombre"], int(data["cantidad"]), float(data["precio"]))
    except Exception:
        return "Datos inválidos", 400
    ok = inv.agregar_producto(producto)
    return redirect(url_for('productos'))

if __name__ == "__main__":
    app.run(debug=True)