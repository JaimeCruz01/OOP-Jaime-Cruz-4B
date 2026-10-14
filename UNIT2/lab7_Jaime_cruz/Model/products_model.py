from Controller.database_connection import Database_connection

class Producto:
    def __init__(self, id=None, nombre=None, precio=None, stock=None):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.db = Database_connection()

    def obtener_todos(self):
        "Retorna una lista con todos los productos registrados."
        query = "SELECT id_producto, nombre, precio, cantidad FROM products"
        return self.db.ejecutar_consulta(query)

    def guardar(self):
        "Insertar un nuevo producto en la base de datos."
        query = "INSERT INTO products (nombre, precio, cantidad) VALUES (%s, %s, %s)"
        conexion = self.db.obtener_conexion()
        if not conexion:
            return False
        
        cursor = conexion.cursor()
        try:
            cursor.execute(query, (self.nombre, self.precio, self.stock))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al guardar producto: {e}")
            return False
        finally:
            cursor.close()
            conexion.close()