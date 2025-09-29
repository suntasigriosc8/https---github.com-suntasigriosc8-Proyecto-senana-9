from conexion.conexion import obtener_conexion
from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email, password):
        self.id = id_usuario
        self.nombre = nombre
        self.email = email
        self.password = password

def cargar_usuario_por_id(id_usuario):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_usuario, nombre, email, password FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return Usuario(row['id_usuario'], row['nombre'], row['email'], row['password'])
    except Exception as e:
        print(f"Error al cargar usuario por ID: {e}")
    return None

def cargar_usuario_por_email(email):
    try:
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_usuario, nombre, email, password FROM usuarios WHERE email = %s", (email,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return Usuario(row['id_usuario'], row['nombre'], row['email'], row['password'])
    except Exception as e:
        print(f"Error al cargar usuario por email: {e}")
    return None
