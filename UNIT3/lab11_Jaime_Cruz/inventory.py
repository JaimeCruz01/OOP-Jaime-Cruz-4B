
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


def main():
    inventario = Inventario()

    try:
        codigo = input("Ingrese el código del producto: ").strip().upper()
        cantidad = int(input("Ingrese la cantidad a retirar: "))

        inventario.retirar(codigo, cantidad)

        print("\nRetiro realizado correctamente.")
        print("Producto:", codigo)
        print("Stock restante:", inventario.productos[codigo].stock)

    except ValueError:
        print("Error: La cantidad debe ser un número entero.")

    except ProductoNoEncontrado as e:
        print(f"Error: {e}")

    except CantidadInvalida as e:
        print(f"Error: {e}")

    except StockInsuficiente as e:
        print(f"Error: {e}")

    except ErrorInventario as e:
        print(f"Error general de inventario: {e}")


if __name__ == "__main__":
    main()
