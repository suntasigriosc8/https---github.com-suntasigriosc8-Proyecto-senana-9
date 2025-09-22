import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import mysql.connector
from forms import ProductoForm
from inventario import Inventario, Producto
from conexion.conexion import obtener_conexion
from models import cargar_usuario_por_id, cargar_usuario_por_email, Usuario
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['SECRET_KEY'] = "mi_clave_secreta"

# Inicializar Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return cargar_usuario_por_id(user_id)

# Inicializar inventario
try:
    inv = Inventario()
except Exception:
    app.logger.exception("Error inicializando Inventario (revisa inventario.py / inventario.db):")
    inv = None

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

@app.route('/')
def index():
    return render_template('index.html', title="Inicio")

# --- CRUD de productos ---
@app.route('/productos', methods=['GET', 'POST'])
def listar_productos():
    q = request.args.get('q', '').strip()
    productos = inv.buscar_por_nombre(q) if q and inv else (inv.mostrar_todos() if inv else [])
    return render_template('productos/index.html', title="Productos", productos=productos, q=q)

@app.route('/productos/agregar', methods=['GET', 'POST'])
@login_required
def agregar_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        cantidad = form.cantidad.data
        precio = float(form.precio.data)
        producto = Producto(id=None, nombre=nombre, cantidad=cantidad, precio=precio)
        ok = inv.agregar_producto(producto) if inv else False
        flash('Producto agregado.' if ok else 'Error al agregar producto.', 'success' if ok else 'danger')
        return redirect(url_for('listar_productos'))
    return render_template('productos/agregar_producto.html', title="Agregar Producto", form=form)

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    if not inv:
        flash('Inventario no disponible.', 'danger')
        return redirect(url_for('listar_productos'))
    producto = inv.obtener(id)
    if not producto:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('listar_productos'))
    form = ProductoForm()
    if request.method == 'GET':
        form.nombre.data = producto.nombre
        form.cantidad.data = producto.cantidad
        form.precio.data = producto.precio
    if form.validate_on_submit():
        inv.actualizar_producto(id, nombre=form.nombre.data, cantidad=form.cantidad.data, precio=float(form.precio.data))
        flash('Producto actualizado.', 'success')
        return redirect(url_for('listar_productos'))
    return render_template('productos/editar_producto.html', title="Editar Producto", form=form, producto=producto)

@app.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    ok = inv.eliminar_producto(id) if inv else False
    flash('Producto eliminado.' if ok else 'No se encontró el producto.', 'success' if ok else 'danger')
    return redirect(url_for('listar_productos'))

# --- Login y Registro ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", 
                           (nombre, email, password))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Usuario registrado correctamente', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error al registrar usuario: {e}', 'danger')
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        usuario = cargar_usuario_por_email(email)
        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)
            flash('Sesión iniciada correctamente', 'success')
            return redirect(url_for('listar_productos'))
        else:
            flash('Email o contraseña incorrectos', 'danger')
    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))

@app.route('/ruta-protegida')
@login_required
def ruta_protegida():
    return f"Hola {current_user.nombre}, estás en una ruta protegida."

@app.route('/about/')
def about():
    return render_template('about.html', title="About")

if __name__ == '__main__':
    app.run(debug=True)
