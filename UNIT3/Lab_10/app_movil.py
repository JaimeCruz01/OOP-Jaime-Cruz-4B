"""Lógica de perfiles y suscripciones para la práctica Lab 10."""


class SuscripcionExpiradaError(Exception):
    """Se intenta utilizar una función PRO con una suscripción vencida."""


class PuntosInsuficientesError(Exception):
    """El perfil no tiene gemas suficientes para completar una operación."""


class PerfilMovil:
    """Representa el perfil básico de un usuario de la aplicación móvil."""

    def __init__(self, username, gemas=50, racha_dias=1,
                 notificaciones_activas=True):
        if not isinstance(username, str) or not username.strip():
            raise ValueError("El username debe ser una cadena no vacía.")

        self.username = username.strip()
        self.gemas = gemas
        self.racha_dias = self._validar_entero_no_negativo(
            racha_dias, "racha_dias"
        )

        if not isinstance(notificaciones_activas, bool):
            raise ValueError("notificaciones_activas debe ser un booleano.")
        self.notificaciones_activas = notificaciones_activas

    @staticmethod
    def _validar_entero_positivo(cantidad, nombre="cantidad"):
        """Valida cantidades enteras estrictamente positivas."""
        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise ValueError("{} debe ser un número entero.".format(nombre))
        if cantidad <= 0:
            raise ValueError("{} debe ser estrictamente positiva.".format(nombre))
        return cantidad

    @staticmethod
    def _validar_entero_no_negativo(valor, nombre):
        if isinstance(valor, bool) or not isinstance(valor, int) or valor < 0:
            raise ValueError("{} debe ser un entero mayor o igual a cero.".format(nombre))
        return valor

    @property
    def gemas(self):
        """Saldo de gemas; la propiedad evita asignar saldos negativos."""
        return self._gemas

    @gemas.setter
    def gemas(self, valor):
        self._gemas = self._validar_entero_no_negativo(valor, "gemas")

    def ganar_gemas(self, cantidad: int) -> int:
        """Agrega gemas al saldo y devuelve el nuevo balance."""
        cantidad = self._validar_entero_positivo(cantidad)
        self.gemas += cantidad
        return self.gemas

    def gastar_gemas(self, cantidad: int) -> int:
        """Resta gemas si existe saldo suficiente y devuelve el balance."""
        cantidad = self._validar_entero_positivo(cantidad)
        if cantidad > self.gemas:
            raise PuntosInsuficientesError(
                "Saldo insuficiente: disponibles {}, solicitadas {}.".format(
                    self.gemas, cantidad
                )
            )
        self.gemas -= cantidad
        return self.gemas


class PerfilPro(PerfilMovil):
    """Perfil con suscripción PRO y acceso a descargas sin conexión."""

    def __init__(self, username, meses_suscripcion, gemas=50,
                 racha_dias=1, notificaciones_activas=True):
        super().__init__(username, gemas, racha_dias, notificaciones_activas)

        if (isinstance(meses_suscripcion, bool)
                or not isinstance(meses_suscripcion, int)
                or meses_suscripcion <= 0):
            raise ValueError("La suscripción inicial debe ser de más de cero meses.")

        self.meses_suscripcion = meses_suscripcion
        self.es_pro = True

    def descargar_contenido_offline(self) -> str:
        """Verifica la vigencia PRO y autoriza la descarga sin conexión.

        Este método comprueba el periodo informado en meses_suscripcion; no
        consume meses por descarga. El sistema que gestione el paso del tiempo
        debe actualizar ese atributo cuando corresponda.
        """
        if self.meses_suscripcion <= 0 or not self.es_pro:
            self.meses_suscripcion = 0
            self.es_pro = False
            raise SuscripcionExpiradaError(
                "La suscripción PRO ha expirado. Renueva para descargar contenido."
            )

        return "Descarga de contenido offline autorizada para {}.".format(
            self.username
        )
