import mysql.connector

def conexion():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="tu_password",
            database="tu_base"
        )
        print("✅ Conexión establecida con MySQL.")
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Error al conectar a MySQL: {e}")
        return None

def cerrar_conexion(conn):
    if conn:
        conn.close()
        print("🔒 Conexión cerrada correctamente.")
