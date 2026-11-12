"""Vista principal Tkinter para gestión y exportación del inventario."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

from Controller.products_controller import ProductsController


class DashboardVentana:
    def __init__(self, root, nombre_usuario):
        self.root = root
        self.root.title("Panel Principal - Sistema")
        self.root.geometry("980x680")
        self.root.minsize(900, 620)
        self.nombre_usuario = nombre_usuario
        self.controller = ProductsController(self)
        self._crear_interfaz()

    def _crear_interfaz(self):
        lbl_bienvenida = tk.Label(
            self.root,
            text=f"Bienvenido/a, {self.nombre_usuario}",
            font=("Helvetica", 14, "bold"),
        )
        lbl_bienvenida.pack(pady=15)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        self.frame_inicio = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.frame_inicio, text="Inicio")
        tk.Label(
            self.frame_inicio,
            text="Utiliza las pestañas superiores para navegar por el sistema.",
            font=("Helvetica", 11),
            bg="white",
        ).pack(pady=40)

        self.frame_productos = tk.Frame(self.notebook)
        self.notebook.add(self.frame_productos, text="Inventario de Productos")
        self._crear_seccion_productos()

    def _crear_seccion_productos(self):
        frame_form = tk.LabelFrame(
            self.frame_productos,
            text=" Registrar Producto ",
            font=("Helvetica", 10, "bold"),
        )
        frame_form.pack(side="left", fill="y", padx=15, pady=15, ipadx=10, ipady=10)

        tk.Label(frame_form, text="Nombre:").pack(anchor="w", pady=(5, 2))
        self.entry_prod_nombre = tk.Entry(frame_form, font=("Helvetica", 10))
        self.entry_prod_nombre.pack(fill="x", pady=2)

        tk.Label(frame_form, text="Precio:").pack(anchor="w", pady=(10, 2))
        self.entry_prod_precio = tk.Entry(frame_form, font=("Helvetica", 10))
        self.entry_prod_precio.pack(fill="x", pady=2)

        tk.Label(frame_form, text="Stock:").pack(anchor="w", pady=(10, 2))
        self.entry_prod_stock = tk.Entry(frame_form, font=("Helvetica", 10))
        self.entry_prod_stock.pack(fill="x", pady=2)

        tk.Button(
            frame_form,
            text="Guardar Producto",
            bg="#4CAF50",
            fg="black",
            font=("Helvetica", 10, "bold"),
            command=self._guardar_producto,
        ).pack(fill="x", pady=25)

        frame_tabla = tk.Frame(self.frame_productos)
        frame_tabla.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        # Controles de exportación: el botón llama directamente al Controlador.
        frame_exportacion = ttk.LabelFrame(frame_tabla, text="Exportar inventario")
        frame_exportacion.pack(fill="x", pady=(0, 10))

        ttk.Label(frame_exportacion, text="Formato:").pack(side="left", padx=(10, 5), pady=8)
        self.combo_formato = ttk.Combobox(
            frame_exportacion,
            values=("CSV", "TXT", "JSON", "PDF"),
            state="readonly",
            width=10,
        )
        self.combo_formato.set("CSV")
        self.combo_formato.pack(side="left", padx=5, pady=8)

        ttk.Button(
            frame_exportacion,
            text="Exportar Reporte",
            command=lambda: self.controller.generar_reporte(self.combo_formato.get()),
        ).pack(side="left", padx=10, pady=8)

        tree_scroll = ttk.Scrollbar(frame_tabla)
        tree_scroll.pack(side="right", fill="y")

        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=("ID", "Nombre", "Precio", "Stock"),
            show="headings",
            yscrollcommand=tree_scroll.set,
        )
        self.tabla.pack(fill="both", expand=True)
        tree_scroll.config(command=self.tabla.yview)

        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Precio", text="Precio ($)")
        self.tabla.heading("Stock", text="Stock")

        self.tabla.column("ID", width=45, anchor="center")
        self.tabla.column("Nombre", width=170, anchor="w")
        self.tabla.column("Precio", width=95, anchor="e")
        self.tabla.column("Stock", width=70, anchor="center")

        self._cargar_productos()

    def _cargar_productos(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        resultados = self.controller.obtener_productos()
        if resultados is None:
            self.mostrar_error(
                "Error de base de datos",
                "No fue posible cargar los productos. Revisa la conexión y la tabla products.",
            )
            return

        for product in resultados:
            self.tabla.insert(
                "",
                "end",
                values=(
                    product["id"],
                    product["nombre"],
                    f"{product['precio']:.2f}",
                    product["stock"],
                ),
            )

    def _guardar_producto(self):
        nombre = self.entry_prod_nombre.get().strip()
        precio_texto = self.entry_prod_precio.get().strip()
        stock_texto = self.entry_prod_stock.get().strip()

        if not nombre or not precio_texto or not stock_texto:
            self.mostrar_advertencia(
                "Campos vacíos",
                "Por favor completa todos los campos del producto.",
            )
            return

        try:
            precio = float(precio_texto)
            stock = int(stock_texto)
            if precio < 0 or stock < 0:
                raise ValueError
        except ValueError:
            self.mostrar_error(
                "Error de formato",
                "El precio debe ser un número igual o mayor que cero y el stock un entero no negativo.",
            )
            return

        if self.controller.guardar_producto(nombre, precio, stock):
            self.mostrar_exito("Éxito", "Producto registrado correctamente.")
            self.entry_prod_nombre.delete(0, tk.END)
            self.entry_prod_precio.delete(0, tk.END)
            self.entry_prod_stock.delete(0, tk.END)
            self._cargar_productos()
        else:
            self.mostrar_error(
                "Error",
                "No se pudo registrar el producto en la base de datos.",
            )

    def solicitar_ruta_exportacion(self, formato, extension):
        formato = str(formato).strip().upper()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return filedialog.asksaveasfilename(
            parent=self.root,
            title="Guardar reporte de productos",
            initialfile=f"reporte_productos_{timestamp}{extension}",
            defaultextension=extension,
            filetypes=[(f"Archivo {formato}", f"*{extension}"), ("Todos los archivos", "*.*")],
        )

    @staticmethod
    def mostrar_error(titulo, mensaje):
        messagebox.showerror(titulo, mensaje)

    @staticmethod
    def mostrar_advertencia(titulo, mensaje):
        messagebox.showwarning(titulo, mensaje)

    @staticmethod
    def mostrar_exito(titulo, mensaje):
        messagebox.showinfo(titulo, mensaje)
