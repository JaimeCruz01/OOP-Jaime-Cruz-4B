class UserModel:

    def __init__(self):
        self.conexion_db = Conexion()

    def registrar_usuario(self, nombre, email, password):
        conexion = self.conexion_db.conectar()

        if conexion is None:
            return "error"

        cursor = None

        try:
            cursor = conexion.cursor()

            consulta = """
                INSERT INTO users (nombre, email, password)
                VALUES (%s, %s, %s)
            """

            cursor.execute(consulta, (nombre, email, password))
            conexion.commit()

            return "ok"

        except mysql.connector.IntegrityError:
            return "duplicado"

        except mysql.connector.Error as error:
            print("Error al registrar usuario:", error)
            return "error"

        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()

    def validar_usuario(self, email, password):
        conexion = self.conexion_db.conectar()

        if conexion is None:
            return None

        cursor = None

        try:
            cursor = conexion.cursor()

            consulta = """
                SELECT id, nombre
                FROM users
                WHERE email = %s AND password = %s
            """

            cursor.execute(consulta, (email, password))
            usuario = cursor.fetchone()

            return usuario

        except mysql.connector.Error as error:
            print("Error al validar usuario:", error)
            return None

        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()

    def cerrar(self):
        # Cada operación cierra su propia conexión.
        # Se conserva este método para mantener la interfaz
        # del controlador sencilla.
        pass