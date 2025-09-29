from dataclasses import dataclass
from typing import Dict, List, Optional
from conexion.conexion import obtener_conexion

@dataclass
class Producto:
    id_producto: Optional[int]
    nombre: str
    precio: float
    stock: int
    imagen: Optional[str]

    @classmethod
    def from_row(cls, row):
        return cls(
            id_producto=row["id_producto"],
            nombre=row["nombre"],
            precio=row["precio"],
            stock=row["stock"],
            imagen=row.get("imagen", "")
        )

    def to_tuple(self, include_id=False):
        if include_id:
            return (self.id_producto, self.nombre, self.precio, self.stock, self.imagen)
        return (self.nombre, self.precio, self.stock, self.imagen)

    def __repr__(self):
        return f"Producto(id_producto={self.id_producto}, nombre='{self.nombre}', precio={self.precio}, stock={self.stock}, imagen='{self.imagen}')"

class Inventario:
    def __init__(self):
        self._productos: Dict[int, Producto] = {}
        try:
            self._verificar_estructura_tabla()
            self._cargar_desde_db()
        except Exception as e:
            print(f"Error al inicializar Inventario: {e}")
            raise

    def _verificar_estructura_tabla(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Verifica si la tabla existe
            cursor.execute("""
                SELECT COUNT(*)
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_SCHEMA = 'desarrollo_web'
                AND TABLE_NAME = 'productos'
            """)
            if cursor.fetchone()[0] == 0:
                # Si no existe, créala
                cursor.execute("""
                    CREATE TABLE productos (
                        id_producto INT AUTO_INCREMENT PRIMARY KEY,
                        nombre VARCHAR(100) NOT NULL,
                        precio DECIMAL(10, 2) NOT NULL,
                        stock INT NOT NULL,
                        imagen VARCHAR(100)
                    )
                """)
                print("✅ Tabla 'productos' creada")

            # Verifica si la columna 'imagen' existe
            cursor.execute("""
                SELECT COUNT(*)
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = 'desarrollo_web'
                AND TABLE_NAME = 'productos'
                AND COLUMN_NAME = 'imagen'
            """)
            if cursor.fetchone()[0] == 0:
                # Si no existe, añade la columna
                cursor.execute("ALTER TABLE productos ADD COLUMN imagen VARCHAR(100)")
                print("✅ Columna 'imagen' añadida a la tabla 'productos'")

            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error al verificar/crear tabla: {e}")
            raise

    def _cargar_desde_db(self):
        try:
            conn = obtener_conexion()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_producto, nombre, precio, stock,
                       IFNULL(imagen, '') as imagen
                FROM productos
            """)
            rows = cursor.fetchall()
            self._productos = {row["id_producto"]: Producto.from_row(row) for row in rows}
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            raise

    def agregar_producto(self, producto: Producto) -> bool:
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            if producto.id_producto is not None:
                if producto.id_producto in self._productos:
                    cursor.close()
                    conn.close()
                    return False
                cursor.execute(
                    "INSERT INTO productos (id_producto, nombre, precio, stock, imagen) VALUES (%s, %s, %s, %s, %s)",
                    producto.to_tuple(include_id=True)
                )
            else:
                cursor.execute(
                    "INSERT INTO productos (nombre, precio, stock, imagen) VALUES (%s, %s, %s, %s)",
                    producto.to_tuple(include_id=False)
                )
                producto.id_producto = cursor.lastrowid
            conn.commit()
            self._productos[producto.id_producto] = producto
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al agregar producto: {e}")
            return False

    def eliminar_producto(self, id_producto: int) -> bool:
        if id_producto not in self._productos:
            return False
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
            conn.commit()
            del self._productos[id_producto]
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar producto: {e}")
            return False

    def actualizar_producto(self, id_producto: int, nombre: Optional[str] = None, precio: Optional[float] = None, stock: Optional[int] = None, imagen: Optional[str] = None) -> bool:
        if id_producto not in self._productos:
            return False
        try:
            producto = self._productos[id_producto]
            new_nombre = nombre if nombre is not None else producto.nombre
            new_precio = precio if precio is not None else producto.precio
            new_stock = stock if stock is not None else producto.stock
            new_imagen = imagen if imagen is not None else producto.imagen
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE productos
                SET nombre = %s, precio = %s, stock = %s, imagen = %s
                WHERE id_producto = %s
            """, (new_nombre, new_precio, new_stock, new_imagen, id_producto))
            conn.commit()
            producto.nombre = new_nombre
            producto.precio = new_precio
            producto.stock = new_stock
            producto.imagen = new_imagen
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al actualizar producto: {e}")
            return False

    def buscar_por_nombre(self, nombre: str) -> List[Producto]:
        try:
            pattern = f"%{nombre}%"
            conn = obtener_conexion()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT id_producto, nombre, precio, stock,
                       IFNULL(imagen, '') as imagen
                FROM productos
                WHERE nombre LIKE %s
            """, (pattern,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return [Producto.from_row(row) for row in rows]
        except Exception as e:
            print(f"Error al buscar productos: {e}")
            return []

    def mostrar_todos(self) -> List[Producto]:
        return list(self._productos.values())

    def obtener(self, id_producto: int) -> Optional[Producto]:
        return self._productos.get(id_producto)
