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
        else:
            print("El precio no puede ser negativo.")

    def get_tipo(self):
        return self.__tipo

    def set_tipo(self, tipo):
        if tipo == "electronico" or tipo == "ropa" or tipo == "alimento":
            self.__tipo = tipo
        else:
            print("Tipo de producto no válido.")


class Pedido:
    def __init__(self, numero, cliente):
        self.__numero = numero
        self.__cliente = cliente
        self.__productos = []
        self.__estado = "CREADO"

    def agregar_producto(self, producto):

        if isinstance(producto, Producto):
            self.__productos.append(producto)
        else:
            print("Solo se pueden agregar productos.")

    def get_productos(self):
        return self.__productos.copy()

    def calcular_total(self):
        total = 0

        for producto in self.__productos:

            if producto.get_tipo() == "electronico":
                total += producto.get_precio() * 1.16

            elif producto.get_tipo() == "ropa":
                total += producto.get_precio() * 1.08

            elif producto.get_tipo() == "alimento":
                total += producto.get_precio() * 1.00

        return total

    def cambiar_estado(self, nuevo_estado):

        if (nuevo_estado == "CREADO" or
            nuevo_estado == "ENVIADO" or
            nuevo_estado == "ENTREGADO" or
            nuevo_estado == "CANCELADO"):

            self.__estado = nuevo_estado

        else:
            print("Estado no válido.")

    # Mostrar pedido
    def mostrar_pedido(self):
        print(f"\nPedido #{self.__numero}")
        print(f"Cliente: {self.__cliente}")
        print(f"Estado: {self.__estado}")

        print("\nProductos:")

        for producto in self.__productos:
            print(
                f"- {producto.get_nombre()}: "
                f"${producto.get_precio():.2f}"
            )

        print(f"\nTotal: ${self.calcular_total():.2f}")


pedido = Pedido(1001, "Ana")

pedido.agregar_producto(
    Producto("Laptop", 15000, "electronico")
    print(producto.nombre)
)

pedido.agregar_producto(
    Producto("Playera", 500, "ropa")
)

pedido.agregar_producto(
    Producto("Cereal", 100, "alimento")
)

pedido.mostrar_pedido()

pedido.cambiar_estado("ENVIADO")

print("\nNuevo estado:", "ENVIADO")