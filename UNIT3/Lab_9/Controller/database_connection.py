"""Conexión y ejecución de consultas para PostgreSQL (psycopg 3)."""

import psycopg
from psycopg.rows import dict_row

from Controller.config import DB_config


class Database_connection:
    def __init__(self):
        self.config = DB_config

    def get_connection(self):
        try:
            return psycopg.connect(**self.config)
        except psycopg.Error as error:
            print(f"Error al conectar con PostgreSQL: {error}")
            return None

    def ejecutar_consulta(self, query, params=()):
        conexion = self.get_connection()
        if conexion is None:
            return None

        try:
            with conexion:
                with conexion.cursor(row_factory=dict_row) as cursor:
                    cursor.execute(query, params)
                    if cursor.description is None:
                        return None
                    return cursor.fetchall()
        except psycopg.Error as error:
            print(f"Error en la consulta SQL: {error}")
            return None
        finally:
            conexion.close()
