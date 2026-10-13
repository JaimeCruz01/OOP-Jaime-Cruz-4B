import psycopg
from config import DB_config

class Database_connection:
    def __init__(self):
         self.config = DB_config

    def get_connection(self):
        try:
            conexion = psycopg.connect(**self.config)
            return conexion
        except Exception as e:
            print(f"Error al conectar con PostgreSQL: {e}")
            return None

    def ejecutar_consulta(self, query, params=()):
            conexion = self.obtener_conexion()
            if not conexion:
                return None
            
            cursor = conexion.cursor(dictionary=True)
            try:
                cursor.execute(query, params)
                resultados = cursor.fetchall()
                return resultados
            except Exception as e:
                print(f"Error en la consulta SQL: {e}")
                return None
            finally:
                if conexion:
                    cursor.close()
                    conexion.close()
