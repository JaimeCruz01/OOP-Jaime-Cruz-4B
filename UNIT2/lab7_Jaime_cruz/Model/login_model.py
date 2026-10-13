
from Controller.database_connection import Database_connection


class User:
    def __init__(self, username, passw):
        self.username = username
        self.password = passw
        self.db = Database_connection()

    def autenticar(self):
        query = """SELECT id_user, username, nombre FROM login_system.users WHERE username = %s AND passw = %s"""

        result = self.db.ejecutar_consulta(query,(self.username, self.password))

        if result:
            print("Encontrado")
            return result[0]

        print("No encontrado")
        return None


