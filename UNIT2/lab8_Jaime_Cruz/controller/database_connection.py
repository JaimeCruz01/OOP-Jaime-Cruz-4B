import os
import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    """Administra conexiones a la base de datos MySQL."""

    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.database = os.getenv("DB_NAME", "login_mvc")
        self.port = int(os.getenv("DB_PORT", "3306"))

    def connect(self):
        """Devuelve una conexión activa o None si falla."""
        try:
            return mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                connection_timeout=5,
            )
        except Error as error:
            print(f"Error al conectar con MySQL: {error}")
            return None

    def test_connection(self):
        """Comprueba conexión y consulta básica."""
        connection = self.connect()
        if connection is None:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            return True
        except Error as error:
            print(f"Error al probar la base de datos: {error}")
            return False
        finally:
            connection.close()
