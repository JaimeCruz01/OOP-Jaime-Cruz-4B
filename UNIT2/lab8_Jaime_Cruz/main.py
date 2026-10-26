import tkinter as tk
from tkinter import messagebox

from controller.database_connection import DatabaseConnection
from controller.authentication_controller import AuthenticationController
from model.user_model import UserModel
from view.login_view import LoginView


def main():
    root = tk.Tk()
    database = DatabaseConnection()
    model = UserModel(database)
    view = LoginView(root)
    AuthenticationController(model, view)

    # Verifica la conexión al iniciar, sin impedir que se abra la interfaz.
    if not database.test_connection():
        messagebox.showwarning(
            "Base de datos",
            "No se pudo conectar con MySQL.\n"
            "Revisa las credenciales y ejecuta database.sql."
        )

    root.mainloop()


if __name__ == "__main__":
    main()
