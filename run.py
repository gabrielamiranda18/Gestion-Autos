#!/usr/bin/env python3
"""
Script de inicio multiplataforma para la aplicación Gestión de Autos
Compatible con Windows, Linux y macOS
"""
import sys
import os
from pathlib import Path

def check_python_version():
    """Verifica que la versión de Python sea compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    required_packages = [
        'customtkinter',
        'mysql.connector',
        'PIL',
        'reportlab',
        'cloudinary',
        'dotenv',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'mysql.connector':
                __import__('mysql.connector')
            elif package == 'PIL':
                __import__('PIL')
            elif package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Faltan dependencias:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print("\n📦 Instala las dependencias con:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    print("✅ Todas las dependencias instaladas")

def check_env_file():
    """Verifica que exista el archivo .env"""
    env_file = Path(__file__).parent / '.env'
    
    if not env_file.exists():
        print("⚠️  Advertencia: No se encontró el archivo .env")
        print("   Para usar Cloudinary, ejecuta: python setup_cloudinary.py")
        return False
    
    print("✅ Archivo .env encontrado")
    return True

def main():
    """Función principal"""
    print("=" * 70)
    print("  SISTEMA DE GESTIÓN DE VENTA DE AUTOS - AutoGest")
    print("=" * 70)
    print()
    
    # Verificaciones
    print("Verificando sistema...")
    check_python_version()
    #check_dependencies()
    check_env_file()
    
    print()
    print("=" * 70)
    print("Iniciando aplicación...")
    print("=" * 70)
    print()
    
    # Importar y ejecutar la aplicación
    try:
        from main import main as app_main
        app_main()
    except KeyboardInterrupt:
        print("\n\n👋 Aplicación cerrada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
