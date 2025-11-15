"""
Modelo de datos para la tabla de autos
Implementa todas las operaciones CRUD
"""
from model.conexion import db

class AutoModel:
    """Clase para gestionar operaciones CRUD de autos"""
    
    @staticmethod
    def crear_auto(marca, modelo, anio, precio, color, transmision, combustible, imagen_url=None, cloudinary_id=None):
        """
        Crea un nuevo registro de auto
        
        Args:
            imagen_url: URL de la imagen en Cloudinary
            cloudinary_id: ID público de la imagen en Cloudinary
            
        Returns:
            tuple: (success, id_auto/error_message)
        """
        query = """
            INSERT INTO autos (marca, modelo, anio, precio, color, transmision, combustible, imagen, cloudinary_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (marca, modelo, anio, precio, color, transmision, combustible, imagen_url, cloudinary_id)
        return db.execute_query(query, params)
    
    @staticmethod
    def obtener_todos():
        """
        Obtiene todos los autos registrados
        
        Returns:
            tuple: (success, list_of_autos/error_message)
        """
        query = "SELECT * FROM autos ORDER BY fecha_registro DESC"
        return db.fetch_all(query)
    
    @staticmethod
    def obtener_por_id(id_auto):
        """
        Obtiene un auto por su ID
        
        Returns:
            tuple: (success, auto_data/error_message)
        """
        query = "SELECT * FROM autos WHERE id_auto = %s"
        return db.fetch_one(query, (id_auto,))
    
    @staticmethod
    def actualizar_auto(id_auto, marca, modelo, anio, precio, color, transmision, combustible, imagen_url=None, cloudinary_id=None):
        """
        Actualiza los datos de un auto existente
        
        Args:
            imagen_url: URL de la imagen en Cloudinary
            cloudinary_id: ID público de la imagen en Cloudinary
            
        Returns:
            tuple: (success, message)
        """
        if imagen_url and cloudinary_id:
            query = """
                UPDATE autos 
                SET marca=%s, modelo=%s, anio=%s, precio=%s, color=%s, 
                    transmision=%s, combustible=%s, imagen=%s, cloudinary_id=%s
                WHERE id_auto=%s
            """
            params = (marca, modelo, anio, precio, color, transmision, combustible, imagen_url, cloudinary_id, id_auto)
        else:
            query = """
                UPDATE autos 
                SET marca=%s, modelo=%s, anio=%s, precio=%s, color=%s, 
                    transmision=%s, combustible=%s
                WHERE id_auto=%s
            """
            params = (marca, modelo, anio, precio, color, transmision, combustible, id_auto)
        
        return db.execute_query(query, params)
    
    @staticmethod
    def eliminar_auto(id_auto):
        """
        Elimina un auto por su ID
        
        Returns:
            tuple: (success, message)
        """
        query = "DELETE FROM autos WHERE id_auto = %s"
        return db.execute_query(query, (id_auto,))
    
    @staticmethod
    def buscar_autos(criterio):
        """
        Busca autos por marca, modelo o color
        
        Returns:
            tuple: (success, list_of_autos/error_message)
        """
        query = """
            SELECT * FROM autos 
            WHERE marca LIKE %s OR modelo LIKE %s OR color LIKE %s
            ORDER BY fecha_registro DESC
        """
        search_term = f"%{criterio}%"
        return db.fetch_all(query, (search_term, search_term, search_term))
