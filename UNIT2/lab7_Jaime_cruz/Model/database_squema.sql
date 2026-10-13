
CREATE SCHEMA IF NOT EXISTS login_system;

CREATE TABLE IF NOT EXISTS login_system.users (
    id_user INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    passw VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL
);

INSERT INTO login_system.users (username, passw, nombre)
VALUES ('admin', 'admin123', 'Super Admin')
ON CONFLICT (username) DO NOTHING;









