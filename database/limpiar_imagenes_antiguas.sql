-- ============================================
-- Script para limpiar registros antiguos
-- con nombres de archivo en lugar de URLs
-- ============================================

USE venta_autos_db;

-- Opción 1: Establecer NULL en registros con nombres de archivo
-- (no URLs de Cloudinary)
UPDATE autos 
SET imagen = NULL, cloudinary_id = NULL
WHERE imagen IS NOT NULL 
  AND imagen NOT LIKE 'http%';

-- Mostrar registros actualizados
SELECT id_auto, marca, modelo, 
       CASE 
           WHEN imagen IS NULL THEN 'SIN IMAGEN'
           WHEN imagen LIKE 'http%' THEN 'URL CLOUDINARY ✅'
           ELSE 'NOMBRE ARCHIVO ❌'
       END AS estado_imagen,
       cloudinary_id
FROM autos
ORDER BY fecha_registro DESC;

-- Opción 2 (comentada): Si prefieres eliminar registros antiguos
-- DELETE FROM autos 
-- WHERE imagen IS NOT NULL 
--   AND imagen NOT LIKE 'http%';
