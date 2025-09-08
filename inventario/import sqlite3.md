import sqlite3
from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path

DB_PATH = Path(__file__).parent / "inventario.db"

@dataclass
class Producto:
    id: int
    nombre: str
    cantidad: int
    precio: float

    @classmethod
    def from_row(cls, row):
        return cls(id=row[0], nombre=row[1], cantidad=row[2], precio=row[3])

    def __repr__(self):
        return f"Producto(id={self.id}, nombre='{self.nombre}', cantidad={self.cantidad}, precio={self.precio})"


class Inventario:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = Path(db_path) if db_path else DB_PATH
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._productos: Dict[int, Producto] = {}
        self._crear_tabla()
        self._cargar_desde_db()

    def _crear_tabla(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )
        """)
        self.conn.commit()

    def _cargar_desde_db(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, nombre, cantidad, precio FROM productos")
        rows = cur.fetchall()
        self._productos = {row["id"]: Producto.from_row((row["id"], row["nombre"], row["cantidad"], row["precio"])) for row in rows}

    def agregar_producto(self, producto: Producto) -> bool:
        if producto.id in self._productos:
            return False
        cur = self.conn.cursor()
        cur.execute("INSERT INTO productos (id, nombre, cantidad, precio) VALUES (?, ?, ?, ?)",
                    (producto.id, producto.nombre, producto.cantidad, producto.precio))
        self.conn.commit()
        self._productos[producto.id] = producto
        return True

    def eliminar_producto(self, id: int) -> bool:
        if id not in self._productos:
            return False
        cur = self.conn.cursor()
        cur.execute("DELETE FROM productos WHERE id = ?", (id,))
        self.conn.commit()
        del self._productos[id]
        return True

    def actualizar_producto(self, id: int, cantidad: Optional[int] = None, precio: Optional[float] = None) -> bool:
        if id not in self._productos:
            return False
        producto = self._productos[id]
        new_cantidad = cantidad if cantidad is not None else producto.cantidad
        new_precio = precio if precio is not None else producto.precio
        cur = self.conn.cursor()
        cur.execute("UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?", (new_cantidad, new_precio, id))
        self.conn.commit()
        producto.cantidad = new_cantidad
        producto.precio = new_precio
        return True

    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        pattern = f"%{nombre}%"
        cur = self.conn.cursor()
        cur.execute("SELECT id, nombre, cantidad, precio FROM productos WHERE nombre LIKE ?", (pattern,))
        rows = cur.fetchall()
        return [Producto.from_row((row["id"], row["nombre"], row["cantidad"], row["precio"])) for row in rows]

    def mostrar_todos(self) -> List[Producto]:
        return list(self._productos.values())

    def obtener(self, id: int) -> Optional[Producto]:
        return self._productos.get(id)

    def cerrar(self):
        self.conn.close()        import sqlite3
        from dataclasses import dataclass
        from typing import Dict, List, Optional
        from pathlib import Path
        
        DB_PATH = Path(__file__).parent / "inventario.db"
        
        @dataclass
        class Producto:
            id: int
            nombre: str
            cantidad: int
            precio: float
        
            @classmethod
            def from_row(cls, row):
                return cls(id=row[0], nombre=row[1], cantidad=row[2], precio=row[3])
        
            def __repr__(self):
                return f"Producto(id={self.id}, nombre='{self.nombre}', cantidad={self.cantidad}, precio={self.precio})"
        
        
        class Inventario:
            def __init__(self, db_path: Optional[str] = None):
                self.db_path = Path(db_path) if db_path else DB_PATH
                self.conn = sqlite3.connect(self.db_path)
                self.conn.row_factory = sqlite3.Row
                self._productos: Dict[int, Producto] = {}
                self._crear_tabla()
                self._cargar_desde_db()
        
            def _crear_tabla(self):
                cur = self.conn.cursor()
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS productos (
                        id INTEGER PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        cantidad INTEGER NOT NULL,
                        precio REAL NOT NULL
                    )
                """)
                self.conn.commit()
        
            def _cargar_desde_db(self):
                cur = self.conn.cursor()
                cur.execute("SELECT id, nombre, cantidad, precio FROM productos")
                rows = cur.fetchall()
                self._productos = {row["id"]: Producto.from_row((row["id"], row["nombre"], row["cantidad"], row["precio"])) for row in rows}
        
            def agregar_producto(self, producto: Producto) -> bool:
                if producto.id in self._productos:
                    return False
                cur = self.conn.cursor()
                cur.execute("INSERT INTO productos (id, nombre, cantidad, precio) VALUES (?, ?, ?, ?)",
                            (producto.id, producto.nombre, producto.cantidad, producto.precio))
                self.conn.commit()
                self._productos[producto.id] = producto
                return True
        
            def eliminar_producto(self, id: int) -> bool:
                if id not in self._productos:
                    return False
                cur = self.conn.cursor()
                cur.execute("DELETE FROM productos WHERE id = ?", (id,))
                self.conn.commit()
                del self._productos[id]
                return True
        
            def actualizar_producto(self, id: int, cantidad: Optional[int] = None, precio: Optional[float] = None) -> bool:
                if id not in self._productos:
                    return False
                producto = self._productos[id]
                new_cantidad = cantidad if cantidad is not None else producto.cantidad
                new_precio = precio if precio is not None else producto.precio
                cur = self.conn.cursor()
                cur.execute("UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?", (new_cantidad, new_precio, id))
                self.conn.commit()
                producto.cantidad = new_cantidad
                producto.precio = new_precio
                return True
        
            def buscar_por_nombre(self, nombre: str) -> List[Producto]:
                pattern = f"%{nombre}%"
                cur = self.conn.cursor()
                cur.execute("SELECT id, nombre, cantidad, precio FROM productos WHERE nombre LIKE ?", (pattern,))
                rows = cur.fetchall()
                return [Producto.from_row((row["id"], row["nombre"], row["cantidad"], row["precio"])) for row in rows]
        
            def mostrar_todos(self) -> List[Producto]:
                return list(self._productos.values())
        
            def obtener(self, id: int) -> Optional[Producto]:
                return self._productos.get(id)
        
            def cerrar(self):
                self.conn.close()                import sqlite3
                from dataclasses import dataclass
                from typing import Dict, List, Optional
                from pathlib import Path
                
                DB_PATH = Path(__file__).parent / "inventario.db"
                
                @dataclass
                class Producto:
                    id: int
                    nombre: str
                    cantidad: int
                    precio: float
                
                    @classmethod
                    def from_row(cls, row):
                        return cls(id=row[0], nombre=row[1], cantidad=row[2], precio=row[3])
                
                    def __repr__(self):
                        return f"Producto(id={self.id}, nombre='{self.nombre}', cantidad={self.cantidad}, precio={self.precio})"
                
                
                class Inventario:
                    def __init__(self, db_path: Optional[str] = None):
                        self.db_path = Path(db_path) if db_path else DB_PATH
                        self.conn = sqlite3.connect(self.db_path)
                        self.conn.row_factory = sqlite3.Row
                        self._productos: Dict[int, Producto] = {}
                        self._crear_tabla()
                        self._cargar_desde_db()
                
                    def _crear_tabla(self):
                        cur = self.conn.cursor()
                        cur.execute("""
                            CREATE TABLE IF NOT EXISTS productos (
                                id INTEGER PRIMARY KEY,
                                nombre TEXT NOT NULL,
                                cantidad INTEGER NOT NULL,
                                precio REAL NOT NULL
                            )
                        """)
                        self.conn.commit()
                
                    def _cargar_desde_db(self):
                        cur = self.conn.cursor()
                        cur.execute("SELECT id, nombre, cantidad, precio FROM productos")
                        rows = cur.fetchall()
                        self._productos = {row["id"]: Producto.from_row((row["id"], row["nombre"], row["cantidad"], row["precio"])) for row in rows}
                
                    def agregar_producto(self, producto: Producto) -> bool:
                        if producto.id in self._productos:
                            return False
                        cur = self.conn.cursor()
                        cur.execute("INSERT INTO productos (id, nombre, cantidad, precio) VALUES (?, ?, ?, ?)",
                                    (producto.id, producto.nombre, producto.cantidad, producto.precio))
                        self.conn.commit()
                        self._productos[producto.id] = producto
                        return True
                
                    def eliminar_producto(self, id: int) -> bool:
                        if id not in self._productos:
                            return False
                        cur = self.conn.cursor()
                        cur.execute("DELETE FROM productos WHERE id = ?", (id,))
                        self.conn.commit()
                        del self._productos[id]
                        return True
                
                    def actualizar_producto(self, id: int, cantidad: Optional[int] = None, precio: Optional[float] = None) -> bool:
                        if id not in self._productos:
                            return False
                        producto = self._productos[id]
                        new_cantidad = cantidad if cantidad is not None else producto.cantidad
                        new_precio = precio if precio is not None else producto.precio
                        cur = self.conn.cursor()
                        cur.execute("UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?", (new_cantidad, new_precio, id))
                        self.conn.commit()
                        producto.cantidad = new_cantidad
                        producto.precio = new_precio
                        return True
                
                    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
                        pattern = f"%{nombre}%"
                        cur = self.conn.cursor()
                        cur.execute("SELECT id, nombre, cantidad, precio FROM productos WHERE nombre LIKE ?", (pattern,))
                        rows = cur.fetchall()
                        return [Producto.from_row((row["id"], row["nombre"], row["cantidad"], row["precio"])) for row in rows]
                
                    def mostrar_todos(self) -> List[Producto]:
                        return list(self._productos.values())
                
                    def obtener(self, id: int) -> Optional[Producto]:
                        return self._productos.get(id)
                
                    def cerrar(self):
                        self.conn.close()                        from inventario import Inventario, Producto
                        
                        def menu():
                            inventario = Inventario()
                            try:
                                while True:
                                    print("\n--- Menú de Inventario ---")
                                    print("1. Agregar producto")
                                    print("2. Eliminar producto")
                                    print("3. Actualizar producto")
                                    print("4. Buscar producto por nombre")
                                    print("5. Mostrar todos los productos")
                                    print("6. Salir")
                                    opcion = input("Seleccione una opción: ")
                        
                                    if opcion == "1":
                                        id = int(input("ID: "))
                                        nombre = input("Nombre: ")
                                        cantidad = int(input("Cantidad: "))
                                        precio = float(input("Precio: "))
                                        producto = Producto(id, nombre, cantidad, precio)
                                        ok = inventario.agregar_producto(producto)
                                        print("Producto agregado." if ok else "ID ya existe. No se agregó.")
                                    elif opcion == "2":
                                        id = int(input("ID del producto a eliminar: "))
                                        ok = inventario.eliminar_producto(id)
                                        print("Producto eliminado." if ok else "No existe el ID.")
                                    elif opcion == "3":
                                        id = int(input("ID del producto a actualizar: "))
                                        cantidad = input("Nueva cantidad (enter para mantener): ")
                                        precio = input("Nuevo precio (enter para mantener): ")
                                        cantidad_val = int(cantidad) if cantidad.strip() != "" else None
                                        precio_val = float(precio) if precio.strip() != "" else None
                                        ok = inventario.actualizar_producto(id, cantidad_val, precio_val)
                                        print("Producto actualizado." if ok else "No existe el ID.")
                                    elif opcion == "4":
                                        nombre = input("Nombre a buscar: ")
                                        productos = inventario.buscar_por_nombre(nombre)
                                        for p in productos:
                                            print(p)
                                        if not productos:
                                            print("No se encontraron productos.")
                                    elif opcion == "5":
                                        productos = inventario.mostrar_todos()
                                        for p in productos:
                                            print(p)
                                        if not productos:
                                            print("Inventario vacío.")
                                    elif opcion == "6":
                                        print("Saliendo...")
                                        break
                                    else:
                                        print("Opción no válida.")
                            finally:
                                inventario.cerrar()
                        
                        if __name__ == "__main__":
                            menu()                            from flask import Flask, render_template, request, redirect, url_for
                            from inventario import Inventario, Producto
                            
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
                                app.run(debug=True)                                <!doctype html>
                                <html lang="es">
                                <head>
                                    <meta charset="utf-8">
                                    <title>{% block title %}Inventario{% endblock %}</title>
                                    <meta name="viewport" content="width=device-width, initial-scale=1">
                                    <style>
                                        body { font-family: Arial, sans-serif; margin: 20px; }
                                        table { border-collapse: collapse; width: 100%; }
                                        th, td { border: 1px solid #ddd; padding: 8px; }
                                        th { background: #f2f2f2; }
                                    </style>
                                </head>
                                <body>
                                    <nav>
                                        <a href="{{ url_for('productos') }}">Productos</a> |
                                        <a href="{{ url_for('about') }}">Acerca</a>
                                    </nav>
                                    <hr>
                                    {% block content %}{% endblock %}
                                </body>
                                </html>                                {% extends "base.html" %}
                                {% block title %}Productos{% endblock %}
                                {% block content %}
                                <h1>Productos en Inventario</h1>
                                
                                <form action="{{ url_for('agregar_producto') }}" method="post">
                                    <h3>Agregar producto</h3>
                                    <label>ID: <input name="id" required></label>
                                    <label>Nombre: <input name="nombre" required></label>
                                    <label>Cantidad: <input name="cantidad" type="number" required></label>
                                    <label>Precio: <input name="precio" type="number" step="0.01" required></label>
                                    <button type="submit">Agregar</button>
                                </form>
                                
                                <table>
                                    <thead>
                                        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
                                    </thead>
                                    <tbody>
                                    {% for p in productos %}
                                        <tr>
                                            <td>{{ p.id }}</td>
                                            <td>{{ p.nombre }}</td>
                                            <td>{{ p.cantidad }}</td>
                                            <td>{{ "%.2f"|format(p.precio) }}</td>
                                        </tr>
                                    {% else %}
                                        <tr><td colspan="4">No hay productos</td></tr>
                                    {% endfor %}
                                    </tbody>
                                </table>
                                {% endblock %}                                Proyecto de gestión de inventario (Ejemplo)
                                
                                Instrucciones:
                                - Instala dependencias: pip install -r requirements.txt
                                - Ejecutar CLI: python -m cli.menu
                                - Ejecutar web: python app.py (acceder a http://127.0.0.1:5000)
                                
                                Estructura:
                                - inventario.py : modelo Producto y clase Inventario con persistencia SQLite.
                                - templates/ : plantillas Jinja para la interfaz web.
                                - cli/menu.py : menú interactivo por consola.                                import sqlite3
                                from dataclasses import dataclass
                                from typing import Dict, List, Optional
                                from pathlib import Path
                                
                                DB_PATH = Path(__file__).parent / "inventario.db"
                                
                                @dataclass
                                class Producto:
                                    id: int
                                    nombre: str
                                    cantidad: int
                                    precio: float
                                
                                    @classmethod
                                    def from_row(cls, row):
                                        return cls(id=row[0], nombre=row[1], cantidad=row[2], precio=row[3])
                                
                                    def __repr__(self):
                                        return f"Producto(id={self.id}, nombre='{self.nombre}', cantidad={self.cantidad}, precio={self.precio})"
                                
                                
                                class Inventario:
                                    def __init__(self, db_path: Optional[str] = None):
                                        self.db_path = Path(db_path) if db_path else DB_PATH
                                        self.conn = sqlite3.connect(self.db_path)
                                        self.conn.row_factory = sqlite3.Row
                                        self._productos: Dict[int, Producto] = {}
                                        self._crear_tabla()
                                        self._cargar_desde_db()
                                
                                    def _crear_tabla(self):
                                        cur = self.conn.cursor()
                                        cur.execute("""
                                            CREATE TABLE IF NOT EXISTS productos (
                                                id INTEGER PRIMARY KEY,
                                                nombre TEXT NOT NULL,
                                                cantidad INTEGER NOT NULL,
                                                precio REAL NOT NULL
                                            )
                                        """)
                                        self.conn.commit()
                                
                                    def _cargar_desde_db(self):
                                        cur = self.conn.cursor()
                                        cur.execute("SELECT id, nombre, cantidad, precio FROM productos")
                                        rows = cur.fetchall()
                                        self._productos = {row["id"]: Producto.from_row((row["id"], row["nombre"], row["cantidad"], row["precio"])) for row in rows}
                                
                                    def agregar_producto(self, producto: Producto) -> bool:
                                        if producto.id in self._productos:
                                            return False
                                        cur = self.conn.cursor()
                                        cur.execute("INSERT INTO productos (id, nombre, cantidad, precio) VALUES (?, ?, ?, ?)",
                                                    (producto.id, producto.nombre, producto.cantidad, producto.precio))
                                        self.conn.commit()
                                        self._productos[producto.id] = producto
                                        return True
                                
                                    def eliminar_producto(self, id: int) -> bool:
                                        if id not in self._productos:
                                            return False
                                        cur = self.conn.cursor()
                                        cur.execute("DELETE FROM productos WHERE id = ?", (id,))
                                        self.conn.commit()
                                        del self._productos[id]
                                        return True
                                
                                    def actualizar_producto(self, id: int, cantidad: Optional[int] = None, precio: Optional[float] = None) -> bool:
                                        if id not in self._productos:
                                            return False
                                        producto = self._productos[id]
                                        new_cantidad = cantidad if cantidad is not None else producto.cantidad
                                        new_precio = precio if precio is not None else producto.precio
                                        cur = self.conn.cursor()
                                        cur.execute("UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?", (new_cantidad, new_precio, id))
                                        self.conn.commit()
                                        producto.cantidad = new_cantidad
                                        producto.precio = new_precio
                                        return True
                                
                                    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
                                        pattern = f"%{nombre}%"
                                        cur = self.conn.cursor()
                                        cur.execute("SELECT id, nombre, cantidad, precio FROM productos WHERE nombre LIKE ?", (pattern,))
                                        rows = cur.fetchall()
                                        return [Producto.from_row((row["id"], row["nombre"], row["cantidad"], row["precio"])) for row in rows]
                                
                                    def mostrar_todos(self) -> List[Producto]:
                                        return list(self._productos.values())
                                
                                    def obtener(self, id: int) -> Optional[Producto]:
                                        return self._productos.get(id)
                                
                                    def cerrar(self):
                                        self.conn.close()# Code Citations

## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>

```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>

```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
   
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">

```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
   
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{%
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Invent
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{%
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% end
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>

```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>
   
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>
    <
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>
    <meta
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>
    <meta name
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>
    <meta name="
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>
    <meta name="viewport
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>
    <meta name="viewport"
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>
    <meta name="viewport" content
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>
    <meta name="viewport" content="
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>
    <meta name="viewport" content="width
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>
    <meta name="viewport" content="width=device
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>
    <meta name="viewport" content="width=device-width
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>
    <meta name="viewport" content="width=device-width,
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>
    <meta name="viewport" content="width=device-width, initial
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>
    <meta name="viewport" content="width=device-width, initial-scale
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>
    <meta name="viewport" content="width=device-width, initial-scale=
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1
```


## License: desconocido
https://github.com/george39/AplicacionInventario/blob/b20bedc75e05296dde458ec5d291bb63911e93e7/src/templates/base/base.html

```
>
<head>
    <meta charset="utf-8">
    <title>{% block title %}Inventario{% endblock %}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1"
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>

```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
   
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>

```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
       
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>C
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>C
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>C
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>

```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>

```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>

```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
   
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
   
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
   
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>

```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>

```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>

```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
   
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
   
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
   
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>

```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>

```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>

```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
   
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
   
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
   
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {%
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {%
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {%
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}

```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}

```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}

```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
       
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
       
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
       
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>

```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>

```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>

```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
           
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
           
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
           
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>

```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>

```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>

```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
           
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
           
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
           
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>

```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>

```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>

```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
           
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
           
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
           
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td>{{
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td>{{
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td>{{
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td>{{ p
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td>{{ p
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td>{{ p
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td>{{ p.c
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td>{{ p.c
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td>{{ p.c
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td>{{ p.cantidad
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td>{{ p.cantidad
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td>{{ p.cantidad
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td>{{ p.cantidad }}</
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td>{{ p.cantidad }}</
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td>{{ p.cantidad }}</
```


## License: desconocido
https://github.com/KAOXDC/2067960/blob/636b8e3ac6790ae7a0a53dcbf646c3b66f520e50/templates/productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td>{{ p.cantidad }}</td
```


## License: desconocido
https://github.com/JESICA26/POO181/blob/f5ab662b652cdb2bf1c3650994b0efcb93bcbdd8/Examen2/ConsultaFlores.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td>{{ p.cantidad }}</td
```


## License: desconocido
https://github.com/Nic0G0nzalez/Tercera-pre-entrega-Gonzalez-Nicolas-prueba/blob/bb3b3b17c699fe0aa5c4f447c02eda307bd45cd1/Almendra_y_coco/Dietetica/templates/Dietetica/Productos.html

```
<table>
    <thead>
        <tr><th>ID</th><th>Nombre</th><th>Cantidad</th><th>Precio</th></tr>
    </thead>
    <tbody>
    {% for p in productos %}
        <tr>
            <td>{{ p.id }}</td>
            <td>{{ p.nombre }}</td>
            <td>{{ p.cantidad }}</td
```

