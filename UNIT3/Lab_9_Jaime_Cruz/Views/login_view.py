"""Vista de inicio de sesión."""

from pathlib import Path
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

from Model.login_model import User
from Views.home_view import DashboardVentana


class LoginVentana:
    def __init__(self, root):
        self.root = root
        self.root.title("Acceso al Sistema")
        self.root.geometry("350x400")
        self.root.resizable(False, False)
        self._crear_interfaz()

    def _crear_interfaz(self):
        tk.Label(
            self.root,
            text="Iniciar Sesión",
            font=("Helvetica", 16, "bold"),
        ).pack(pady=25)

        image_path = Path(__file__).resolve().parents[1] / "assets" / "icon.png"
        if image_path.is_file():
            try:
                image = Image.open(image_path).resize((75, 75))
                self.img_logo = ImageTk.PhotoImage(image)
                tk.Label(self.root, image=self.img_logo).pack(pady=10)
            except OSError:
                pass

        tk.Label(self.root, text="Usuario:", font=("Helvetica", 10)).pack(
            anchor="w", padx=30, pady=(5, 2)
        )
        self.entry_usuario = tk.Entry(self.root, font=("Helvetica", 11))
        self.entry_usuario.pack(fill="x", padx=30)

        tk.Label(self.root, text="Contraseña:", font=("Helvetica", 10)).pack(
            anchor="w", padx=30, pady=(15, 2)
        )
        self.entry_pass = tk.Entry(self.root, font=("Helvetica", 11), show="*")
        self.entry_pass.pack(fill="x", padx=30)

        tk.Button(
            self.root,
            text="Entrar",
            font=("Helvetica", 11, "bold"),
            bg="#2196F3",
            fg="white",
            cursor="hand2",
            command=self._validar_login,
        ).pack(fill="x", padx=30, pady=30)

    def _validar_login(self):
        usuario_texto = self.entry_usuario.get().strip()
        pass_texto = self.entry_pass.get().strip()

        if not usuario_texto or not pass_texto:
            messagebox.showwarning(
                "Campos vacíos",
                "Por favor ingresa usuario y contraseña.",
            )
            return

        datos_usuario = User(usuario_texto, pass_texto).autenticar()
        if datos_usuario:
            messagebox.showinfo(
                "Bienvenido",
                f"¡Hola {datos_usuario['username']}! Acceso concedido.",
            )
            self._abrir_dashboard(datos_usuario["username"])
        else:
            messagebox.showerror(
                "Error de acceso",
                "Usuario o contraseña incorrectos.",
            )

    def _abrir_dashboard(self, nombre_usuario):
        self.root.destroy()
        root_dashboard = tk.Tk()
        DashboardVentana(root_dashboard, nombre_usuario)
        root_dashboard.mainloop()
