-- Ejecuta este script en MySQL Workbench, phpMyAdmin o la consola de MySQL.
CREATE DATABASE IF NOT EXISTS login_mvc
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE login_mvc;

CREATE TABLE IF NOT EXISTS users (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_email (email)
) ENGINE=InnoDB;
