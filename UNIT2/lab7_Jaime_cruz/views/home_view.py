import tkinter as tk
from tkinter import ttk, messagebox
from Model.products_model import Producto

class DashboardVentana:
    def __init__(self, root, nombre_usuario):
        self.root = root
        self.root.title("Panel Principal - Sistema")
        self.root.geometry("900x650")
        self.root.resizable(False, False)

        self.nombre_usuario = nombre_usuario
        self._crear_interfaz()

    def _crear_interfaz(self):
        # Encabezado
        lbl_bienvenida = tk.Label(
            self.root, 
            text=f"Bienvenido/a, {self.nombre_usuario}", 
            font=("Helvetica", 14, "bold")
        )
        lbl_bienvenida.pack(pady=15)

        # contenedor principal con pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # pestaña 1: Inicio
        self.frame_inicio = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.frame_inicio, text="Inicio")
        
        lbl_info = tk.Label(
            self.frame_inicio, 
            text="Utiliza las pestañas superiores para navegar por el sistema.", 
            font=("Helvetica", 11), 
            bg="white"
        )
        lbl_info.pack(pady=40)

        # pestaña 2: Gestión de Productos
        self.frame_productos = tk.Frame(self.notebook)
        self.notebook.add(self.frame_productos, text="Inventario de Productos")
        
        self._crear_seccion_productos()

    def _crear_seccion_productos(self):
        #  Formulario de Registro - izquierda 
        frame_form = tk.LabelFrame(self.frame_productos, text=" Registrar Producto ", font=("Helvetica", 10, "bold"))
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

        btn_guardar = tk.Button(
            frame_form, 
            text="Guardar Producto", 
            bg="#4CAF50", 
            fg="black", 
            font=("Helvetica", 10, "bold"),
            command=self._guardar_producto
        )
        btn_guardar.pack(fill="x", pady=25)

        #  Tabla (Treeview, intruccion para generar tabla en tkinter) - derecha 
        frame_tabla = tk.Frame(self.frame_productos)
        frame_tabla.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        # Scrollbar para la tabla
        tree_scroll = ttk.Scrollbar(frame_tabla)
        tree_scroll.pack(side="right", fill="y")

        # Tabla
        self.tabla = ttk.Treeview(
            frame_tabla, 
            columns=("ID", "Nombre", "Precio", "Stock"), 
            show="headings",
            yscrollcommand=tree_scroll.set
        )
        self.tabla.pack(fill="both", expand=True)
        tree_scroll.config(command=self.tabla.yview)

        # Definir columnas
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Precio", text="Precio ($)")
        self.tabla.heading("Stock", text="Stock")

        # Ajustar anchos de columnas
        self.tabla.column("ID", width=40, anchor="center")
        self.tabla.column("Nombre", width=140, anchor="w")
        self.tabla.column("Precio", width=80, anchor="e")
        self.tabla.column("Stock", width=60, anchor="center")

        # Cargar los datos iniciales en la tabla
        self._cargar_productos()

    def _cargar_productos(self):
        #Limpia la tabla y carga los registros actuales desde la base de datos.
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        prod_obj = Producto()
        resultados = prod_obj.obtener_todos()

        if resultados:
            for p in resultados:
                self.tabla.insert("", "end", values=(p['id'], p['nombre'], f"{p['precio']:.2f}", p['stock']))

    def _guardar_producto(self):
        nombre = self.entry_prod_nombre.get().strip()
        precio_str = self.entry_prod_precio.get().strip()
        stock_str = self.entry_prod_stock.get().strip()

        if not nombre or not precio_str or not stock_str:
            messagebox.showwarning("Campos Vacíos", "Por favor completa todos los campos del producto.")
            return

        try:
            precio = float(precio_str)
            stock = int(stock_str)
        except ValueError:
            messagebox.showerror("Error de Formato", "El precio debe ser un número decimal y el stock un número entero.")
            return

        # Instanciar modelo y guardar
        nuevo_prod = Producto(nombre=nombre, precio=precio, stock=stock)
        if nuevo_prod.guardar():
            messagebox.showinfo("Éxito", "Producto registrado correctamente.")
            self.entry_prod_nombre.delete(0, tk.END)
            self.entry_prod_precio.delete(0, tk.END)
            self.entry_prod_stock.delete(0, tk.END)
            self._cargar_productos()  # reload table
        else:
            messagebox.showerror("Error", "No se pudo registrar el producto en la base de datos.")