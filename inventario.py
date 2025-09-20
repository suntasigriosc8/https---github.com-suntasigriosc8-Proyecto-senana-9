import sqlite3
from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path

DB_PATH = Path(__file__).parent / "inventario.db"

@dataclass
class Producto:
    id: Optional[int]
    nombre: str
    cantidad: int
    precio: float

    @classmethod
    def from_row(cls, row):
        return cls(id=row["id"], nombre=row["nombre"], cantidad=row["cantidad"], precio=row["precio"])

    def to_tuple(self, include_id=False):
        if include_id:
            return (self.id, self.nombre, self.cantidad, self.precio)
        return (self.nombre, self.cantidad, self.precio)

    def __repr__(self):
        return f"Producto(id={self.id}, nombre='{self.nombre}', cantidad={self.cantidad}, precio={self.precio})"


class Inventario:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = Path(db_path) if db_path else DB_PATH
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._productos: Dict[int, Producto] = {}
        self._crear_tabla()
        self._cargar_desde_db()

    def _crear_tabla(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        self._productos = {row["id"]: Producto.from_row(row) for row in rows}

    def agregar_producto(self, producto: Producto) -> bool:
        cur = self.conn.cursor()
        # si se proporciona id, verificar existencia
        if producto.id is not None:
            if producto.id in self._productos:
                return False
            cur.execute(
                "INSERT INTO productos (id, nombre, cantidad, precio) VALUES (?, ?, ?, ?)",
                producto.to_tuple(include_id=True)
            )
        else:
            cur.execute(
                "INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
                producto.to_tuple(include_id=False)
            )
            producto.id = cur.lastrowid
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

    def actualizar_producto(self, id: int, nombre: Optional[str] = None,
                           cantidad: Optional[int] = None, precio: Optional[float] = None) -> bool:
        if id not in self._productos:
            return False
        producto = self._productos[id]
        new_nombre = nombre if nombre is not None else producto.nombre
        new_cantidad = cantidad if cantidad is not None else producto.cantidad
        new_precio = precio if precio is not None else producto.precio
        cur = self.conn.cursor()
        cur.execute("UPDATE productos SET nombre = ?, cantidad = ?, precio = ? WHERE id = ?",
                    (new_nombre, new_cantidad, new_precio, id))
        self.conn.commit()
        producto.nombre = new_nombre
        producto.cantidad = new_cantidad
        producto.precio = new_precio
        return True

    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        pattern = f"%{nombre}%"
        cur = self.conn.cursor()
        cur.execute("SELECT id, nombre, cantidad, precio FROM productos WHERE nombre LIKE ?", (pattern,))
        rows = cur.fetchall()
        return [Producto.from_row(row) for row in rows]

    def mostrar_todos(self) -> List[Producto]:
        return list(self._productos.values())

    def obtener(self, id: int) -> Optional[Producto]:
        return self._productos.get(id)

    def cerrar(self):
        try:
            self.conn.close()
        except Exception:
            pass