import tkinter as tk
from tkinter import messagebox


class LoginView:
    """Ventana principal de inicio de sesión."""

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de acceso")
        self.root.geometry("420x350")
        self.root.configure(bg="#EAF2F8")
        self.root.resizable(False, False)

        self.title_label = tk.Label(
            root, text="INICIAR SESIÓN", font=("Arial", 20, "bold"),
            bg="#EAF2F8", fg="#154360"
        )
        self.title_label.pack(pady=20)

        self.lbl_email = tk.Label(
            root, text="Correo electrónico:", font=("Arial", 11), bg="#EAF2F8"
        )
        self.lbl_email.pack()

        self.entry_email = tk.Entry(root, width=35, font=("Arial", 11))
        self.entry_email.pack(pady=5)

        self.lbl_password = tk.Label(
            root, text="Contraseña:", font=("Arial", 11), bg="#EAF2F8"
        )
        self.lbl_password.pack()

        self.entry_password = tk.Entry(
            root, width=35, font=("Arial", 11), show="*"
        )
        self.entry_password.pack(pady=5)

        self.btn_login = tk.Button(
            root, text="Ingresar", width=20, bg="#2874A6", fg="white",
            font=("Arial", 11, "bold"), cursor="hand2"
        )
        self.btn_login.pack(pady=15)

        self.btn_register = tk.Button(
            root, text="Crear cuenta", width=20, bg="#27AE60", fg="white",
            font=("Arial", 10), cursor="hand2"
        )
        self.btn_register.pack()
        self.entry_email.focus_set()

    def get_data(self):
        return self.entry_email.get().strip(), self.entry_password.get()

    def clear_fields(self):
        self.entry_email.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_email.focus_set()

    def show_message(self, title, message, kind="info"):
        if kind == "error":
            messagebox.showerror(title, message, parent=self.root)
        else:
            messagebox.showinfo(title, message, parent=self.root)
