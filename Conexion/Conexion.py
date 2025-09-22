import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root", # Cambia "root" por tu usuario de MySQL
        password="1234567", # Cambia "1234567" por tu contraseña de MySQL
        database="venta_por_catalogo"
    )
