# Clase conexion sin sqlalchelmy
import mysql.connector
from mysql.connector import Error
from typing import Optional

def conectar(host: str = "localhost",
            user: str = "root",
            password: str = "",
            database: str = "flask_db",
            **kwargs) -> Optional[mysql.connector.connection_cext.CMySQLConnection]:
    """
    Intenta conectar a MySQL y devuelve la conexión.
    Lanza mysql.connector.Error si falla la conexión.
    Parámetros pueden sobreescribirse al llamar.
    """
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            **kwargs
        )
        return conn
    except Error as e:
        # No silenciar el error: registrar y volver a lanzar para que la aplicación lo maneje
        print(f"[Conexion] Error al conectar a la BD: {e}")
        raise

def cerrar_conexion(conexion: Optional[mysql.connector.connection_cext.CMySQLConnection]) -> None:
    """
    Cierra la conexión si está abierta. No falla si se pasa None.
    """
    try:
        if conexion is None:
            return
        # algunos conectores usan is_connected()
        is_conn = getattr(conexion, "is_connected", None)
        if callable(is_conn):
            if conexion.is_connected():
                conexion.close()
                # print opcional para debug
                print("Conexión cerrada.")
        else:
            # intentar cerrar de forma segura
            conexion.close()
            print("Conexión cerrada.")
    except Exception as e:
        # registrar sin lanzar para evitar romper el flujo de la app al cerrar
        print(f"[Conexion] Error al cerrar la conexión: {e}")

