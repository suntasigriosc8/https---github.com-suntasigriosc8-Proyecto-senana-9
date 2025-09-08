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
        self.conn.close()        from inventario import Inventario, Producto
        
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
            menu()