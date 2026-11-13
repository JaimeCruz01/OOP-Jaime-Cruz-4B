from product import Product, ProductoNoEncontrado
class Inventario:
    def __init__(self):
        self.productos = {
            "P01": Product("P01", 5),
            "P02": Product("P02", 10),
            "P03": Product("P03", 15)
        }

    def retirar(self, codigo, cantidad):

        if codigo not in self.productos:
            raise ProductoNoEncontrado(
                f"El producto {codigo} no existe en el inventario."
            )

        self.productos[codigo].retirar(cantidad)