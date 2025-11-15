-- Script de migración para agregar soporte de Cloudinary
-- Ejecutar este script en tu base de datos MySQL

-- Agregar columna cloudinary_id si no existe
ALTER TABLE autos 
ADD COLUMN IF NOT EXISTS cloudinary_id VARCHAR(255) DEFAULT NULL
AFTER imagen;

-- Modificar columna imagen para almacenar URLs completas
ALTER TABLE autos 
MODIFY COLUMN imagen VARCHAR(500) DEFAULT NULL;

-- Comentarios de las columnas
ALTER TABLE autos 
MODIFY COLUMN imagen VARCHAR(500) DEFAULT NULL COMMENT 'URL de la imagen en Cloudinary',
MODIFY COLUMN cloudinary_id VARCHAR(255) DEFAULT NULL COMMENT 'ID público de la imagen en Cloudinary para eliminación';
