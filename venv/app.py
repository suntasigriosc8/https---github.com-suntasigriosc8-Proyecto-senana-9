
from flask import Flask, render_template, request, redirect, url_for, flash
from Conexion.Conexion import conectar, cerrar_conexion
from datetime import datetime
from forms import productoforms

app = Flask(__name__)
app.config['SECRET_KEY'] = "mi_clave_secreta"

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

@app.route('/')
def index():
    return render_template('index.html', title="Inicio")

@app.route('/productos')
def listar_productos():
    q = request.args.get('q', '').strip()
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    if q:
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE %s", ('%' + q + '%',))
    else:
        cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cerrar_conexion(conexion)
    return render_template('productos/index.html', title="Productos", productos=productos, q=q)

@app.route('/productos/agregar', methods=['GET', 'POST'])
def agregar_producto():
    form = productoforms()
    if form.validate_on_submit():
        nombre = form.nombre.data
        cantidad = form.cantidad.data
        precio = form.precio.data
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (%s, %s, %s)", (nombre, cantidad, precio))
        conexion.commit()
        cerrar_conexion(conexion)
        flash('Producto agregado exitosamente!', 'success')
        return redirect(url_for('listar_productos'))
    return render_template('agregar_producto.html', title="Agregar Producto", form=form)

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cursor.fetchone()
    
    if not producto:
        cerrar_conexion(conexion)
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('listar_productos'))
    
    form = productoforms(data=producto)
    if form.validate_on_submit():
        nombre = form.nombre.data
        cantidad = form.cantidad.data
        precio = form.precio.data
        cursor = conexion.cursor()
        cursor.execute("UPDATE productos SET nombre=%s, cantidad=%s, precio=%s WHERE id=%s", (nombre, cantidad, precio, id))
        conexion.commit()
        cerrar_conexion(conexion)
        flash('Producto actualizado exitosamente!', 'success')
        return redirect(url_for('listar_productos'))
    
    cerrar_conexion(conexion)
    return render_template('editar_producto.html', title="Editar Producto", form=form, producto=producto)

@app.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conexion.commit()
    cerrar_conexion(conexion)
    flash('Producto eliminado exitosamente!', 'success')
    return redirect(url_for('listar_productos'))

@app.route('/about/')
def about():
    return render_template('about.html', title="About")

if __name__ == '__main__':
    app.run(debug=True)

