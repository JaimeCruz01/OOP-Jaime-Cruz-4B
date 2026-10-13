CREATE DATABASE IF NOT EXISTS login_system_db;
USE login_system_db;

CREATE TABLE users {
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    passw VARCHAR(50) NOT NULL,
    nombre VARCHAR(100) NOT NULL
};

INSERT INTO users (username,passw,nombre) VALUES ('admin','admin123','Super Admin');








