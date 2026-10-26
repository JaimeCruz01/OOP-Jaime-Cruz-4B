import tkinter as tk
from tkinter import messagebox


class RegisterView:
    """Ventana secundaria para crear una cuenta."""

    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Registro de usuarios")
        self.window.geometry("420x440")
        self.window.configure(bg="#E8F8F5")
        self.window.resizable(False, False)
        self.window.transient(root)
        self.window.grab_set()

        self.title_label = tk.Label(
            self.window, text="CREAR CUENTA", font=("Arial", 19, "bold"),
            bg="#E8F8F5", fg="#117864"
        )
        self.title_label.pack(pady=18)

        self.lbl_name = tk.Label(
            self.window, text="Nombre completo:", bg="#E8F8F5", font=("Arial", 10)
        )
        self.lbl_name.pack()
        self.entry_name = tk.Entry(self.window, width=35, font=("Arial", 10))
        self.entry_name.pack(pady=4)

        self.lbl_email = tk.Label(
            self.window, text="Correo electrónico:", bg="#E8F8F5", font=("Arial", 10)
        )
        self.lbl_email.pack()
        self.entry_email = tk.Entry(self.window, width=35, font=("Arial", 10))
        self.entry_email.pack(pady=4)

        self.lbl_password = tk.Label(
            self.window, text="Contraseña:", bg="#E8F8F5", font=("Arial", 10)
        )
        self.lbl_password.pack()
        self.entry_password = tk.Entry(
            self.window, width=35, show="*", font=("Arial", 10)
        )
        self.entry_password.pack(pady=4)

        self.lbl_confirmation = tk.Label(
            self.window, text="Confirmar contraseña:", bg="#E8F8F5", font=("Arial", 10)
        )
        self.lbl_confirmation.pack()
        self.entry_confirmation = tk.Entry(
            self.window, width=35, show="*", font=("Arial", 10)
        )
        self.entry_confirmation.pack(pady=4)

        self.btn_save = tk.Button(
            self.window, text="Registrar usuario", width=22, bg="#17A589",
            fg="white", font=("Arial", 10, "bold"), cursor="hand2"
        )
        self.btn_save.pack(pady=12)

        self.btn_cancel = tk.Button(
            self.window, text="Cancelar", width=22, command=self.close, cursor="hand2"
        )
        self.btn_cancel.pack()
        self.entry_name.focus_set()

    def get_data(self):
        return (
            self.entry_name.get().strip(),
            self.entry_email.get().strip(),
            self.entry_password.get(),
            self.entry_confirmation.get(),
        )

    def show_message(self, title, message, kind="info"):
        if kind == "error":
            messagebox.showerror(title, message, parent=self.window)
        else:
            messagebox.showinfo(title, message, parent=self.window)

    def close(self):
        try:
            self.window.grab_release()
        except tk.TclError:
            pass
        self.window.destroy()
