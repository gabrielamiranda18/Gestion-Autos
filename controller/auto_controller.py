"""
Controlador para la gestión de autos
Intermediario entre la vista y el modelo
"""
from model.auto_model import AutoModel
from utils.validators import Validator
from utils.cloudinary_service import CloudinaryService
from pathlib import Path

class AutoController:
    """Controlador para operaciones de autos"""
    
    @staticmethod
    def validar_datos_auto(marca, modelo, anio, precio, color, transmision, combustible):
        """
        Valida los datos de un auto antes de guardar
        
        Returns:
            tuple: (is_valid, error_message)
        """
        # Validar campos requeridos
        valid, msg = Validator.validate_required(marca, "Marca")
        if not valid:
            return False, msg
        
        valid, msg = Validator.validate_required(modelo, "Modelo")
        if not valid:
            return False, msg
        
        valid, msg = Validator.validate_year(anio)
        if not valid:
            return False, msg
        
        valid, msg = Validator.validate_number(precio, "Precio", min_value=0)
        if not valid:
            return False, msg
        
        valid, msg = Validator.validate_required(color, "Color")
        if not valid:
            return False, msg
        
        return True, ""
    
    @staticmethod
    def guardar_imagen(source_path):
        """
        Sube una imagen a Cloudinary
        
        Args:
            source_path (str): Ruta local de la imagen
            
        Returns:
            tuple: (image_url, public_id) o (None, None) si hay error
        """
        if not source_path:
            return None, None
        
        try:
            source = Path(source_path)
            if not source.exists():
                return None, None
            
            # Subir a Cloudinary
            success, url_or_error, public_id = CloudinaryService.upload_image(str(source), folder="gestion-autos/autos")
            
            if success:
                return url_or_error, public_id
            else:
                print(f"Error al subir imagen: {url_or_error}")
                return None, None
                
        except Exception as e:
            print(f"Error al guardar imagen: {e}")
            return None, None
    
    @staticmethod
    def crear_auto(marca, modelo, anio, precio, color, transmision, combustible, imagen_path=None):
        """
        Crea un nuevo auto después de validar los datos
        
        Returns:
            tuple: (success, id_auto/error_message)
        """
        # Validar datos
        valid, msg = AutoController.validar_datos_auto(
            marca, modelo, anio, precio, color, transmision, combustible
        )
        if not valid:
            return False, msg
        
        # Subir imagen a Cloudinary si existe
        imagen_url = None
        cloudinary_id = None
        if imagen_path:
            imagen_url, cloudinary_id = AutoController.guardar_imagen(imagen_path)
        
        # Crear el auto
        return AutoModel.crear_auto(
            marca, modelo, anio, precio, color, transmision, combustible, imagen_url, cloudinary_id
        )
    
    @staticmethod
    def actualizar_auto(id_auto, marca, modelo, anio, precio, color, transmision, combustible, imagen_path=None):
        """
        Actualiza un auto existente después de validar los datos
        
        Returns:
            tuple: (success, message)
        """
        # Validar datos
        valid, msg = AutoController.validar_datos_auto(
            marca, modelo, anio, precio, color, transmision, combustible
        )
        if not valid:
            return False, msg
        
        # Obtener datos actuales del auto para eliminar imagen anterior si existe
        imagen_url = None
        cloudinary_id = None
        
        if imagen_path:
            # Obtener el auto actual
            success_get, auto_actual = AutoModel.obtener_por_id(id_auto)
            
            # Si hay una imagen anterior en Cloudinary, eliminarla
            if success_get and auto_actual.get('cloudinary_id'):
                CloudinaryService.delete_image(auto_actual['cloudinary_id'])
            
            # Subir nueva imagen
            imagen_url, cloudinary_id = AutoController.guardar_imagen(imagen_path)
        
        # Actualizar el auto
        return AutoModel.actualizar_auto(
            id_auto, marca, modelo, anio, precio, color, transmision, combustible, imagen_url, cloudinary_id
        )
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los autos"""
        return AutoModel.obtener_todos()
    
    @staticmethod
    def obtener_por_id(id_auto):
        """Obtiene un auto por ID"""
        return AutoModel.obtener_por_id(id_auto)
    
    @staticmethod
    def eliminar_auto(id_auto):
        """Elimina un auto"""
        return AutoModel.eliminar_auto(id_auto)
    
    @staticmethod
    def buscar_autos(criterio):
        """Busca autos por criterio"""
        return AutoModel.buscar_autos(criterio)
