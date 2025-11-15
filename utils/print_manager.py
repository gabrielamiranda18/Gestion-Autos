"""
Gestor de Impresión Digital
Maneja la impresión mediante el diálogo nativo del sistema operativo
"""
import platform
import subprocess
import os
import tempfile
from pathlib import Path

# Intentar importar win32 solo en Windows
try:
    if platform.system() == 'Windows':
        import win32print
        import win32api
        WIN32_AVAILABLE = True
    else:
        WIN32_AVAILABLE = False
except ImportError:
    WIN32_AVAILABLE = False
    print("⚠️ pywin32 no disponible. Funcionalidad de impresión limitada en Windows.")


class PrintManager:
    """Gestor de impresión digital multiplataforma"""
    
    @staticmethod
    def get_available_printers():
        """
        Obtiene la lista de impresoras disponibles en el sistema
        
        Returns:
            list: Lista de nombres de impresoras
        """
        try:
            system = platform.system()
            
            if system == 'Windows':
                # Obtener impresoras en Windows
                if WIN32_AVAILABLE:
                    printers = []
                    printer_info = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
                    for printer in printer_info:
                        printers.append(printer[2])  # Nombre de la impresora
                    return printers
                else:
                    return []
            
            elif system == 'Darwin':  # macOS
                # Obtener impresoras en macOS
                result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True)
                printers = []
                for line in result.stdout.split('\n'):
                    if line.startswith('printer'):
                        printer_name = line.split()[1]
                        printers.append(printer_name)
                return printers
            
            else:  # Linux
                # Obtener impresoras en Linux
                result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True)
                printers = []
                for line in result.stdout.split('\n'):
                    if line.startswith('printer'):
                        printer_name = line.split()[1]
                        printers.append(printer_name)
                return printers
                
        except Exception as e:
            print(f"Error al obtener impresoras: {e}")
            return []
    
    @staticmethod
    def get_default_printer():
        """
        Obtiene el nombre de la impresora predeterminada
        
        Returns:
            str: Nombre de la impresora predeterminada
        """
        try:
            system = platform.system()
            
            if system == 'Windows':
                if WIN32_AVAILABLE:
                    return win32print.GetDefaultPrinter()
                else:
                    return None
            elif system == 'Darwin':  # macOS
                result = subprocess.run(['lpstat', '-d'], capture_output=True, text=True)
                return result.stdout.split(':')[-1].strip()
            else:  # Linux
                result = subprocess.run(['lpstat', '-d'], capture_output=True, text=True)
                return result.stdout.split(':')[-1].strip()
                
        except Exception as e:
            print(f"Error al obtener impresora predeterminada: {e}")
            return None
    
    @staticmethod
    def print_pdf_with_dialog(pdf_path):
        """
        Abre el PDF para que el usuario pueda imprimirlo
        En Windows, abre con el visor predeterminado (Edge, Adobe, etc.)
        El usuario puede presionar Ctrl+P o usar Archivo → Imprimir
        
        Args:
            pdf_path (str): Ruta del archivo PDF a imprimir
            
        Returns:
            bool: True si se abrió correctamente
        """
        try:
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                print(f"El archivo no existe: {pdf_path}")
                return False
            
            system = platform.system()
            
            if system == 'Windows':
                # Windows: Abrir con el programa predeterminado
                # El usuario puede usar Ctrl+P para imprimir
                try:
                    os.startfile(str(pdf_path))
                    print(f"✓ PDF abierto. Usa Ctrl+P para imprimir.")
                    return True
                except Exception as e:
                    print(f"Error al abrir PDF: {e}")
                    return False
                
            elif system == 'Darwin':  # macOS
                # macOS: Abrir con Preview
                subprocess.run(['open', '-a', 'Preview', str(pdf_path)])
                return True
                
            else:  # Linux
                # Linux: Abrir con visor PDF
                try:
                    subprocess.run(['evince', str(pdf_path)])
                except FileNotFoundError:
                    try:
                        subprocess.run(['okular', str(pdf_path)])
                    except FileNotFoundError:
                        subprocess.run(['xdg-open', str(pdf_path)])
                return True
                
        except Exception as e:
            print(f"Error al abrir PDF: {e}")
            return False
    
    @staticmethod
    def print_to_printer(pdf_path, printer_name=None, copies=1):
        """
        Envía un PDF directamente a una impresora sin mostrar el diálogo
        
        Args:
            pdf_path (str): Ruta del archivo PDF
            printer_name (str): Nombre de la impresora (None = predeterminada)
            copies (int): Número de copias
            
        Returns:
            bool: True si se envió correctamente
        """
        try:
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                return False
            
            system = platform.system()
            
            if system == 'Windows':
                if not WIN32_AVAILABLE:
                    print("pywin32 no disponible. Usando método alternativo.")
                    return False
                
                if printer_name is None:
                    printer_name = PrintManager.get_default_printer()
                
                # Usar win32api para imprimir
                win32api.ShellExecute(
                    0,
                    "printto",
                    str(pdf_path),
                    f'"{printer_name}"',
                    ".",
                    0
                )
                return True
                
            elif system == 'Darwin':  # macOS
                cmd = ['lpr']
                if printer_name:
                    cmd.extend(['-P', printer_name])
                if copies > 1:
                    cmd.extend(['-#', str(copies)])
                cmd.append(str(pdf_path))
                
                subprocess.run(cmd)
                return True
                
            else:  # Linux
                cmd = ['lpr']
                if printer_name:
                    cmd.extend(['-P', printer_name])
                if copies > 1:
                    cmd.extend(['-#', str(copies)])
                cmd.append(str(pdf_path))
                
                subprocess.run(cmd)
                return True
                
        except Exception as e:
            print(f"Error al imprimir directamente: {e}")
            return False
    
    @staticmethod
    def show_print_preview_dialog(pdf_path):
        """
        Muestra una ventana de vista previa con opciones de impresión
        
        Args:
            pdf_path (str): Ruta del archivo PDF
            
        Returns:
            bool: True si se mostró correctamente
        """
        # Por ahora, delegamos al diálogo del sistema
        return PrintManager.print_pdf_with_dialog(pdf_path)


# Instancia global
print_manager = PrintManager()
