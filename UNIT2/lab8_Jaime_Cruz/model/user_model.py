import hashlib
import hmac
import secrets
import mysql.connector
from mysql.connector import Error


class UserModel:
    """Acceso a datos y reglas de usuario. Las contraseñas se guardan con hash."""

    ITERATIONS = 310_000

    def __init__(self, database_connection):
        self.database = database_connection

    @classmethod
    def _hash_password(cls, password, salt=None):
        salt = salt or secrets.token_bytes(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, cls.ITERATIONS
        )
        return f"pbkdf2_sha256${cls.ITERATIONS}${salt.hex()}${digest.hex()}"

    @classmethod
    def _verify_password(cls, password, stored):
        try:
            algorithm, iterations, salt_hex, digest_hex = stored.split("$")
            if algorithm != "pbkdf2_sha256":
                return False
            digest = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                bytes.fromhex(salt_hex),
                int(iterations),
            )
            return hmac.compare_digest(digest.hex(), digest_hex)
        except (ValueError, TypeError):
            return False

    def register_user(self, name, email, password):
        connection = self.database.connect()
        if connection is None:
            return "error"

        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO users (nombre, email, password_hash) VALUES (%s, %s, %s)",
                (name, email.lower(), self._hash_password(password)),
            )
            connection.commit()
            return "ok"
        except mysql.connector.IntegrityError:
            connection.rollback()
            return "duplicate"
        except Error as error:
            connection.rollback()
            print(f"Error al registrar usuario: {error}")
            return "error"
        finally:
            if cursor is not None:
                cursor.close()
            connection.close()

    def authenticate_user(self, email, password):
        connection = self.database.connect()
        if connection is None:
            return None

        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, nombre, password_hash FROM users WHERE email = %s",
                (email.lower(),),
            )
            row = cursor.fetchone()
            if row is not None and self._verify_password(password, row[2]):
                return row[0], row[1]
            return None
        except Error as error:
            print(f"Error al validar usuario: {error}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
            connection.close()

    def close(self):
        # Las conexiones se abren y cierran dentro de cada operación.
        pass
