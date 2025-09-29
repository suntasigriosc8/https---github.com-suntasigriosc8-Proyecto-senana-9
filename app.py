import logging
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from forms import ProductoForm, RegisterForm, LoginForm
from inventario import Inventario, Producto
from models import cargar_usuario_por_id, cargar_usuario_por_email
from conexion.conexion import obtener_conexion

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['SECRET_KEY'] = "mi_clave_secreta"

# Configuración para subir imágenes
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Inicializar Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return cargar_usuario_por_id(user_id)

# Inicializar inventario
try:
    inv = Inventario()
except Exception as e:
    print(f"No se pudo inicializar el inventario: {e}")
    inv = None

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.template_filter('sum')
def sum_filter(items, attribute):
    return sum(getattr(item, attribute) for item in items)

@app.route('/')
def index():
    return render_template('index.html', title="Inicio")

@app.route('/test_db')
def test_db():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return f"[✓] Conexión exitosa a la base de datos: {db_name}"
    except Exception as e:
        return f"[✗] Error de conexión a MySQL: {e}"

# --- CRUD de productos ---
@app.route('/productos')
@login_required
def listar_productos():
    q = request.args.get('q', '').strip()
    productos = inv.buscar_por_nombre(q) if q and inv else (inv.mostrar_todos() if inv else [])
    return render_template('productos/index.html', title="Productos", productos=productos, q=q)

@app.route('/productos/crear', methods=['GET', 'POST'])
@login_required
def crear_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        precio = float(form.precio.data)
        stock = form.stock.data

        # Manejar la imagen
        imagen_filename = None
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                imagen_filename = filename

        producto = Producto(id_producto=None, nombre=nombre, precio=precio, stock=stock, imagen=imagen_filename)
        ok = inv.agregar_producto(producto) if inv else False
        flash('Producto agregado.' if ok else 'Error al agregar producto.', 'success' if ok else 'danger')
        return redirect(url_for('listar_productos'))
    return render_template('productos/crear.html', title="Crear Producto", form=form)

@app.route('/productos/editar/<int:id_producto>', methods=['GET', 'POST'])
@login_required
def editar_producto(id_producto):
    if not inv:
        flash('Inventario no disponible.', 'danger')
        return redirect(url_for('listar_productos'))
    producto = inv.obtener(id_producto)
    if not producto:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('listar_productos'))
    form = ProductoForm()
    if request.method == 'GET':
        form.nombre.data = producto.nombre
        form.precio.data = producto.precio
        form.stock.data = producto.stock
    if form.validate_on_submit():
        nombre = form.nombre.data
        precio = float(form.precio.data)
        stock = form.stock.data

        # Manejar la imagen
        imagen_filename = producto.imagen
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                imagen_filename = filename

        inv.actualizar_producto(id_producto, nombre=nombre, precio=precio, stock=stock, imagen=imagen_filename)
        flash('Producto actualizado.', 'success')
        return redirect(url_for('listar_productos'))
    return render_template('productos/editar.html', title="Editar Producto", form=form, producto=producto)

@app.route('/productos/eliminar/<int:id_producto>', methods=['GET', 'POST'])
@login_required
def eliminar_producto(id_producto):
    if not inv:
        flash('Inventario no disponible.', 'danger')
        return redirect(url_for('listar_productos'))
    producto = inv.obtener(id_producto)
    if not producto:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('listar_productos'))
    if request.method == 'POST':
        ok = inv.eliminar_producto(id_producto)
        flash('Producto eliminado.' if ok else 'No se pudo eliminar el producto.', 'success' if ok else 'danger')
        return redirect(url_for('listar_productos'))
    return render_template('productos/eliminar.html', title="Eliminar Producto", producto=producto)

# Ruta para el inventario
@app.route('/inventario')
@login_required
def inventario():
    q = request.args.get('q', '').strip()
    productos = inv.buscar_por_nombre(q) if q and inv else (inv.mostrar_todos() if inv else [])
    return render_template('productos/inventario.html', title="Inventario", productos=productos, q=q)

# --- Login y Registro ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", (nombre, email, password))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Usuario registrado correctamente. Por favor, inicia sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error al registrar usuario: {e}', 'danger')
    return render_template('auth/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        usuario = cargar_usuario_por_email(email)
        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)
            next_page = request.args.get('next')
            flash('Sesión iniciada correctamente', 'success')
            return redirect(next_page or url_for('listar_productos'))
        else:
            flash('Email o contraseña incorrectos', 'danger')
    return render_template('auth/login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))

@app.route('/about/')
def about():
    return render_template('about.html', title="Acerca de")

if __name__ == '__main__':
    app.run(debug=True)
