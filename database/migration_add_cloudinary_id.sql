-- Migración para agregar columna cloudinary_id a la tabla autos
-- Esta columna almacenará el public_id de Cloudinary para gestionar las imágenes

USE venta_autos_db;

-- Agregar columna cloudinary_id si no existe
ALTER TABLE autos 
ADD COLUMN IF NOT EXISTS cloudinary_id VARCHAR(255) AFTER imagen;

-- Actualizar el campo imagen para que acepte URLs más largas
ALTER TABLE autos 
MODIFY COLUMN imagen VARCHAR(500);

-- Mostrar estructura actualizada
DESCRIBE autos;
