class ErrorInventario(Exception):
    """Excepción base del inventario."""
    pass


class ProductoNoEncontrado(ErrorInventario):
    pass


class CantidadInvalida(ErrorInventario):
    pass


class StockInsuficiente(ErrorInventario):
    pass

class Product:
    def __init__(self, codigo, stock):
        self.codigo = codigo
        self.stock = stock

    def retirar(self, cantidad):

        if cantidad <= 0:
            raise CantidadInvalida(
                "La cantidad a retirar debe ser un número positivo."
            )

        if self.stock < cantidad:
            raise StockInsuficiente(
                f"Stock insuficiente. Disponible: {self.stock}, solicitado: {cantidad}."
            )

        self.stock -= cantidad