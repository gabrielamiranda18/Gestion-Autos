-- Script de creación de base de datos para el sistema de venta de autos
-- Compatible con MySQL 5.7+

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS venta_autos_db;
USE venta_autos_db;

-- Tabla de autos
CREATE TABLE IF NOT EXISTS autos (
    id_auto INT AUTO_INCREMENT PRIMARY KEY,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    anio YEAR NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    color VARCHAR(30),
    transmision ENUM('Manual','Automática') DEFAULT 'Manual',
    combustible ENUM('Gasolina','Diésel','Eléctrico','Híbrido') DEFAULT 'Gasolina',
    imagen VARCHAR(255),
    cloudinary_id VARCHAR(255),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100),
    direccion VARCHAR(150)
);

-- Tabla de ventas
CREATE TABLE IF NOT EXISTS ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_auto INT NOT NULL,
    id_cliente INT NOT NULL,
    fecha_venta DATE DEFAULT (CURRENT_DATE),
    monto DECIMAL(10,2) NOT NULL,
    metodo_pago ENUM('Efectivo','Tarjeta','Transferencia') DEFAULT 'Efectivo',
    FOREIGN KEY (id_auto) REFERENCES autos(id_auto) ON DELETE CASCADE,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE
);

-- Datos de ejemplo (opcional)
INSERT INTO autos (marca, modelo, anio, precio, color, transmision, combustible) VALUES
('Toyota', 'Corolla', 2022, 18500.00, 'Gris', 'Automática', 'Gasolina'),
('Honda', 'Civic', 2021, 21000.00, 'Negro', 'Manual', 'Gasolina'),
('Tesla', 'Model 3', 2023, 45000.00, 'Blanco', 'Automática', 'Eléctrico'),
('Ford', 'Mustang', 2022, 35000.00, 'Rojo', 'Manual', 'Gasolina'),
('Chevrolet', 'Spark', 2020, 12000.00, 'Azul', 'Manual', 'Gasolina');

INSERT INTO clientes (nombre, telefono, correo, direccion) VALUES
('Juan Pérez', '555-1234', 'juan.perez@email.com', 'Calle Principal 123'),
('María García', '555-5678', 'maria.garcia@email.com', 'Avenida Central 456'),
('Carlos López', '555-9012', 'carlos.lopez@email.com', 'Boulevard Norte 789');

INSERT INTO ventas (id_auto, id_cliente, fecha_venta, monto, metodo_pago) VALUES
(1, 1, '2024-01-15', 18500.00, 'Transferencia'),
(2, 2, '2024-01-20', 21000.00, 'Efectivo'),
(5, 3, '2024-02-01', 12000.00, 'Tarjeta');
