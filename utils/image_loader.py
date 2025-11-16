"""
Utilidad para cargar imágenes desde URLs (Cloudinary)
Con optimizaciones de rendimiento: caché, URLs optimizadas y carga asíncrona
"""
from PIL import Image
import requests
from io import BytesIO
from pathlib import Path
import hashlib
from threading import Thread
from queue import Queue

class ImageLoader:
    """Clase para cargar y procesar imágenes con caché"""
    
    # Caché en memoria para imágenes
    _cache = {}
    _cache_dir = Path("cache/images")
    
    @staticmethod
    def _init_cache():
        """Inicializa el directorio de caché"""
        ImageLoader._cache_dir.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def _get_cache_key(url, size):
        """Genera una clave única para el caché"""
        return hashlib.md5(f"{url}_{size}".encode()).hexdigest()
    
    @staticmethod
    def _optimize_cloudinary_url(url, width, height):
        """
        Optimiza la URL de Cloudinary para cargar imágenes más pequeñas
        Esto reduce el tamaño de descarga hasta un 90%
        """
        if not url or 'cloudinary.com' not in url:
            return url
        
        try:
            # Insertar transformaciones en la URL de Cloudinary
            # Formato: https://res.cloudinary.com/xxx/image/upload/w_50,h_50,c_fill,q_auto,f_auto/v1/xxx
            parts = url.split('/upload/')
            if len(parts) == 2:
                transformations = f"w_{width},h_{height},c_fill,q_auto:low,f_auto"
                optimized_url = f"{parts[0]}/upload/{transformations}/{parts[1]}"
                return optimized_url
        except Exception as e:
            print(f"Error al optimizar URL: {e}")
        
        return url
    
    @staticmethod
    def load_from_url_async(url, size, callback):
        """
        Carga una imagen de forma asíncrona y ejecuta un callback cuando termina
        
        Args:
            url (str): URL de la imagen
            size (tuple): Tamaño deseado (ancho, alto)
            callback (function): Función a llamar con la imagen cargada
        """
        def _load():
            img = ImageLoader.load_from_url(url, size, use_cache=True)
            if callback:
                callback(img)
        
        thread = Thread(target=_load, daemon=True)
        thread.start()
    
    @staticmethod
    def load_from_url(url, size=(50, 50), use_cache=True):
        """
        Carga una imagen desde una URL con caché y optimización
        
        Args:
            url (str): URL de la imagen
            size (tuple): Tamaño deseado (ancho, alto)
            use_cache (bool): Usar caché de memoria
            
        Returns:
            PIL.Image: Imagen cargada y redimensionada o None si hay error
        """
        if not url:
            return None
        
        # Verificar caché en memoria
        if use_cache:
            cache_key = ImageLoader._get_cache_key(url, size)
            if cache_key in ImageLoader._cache:
                return ImageLoader._cache[cache_key].copy()
        
        try:
            # Optimizar URL de Cloudinary para descargar imagen más pequeña
            optimized_url = ImageLoader._optimize_cloudinary_url(url, size[0], size[1])
            
            # Descargar con timeout corto para no bloquear la UI
            response = requests.get(optimized_url, timeout=3, stream=True)
            response.raise_for_status()
            
            # Cargar imagen
            img = Image.open(BytesIO(response.content))
            
            # Redimensionar solo si es necesario (Cloudinary ya lo hace)
            if img.size != size:
                img = img.resize(size, Image.Resampling.LANCZOS)
            
            # Guardar en caché
            if use_cache:
                ImageLoader._cache[cache_key] = img.copy()
            
            return img
            
        except requests.exceptions.Timeout:
            return None
        except requests.exceptions.RequestException:
            return None
        except Exception:
            return None
    
    @staticmethod
    def load_from_path(path, size=(50, 50)):
        """
        Carga una imagen desde una ruta local
        
        Args:
            path (str): Ruta local de la imagen
            size (tuple): Tamaño deseado (ancho, alto)
            
        Returns:
            PIL.Image: Imagen cargada y redimensionada o None si hay error
        """
        if not path:
            return None
        
        try:
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return img
        except Exception as e:
            print(f"Error al cargar imagen desde ruta: {e}")
            return None
