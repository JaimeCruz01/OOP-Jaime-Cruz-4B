"""Modelo de productos: operaciones SQL sobre login_system.products."""
from Controller.database_connection import Database_connection


class Producto:
    def __init__(self, id=None, nombre=None, precio=None, stock=None, descripcion=None):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.descripcion = descripcion
        self.db = Database_connection()

    def obtener_todos(self):
        """Devuelve los cinco campos reales con claves estables para Vista/exportadores."""
        query = """
            SELECT
                id_producto AS id,
                nombre,
                precio,
                cantidad AS stock,
                descripcion
            FROM login_system.products
            ORDER BY id_producto
        """
        return self.db.ejecutar_consulta(query)

    def guardar(self):
        """Inserta un producto en el esquema correcto."""
        query = """
            INSERT INTO login_system.products
                (nombre, precio, cantidad, descripcion)
            VALUES (%s, %s, %s, %s)
        """
        conexion = self.db.get_connection()
        if conexion is None:
            return False
        try:
            with conexion:
                with conexion.cursor() as cursor:
                    cursor.execute(
                        query,
                        (self.nombre, self.precio, self.stock, self.descripcion or self.nombre),
                    )
            return True
        except Exception as error:
            print(f"Error al guardar producto: {error}")
            return False
        finally:
            conexion.close()
