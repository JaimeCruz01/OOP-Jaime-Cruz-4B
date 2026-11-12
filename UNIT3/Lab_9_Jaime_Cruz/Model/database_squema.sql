-- Lab 9: esquema alineado con la base existente en DBeaver.
-- Ejecutar conectado a la misma base de datos que indica el archivo .env.
-- No crea public.products ni elimina/modifica registros existentes.

CREATE SCHEMA IF NOT EXISTS login_system;

CREATE TABLE IF NOT EXISTS login_system.users (
    id_user INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    passw VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL
);

-- La tabla users ya puede existir sin UNIQUE(username). Agregamos la restricción
-- de forma segura para que ON CONFLICT (username) funcione.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conrelid = 'login_system.users'::regclass
          AND conname = 'users_username_unique'
    ) THEN
        IF EXISTS (
            SELECT username
            FROM login_system.users
            GROUP BY username
            HAVING COUNT(*) > 1
        ) THEN
            RAISE EXCEPTION
                'Hay usernames duplicados en login_system.users. Corrígelos antes de crear UNIQUE.';
        END IF;

        ALTER TABLE login_system.users
            ADD CONSTRAINT users_username_unique UNIQUE (username);
    END IF;
END $$;

INSERT INTO login_system.users (username, passw, nombre)
VALUES ('admin', 'admin123', 'Super Admin')
ON CONFLICT (username) DO NOTHING;

-- Estructura de productos conforme a la tabla que ya utiliza el usuario.
CREATE TABLE IF NOT EXISTS login_system.products (
    id_producto INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    precio NUMERIC(12, 2) NOT NULL CHECK (precio >= 0),
    cantidad NUMERIC NOT NULL DEFAULT 0 CHECK (cantidad >= 0),
    descripcion VARCHAR(255)
);

ALTER TABLE login_system.products
    ADD COLUMN IF NOT EXISTS descripcion VARCHAR(255);

CREATE INDEX IF NOT EXISTS idx_login_system_products_nombre
    ON login_system.products (nombre);
