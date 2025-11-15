"""
Gestión de conexión a la base de datos MySQL
Compatible con Windows y Linux
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class DatabaseConnection:
    """Clase para gestionar la conexión a MySQL"""
    
    def __init__(self, host=None, user=None, password=None, database=None):
        # Intentar cargar desde variables de entorno, sino usar valores por defecto
        self.host = host or os.getenv('DB_HOST', 'localhost')
        self.user = user or os.getenv('DB_USER', 'root')
        self.password = password or os.getenv('DB_PASSWORD', '')
        self.database = database or os.getenv('DB_NAME', 'venta_autos_db')
        self.connection = None
    
    def connect(self):
        """Establece la conexión con la base de datos"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                return True, "Conexión exitosa"
        except Error as e:
            return False, f"Error al conectar: {str(e)}"
        return False, "No se pudo establecer la conexión"
    
    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """
        Ejecuta una consulta SQL (INSERT, UPDATE, DELETE)
        
        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros para la consulta (tupla)
        
        Returns:
            tuple: (success, message/lastrowid)
        """
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            lastrowid = cursor.lastrowid
            cursor.close()
            return True, lastrowid
        except Error as e:
            return False, f"Error en la consulta: {str(e)}"
    
    def fetch_all(self, query, params=None):
        """
        Ejecuta una consulta SELECT y retorna todos los resultados
        
        Args:
            query: Consulta SQL SELECT
            params: Parámetros para la consulta (tupla)
        
        Returns:
            tuple: (success, results/error_message)
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return True, results
        except Error as e:
            return False, f"Error al obtener datos: {str(e)}"
    
    def fetch_one(self, query, params=None):
        """
        Ejecuta una consulta SELECT y retorna un solo resultado
        
        Args:
            query: Consulta SQL SELECT
            params: Parámetros para la consulta (tupla)
        
        Returns:
            tuple: (success, result/error_message)
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return True, result
        except Error as e:
            return False, f"Error al obtener datos: {str(e)}"

# Instancia global de la conexión
db = DatabaseConnection()
