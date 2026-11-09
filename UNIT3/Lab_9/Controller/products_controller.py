"""Controlador de productos e integración polimórfica de exportadores."""
from exporters import create_exporter
from Model.products_model import Producto


class ProductsController:
    def __init__(self, view, model=None):
        self.view = view
        self.model = model or Producto()

    def obtener_productos(self):
        return self.model.obtener_todos()

    def guardar_producto(self, nombre, precio, stock):
        self.model.nombre = nombre
        self.model.precio = precio
        self.model.stock = stock
        # La Vista actual no solicita descripción; se conserva el nombre como descripción inicial.
        self.model.descripcion = nombre
        return self.model.guardar()

    def generar_reporte(self, formato):
        """Obtiene registros y llama a export() sin lógica de formato en el Controlador."""
        try:
            exporter = create_exporter(formato)
        except ValueError as error:
            self.view.mostrar_error("Formato no válido", str(error))
            return False

        productos = self.model.obtener_todos()
        if productos is None:
            self.view.mostrar_error(
                "Error de base de datos",
                "No fue posible consultar login_system.products. Revisa PostgreSQL.",
            )
            return False
        if not productos:
            self.view.mostrar_advertencia(
                "Inventario vacío", "No hay productos registrados para exportar."
            )
            return False

        ruta_archivo = self.view.solicitar_ruta_exportacion(
            formato=formato, extension=exporter.extension
        )
        if not ruta_archivo:
            return False

        try:
            exporter.export(productos, ruta_archivo)
        except Exception as error:
            self.view.mostrar_error("Error de exportación", str(error))
            return False

        self.view.mostrar_exito(
            "Exportación completada",
            f"El reporte se generó correctamente en:\n{ruta_archivo}",
        )
        return True
