"""
Servicio para gestión de imágenes en Cloudinary
Implementa subida, eliminación y obtención de URLs de imágenes
"""
import cloudinary
import cloudinary.uploader
import cloudinary.api
from pathlib import Path
import os
from dotenv import load_dotenv

class CloudinaryService:
    """Servicio para operaciones con Cloudinary"""
    
    _initialized = False
    
    @staticmethod
    def initialize():
        """
        Inicializa la configuración de Cloudinary
        Carga las credenciales desde variables de entorno
        """
        if CloudinaryService._initialized:
            return True
        
        try:
            # Cargar variables de entorno
            load_dotenv()
            
            # Obtener credenciales
            cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
            api_key = os.getenv('CLOUDINARY_API_KEY')
            api_secret = os.getenv('CLOUDINARY_API_SECRET')
            
            # Validar que existan las credenciales
            if not all([cloud_name, api_key, api_secret]):
                raise ValueError(
                    "Faltan credenciales de Cloudinary. "
                    "Verifica que el archivo .env contenga CLOUDINARY_CLOUD_NAME, "
                    "CLOUDINARY_API_KEY y CLOUDINARY_API_SECRET"
                )
            
            # Configurar Cloudinary
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret,
                secure=True
            )
            
            CloudinaryService._initialized = True
            return True
            
        except Exception as e:
            print(f"Error al inicializar Cloudinary: {e}")
            return False
    
    @staticmethod
    def upload_image(image_path, folder="autos"):
        """
        Sube una imagen a Cloudinary
        
        Args:
            image_path (str): Ruta local de la imagen
            folder (str): Carpeta en Cloudinary donde se guardará
            
        Returns:
            tuple: (success, url/error_message, public_id)
        """
        if not CloudinaryService.initialize():
            return False, "Error al inicializar Cloudinary", None
        
        try:
            # Validar que el archivo existe
            if not Path(image_path).exists():
                return False, "El archivo de imagen no existe", None
            
            # Subir imagen con optimización de tamaño y calidad
            result = cloudinary.uploader.upload(
                image_path,
                folder=folder,
                resource_type="image",
                transformation=[
                    {'width': 600, 'height': 600, 'crop': 'limit'},
                    {'quality': 'auto:eco'}  # Calidad más baja pero más rápida
                ],
                eager=[
                    {'width': 50, 'height': 50, 'crop': 'fill', 'quality': 'auto:low'}  # Miniatura precargada
                ],
                eager_async=False  # Generar miniaturas inmediatamente
            )
            
            # Extraer información
            url = result.get('secure_url')
            public_id = result.get('public_id')
            
            return True, url, public_id
            
        except Exception as e:
            return False, f"Error al subir imagen: {str(e)}", None
    
    @staticmethod
    def delete_image(public_id):
        """
        Elimina una imagen de Cloudinary
        
        Args:
            public_id (str): ID público de la imagen en Cloudinary
            
        Returns:
            tuple: (success, message)
        """
        if not CloudinaryService.initialize():
            return False, "Error al inicializar Cloudinary"
        
        if not public_id:
            return True, "No hay imagen para eliminar"
        
        try:
            result = cloudinary.uploader.destroy(public_id)
            
            if result.get('result') == 'ok':
                return True, "Imagen eliminada correctamente"
            else:
                return False, f"No se pudo eliminar la imagen: {result}"
                
        except Exception as e:
            return False, f"Error al eliminar imagen: {str(e)}"
    
    @staticmethod
    def get_image_url(public_id, transformations=None):
        """
        Obtiene la URL de una imagen con transformaciones opcionales
        
        Args:
            public_id (str): ID público de la imagen
            transformations (dict): Transformaciones a aplicar (opcional)
            
        Returns:
            str: URL de la imagen
        """
        if not CloudinaryService.initialize():
            return None
        
        try:
            if transformations:
                url = cloudinary.CloudinaryImage(public_id).build_url(**transformations)
            else:
                url = cloudinary.CloudinaryImage(public_id).build_url()
            
            return url
            
        except Exception as e:
            print(f"Error al obtener URL: {e}")
            return None
    
    @staticmethod
    def extract_public_id_from_url(url):
        """
        Extrae el public_id de una URL de Cloudinary
        
        Args:
            url (str): URL completa de Cloudinary
            
        Returns:
            str: public_id o None si no se puede extraer
        """
        if not url:
            return None
        
        try:
            # Formato típico: https://res.cloudinary.com/{cloud_name}/image/upload/v{version}/{public_id}.{format}
            parts = url.split('/')
            
            # Buscar 'upload' en la URL
            if 'upload' in parts:
                upload_index = parts.index('upload')
                # El public_id está después de 'upload' y puede incluir la versión
                public_id_parts = parts[upload_index + 1:]
                
                # Unir las partes y remover la extensión del último elemento
                public_id = '/'.join(public_id_parts)
                
                # Remover versión si existe (formato v1234567890/)
                if public_id.startswith('v') and '/' in public_id:
                    public_id = '/'.join(public_id.split('/')[1:])
                
                # Remover extensión
                if '.' in public_id.split('/')[-1]:
                    last_part = public_id.split('/')[-1]
                    public_id = '/'.join(public_id.split('/')[:-1]) + '/' + last_part.rsplit('.', 1)[0]
                
                return public_id
                
        except Exception as e:
            print(f"Error al extraer public_id: {e}")
        
        return None
