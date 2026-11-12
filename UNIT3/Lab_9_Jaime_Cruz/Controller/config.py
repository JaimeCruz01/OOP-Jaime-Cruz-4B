"""Configuración de PostgreSQL mediante variables de entorno y archivo .env."""
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env"


def _load_env_file():
    """Carga variables sencillas desde .env sin sobrescribir el entorno."""
    if not ENV_FILE.is_file():
        return
    for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file()

_password = os.getenv("DB_PASSWORD")
if not _password:
    raise RuntimeError(
        "Falta DB_PASSWORD. Crea el archivo .env a partir de .env.example "
        "y configura la contraseña de PostgreSQL."
    )

DB_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": _password,
    "dbname": os.getenv("DB_NAME", "postgres"),
    "port": int(os.getenv("DB_PORT", "5432")),
}
