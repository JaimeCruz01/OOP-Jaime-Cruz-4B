class Conexion:

    def __init__(self):
        self.host = "localhost"
        self.usuario = "root"
        self.password = ""
        self.base_datos = "login_mvc"

    def conectar(self):
        try:
            conexion = mysql.connector.connect(
                host=self.host,
                user=self.usuario,
                password=self.password,
                database=self.base_datos
            )
            return conexion

        except mysql.connector.Error as error:
            print("Error al conectar con MySQL:", error)
            return None