import tkinter as tk
from view.register_view import RegisterView


class AuthenticationController:
    """Conecta las vistas con las operaciones del modelo."""

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.register_view = None

        self.view.btn_login.config(command=self.login)
        self.view.btn_register.config(command=self.open_register)
        self.view.root.protocol("WM_DELETE_WINDOW", self.close_application)

    def login(self):
        email, password = self.view.get_data()
        if not email or not password:
            self.view.show_message(
                "Campos vacíos", "Ingresa el correo y la contraseña.", "error"
            )
            return

        user = self.model.authenticate_user(email, password)
        if user is not None:
            user_id, name = user
            self.view.show_message("Acceso correcto", f"¡Bienvenido, {name}!")
            self.view.clear_fields()
        else:
            self.view.show_message(
                "Acceso denegado",
                "Correo o contraseña incorrectos, o no fue posible consultar la base de datos.",
                "error",
            )

    def open_register(self):
        if self.register_view is not None:
            try:
                if self.register_view.window.winfo_exists():
                    self.register_view.window.lift()
                    self.register_view.window.focus_force()
                    return
            except tk.TclError:
                pass

        self.register_view = RegisterView(self.view.root)
        self.register_view.btn_save.config(command=self.register_user)
        self.register_view.window.protocol(
            "WM_DELETE_WINDOW", self.close_register
        )

    def register_user(self):
        name, email, password, confirmation = self.register_view.get_data()

        if not all((name, email, password, confirmation)):
            self.register_view.show_message(
                "Campos vacíos", "Todos los campos son obligatorios.", "error"
            )
            return

        if len(name) > 100:
            self.register_view.show_message(
                "Nombre demasiado largo", "El nombre no debe superar 100 caracteres.", "error"
            )
            return

        if "@" not in email or "." not in email.rsplit("@", 1)[-1] or len(email) > 150:
            self.register_view.show_message(
                "Correo inválido", "Ingresa un correo electrónico válido (máximo 150 caracteres).", "error"
            )
            return

        if len(password) < 8:
            self.register_view.show_message(
                "Contraseña insegura", "Usa una contraseña de al menos 8 caracteres.", "error"
            )
            return

        if password != confirmation:
            self.register_view.show_message(
                "Contraseñas diferentes", "Las contraseñas no coinciden.", "error"
            )
            return

        result = self.model.register_user(name, email, password)
        if result == "ok":
            self.register_view.show_message(
                "Registro exitoso", "El usuario se registró correctamente."
            )
            self.close_register()
            self.view.entry_email.delete(0, tk.END)
            self.view.entry_email.insert(0, email)
        elif result == "duplicate":
            self.register_view.show_message(
                "Correo existente", "Ya existe una cuenta con ese correo.", "error"
            )
        else:
            self.register_view.show_message(
                "Error", "No fue posible registrar el usuario. Revisa MySQL y la tabla users.", "error"
            )

    def close_register(self):
        if self.register_view is not None:
            try:
                if self.register_view.window.winfo_exists():
                    self.register_view.close()
            except tk.TclError:
                pass
            self.register_view = None

    def close_application(self):
        self.close_register()
        self.model.close()
        self.view.root.destroy()
