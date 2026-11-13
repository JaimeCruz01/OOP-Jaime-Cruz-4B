from inventory import Inventario
from product import ErrorInventario,ProductoNoEncontrado,CantidadInvalida, StockInsuficiente


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