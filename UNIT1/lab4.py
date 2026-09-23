class Producto:
    def __init__(self, nombre, precio, tipo):
        self.__nombre = nombre
        self.__precio = precio
        self.__tipo = tipo

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        if nombre != "":
            self.__nombre = nombre

    def get_precio(self):
        return self.__precio

    def set_precio(self, precio):
        if precio >= 0:
            self.__precio = precio

    def get_tipo(self):
        return self.__tipo

    def set_tipo(self, tipo):
        self.__tipo = tipo


class Pedido:
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.productos = []
        self.estado = "CREADO"

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def calcular_total(self):
        total = 0

        for producto in self.productos:

            if producto.tipo == "electronico":
                total += producto.precio * 1.16

            elif producto.tipo == "ropa":
                total += producto.precio * 1.08

            elif producto.tipo == "alimento":
                total += producto.precio * 1.00

        return total

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def mostrar_pedido(self):
        print(f"\nPedido #{self.numero}")
        print(f"Cliente: {self.cliente}")
        print(f"Estado: {self.estado}")

        print("\nProductos:")

        for producto in self.productos:
            print(
                f"- {producto.nombre}: "
                f"${producto.precio:.2f}"
            )

        print(f"\nTotal: ${self.calcular_total():.2f}")


# main program

pedido = Pedido(1001, "Ana")

pedido.agregar_producto(
    Producto("Laptop", 15000, "electronico")
)

pedido.agregar_producto(
    Producto("Playera", 500, "ropa")
)

pedido.agregar_producto(
    Producto("Cereal", 100, "alimento")
)

pedido.mostrar_pedido()

pedido.cambiar_estado("ENVIADO")

print("\nNuevo estado:", pedido.estado)