import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from forms import ProductoForm  
from inventario import Inventario, Producto

# Configuración de logging para depuración
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")

# Inicialización de la aplicación Flask
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['SECRET_KEY'] = "mi_clave_secreta"  # Clave para formularios seguros

# Inicializar inventario
try:
    inv = Inventario()
except Exception:
    app.logger.exception("Error inicializando Inventario (revisa inventario.py / inventario.db):")
    inv = None

# Inyectar fecha actual en todas las plantillas
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html', title="Inicio")

# Listar productos
@app.route('/productos', methods=['GET', 'POST'])
def listar_productos():
    q = request.args.get('q', '').strip()
    productos = inv.buscar_por_nombre(q) if q and inv else (inv.mostrar_todos() if inv else [])
    return render_template('productos/index.html', title="Productos", productos=productos, q=q)

# Agregar producto
@app.route('/productos/agregar', methods=['GET', 'POST'])
def agregar_producto():
    form = ProductoForm()  # 
    if form.validate_on_submit():
        nombre = form.nombre.data
        cantidad = form.cantidad.data
        precio = float(form.precio.data)
        producto = Producto(id=None, nombre=nombre, cantidad=cantidad, precio=precio)
        ok = inv.agregar_producto(producto) if inv else False
        flash('Producto agregado.' if ok else 'Error al agregar producto.', 'success' if ok else 'danger')
        return redirect(url_for('listar_productos'))
    return render_template('productos/agregar_producto.html', title="Agregar Producto", form=form)

# Editar producto
@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
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

# Eliminar producto
@app.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    ok = inv.eliminar_producto(id) if inv else False
    flash('Producto eliminado.' if ok else 'No se encontró el producto.', 'success' if ok else 'danger')
    return redirect(url_for('listar_productos'))

# Página "Acerca de"
@app.route('/about/')
def about():
    return render_template('about.html', title="About")

# Manejo de errores 500
@app.errorhandler(500)
def internal_error(error):
    app.logger.exception("500 Internal Server Error:")
    try:
        return render_template("500.html"), 500
    except Exception:
        return "Error interno del servidor. Revisa los logs en la consola.", 500

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
