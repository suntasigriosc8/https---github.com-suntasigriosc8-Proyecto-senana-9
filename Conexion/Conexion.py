import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234567",  # Cambia si tienes contraseña
            database="desarrollo_web",
            port=3306
        )
        if conn.is_connected():
            return conn
        else:
            raise Exception("No se pudo establecer conexión con la base de datos.")
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise
