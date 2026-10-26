class Authentication:

    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self.vista_registro = None

        # Conectar botones con sus funciones.
        self.vista.btn_login.config(
            command=self.iniciar_sesion
        )

        self.vista.btn_register.config(
            command=self.abrir_registro
        )

        self.vista.root.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar_aplicacion
        )

    def iniciar_sesion(self):
        email, password = self.vista.obtener_datos()

        if not email or not password:
            self.vista.mostrar_mensaje(
                "Campos vacíos",
                "Ingresa el correo y la contraseña.",
                "error"
            )
            return

        usuario = self.modelo.validar_usuario(email, password)

        if usuario is not None:
            id_usuario, nombre = usuario

            self.vista.mostrar_mensaje(
                "Acceso correcto",
                f"Bienvenido, {nombre}."
            )

            self.vista.limpiar_campos()

        else:
            self.vista.mostrar_mensaje(
                "Acceso denegado",
                "Correo o contraseña incorrectos.",
                "error"
            )

    def abrir_registro(self):
        # Evita abrir múltiples ventanas de registro.
        if (
            self.vista_registro is not None
            and self.vista_registro.ventana.winfo_exists()
        ):
            self.vista_registro.ventana.lift()
            self.vista_registro.ventana.focus_force()
            return

        self.vista_registro = RegisterView(self.vista.root)

        self.vista_registro.btn_guardar.config(
            command=self.registrar_usuario
        )

        self.vista_registro.ventana.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar_registro
        )

    def registrar_usuario(self):
        nombre, email, password, confirmar = (
            self.vista_registro.obtener_datos()
        )

        if not nombre or not email or not password or not confirmar:
            self.vista_registro.mostrar_mensaje(
                "Campos vacíos",
                "Todos los campos son obligatorios.",
                "error"
            )
            return

        if "@" not in email or "." not in email.split("@")[-1]:
            self.vista_registro.mostrar_mensaje(
                "Correo inválido",
                "Ingresa un correo electrónico válido.",
                "error"
            )
            return

        if password != confirmar:
            self.vista_registro.mostrar_mensaje(
                "Contraseñas diferentes",
                "Las contraseñas no coinciden.",
                "error"
            )
            return

        resultado = self.modelo.registrar_usuario(
            nombre,
            email,
            password
        )

        if resultado == "ok":
            self.vista_registro.mostrar_mensaje(
                "Registro exitoso",
                "El usuario se registró correctamente."
            )

            self.cerrar_registro()

            self.vista.entry_email.delete(0, tk.END)
            self.vista.entry_email.insert(0, email)

        elif resultado == "duplicado":
            self.vista_registro.mostrar_mensaje(
                "Correo existente",
                "Ya existe una cuenta con ese correo.",
                "error"
            )

        else:
            self.vista_registro.mostrar_mensaje(
                "Error",
                "No fue posible registrar el usuario. "
                "Verifica la conexión con MySQL.",
                "error"
            )

    def cerrar_registro(self):
        if self.vista_registro is not None:
            if self.vista_registro.ventana.winfo_exists():
                self.vista_registro.cerrar()

            self.vista_registro = None

    def cerrar_aplicacion(self):
        self.cerrar_registro()
        self.modelo.cerrar()
        self.vista.root.destroy()