"""
Diálogo de Selección de Impresora
Simula el diálogo nativo de Windows para selección de impresora
"""
import customtkinter as ctk
from tkinter import messagebox
import platform

try:
    from utils.print_manager import print_manager
    PRINT_MANAGER_AVAILABLE = True
except:
    PRINT_MANAGER_AVAILABLE = False


class PrinterDialog(ctk.CTkToplevel):
    """Diálogo de selección de impresora personalizado"""
    
    def __init__(self, parent, pdf_path):
        super().__init__(parent)
        
        self.pdf_path = pdf_path
        self.selected_printer = None
        self.result = None
        
        # Configurar ventana
        self.title("Printer")
        self.geometry("350x180")
        self.resizable(False, False)
        
        # Centrar ventana
        self.transient(parent)
        self.grab_set()
        
        # Centrar en pantalla
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        # Crear interfaz
        self.create_widgets()
        
        # Cargar impresoras
        self.load_printers()
    
    def create_widgets(self):
        """Crea los widgets del diálogo"""
        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color="#F0F0F0")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Label "Printer" con icono de ayuda
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        printer_label = ctk.CTkLabel(
            header_frame,
            text="Printer",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#000000",
            anchor="w"
        )
        printer_label.pack(side="left")
        
        # ComboBox de impresoras
        self.printer_combo = ctk.CTkComboBox(
            main_frame,
            values=["Cargando..."],
            height=35,
            border_width=1,
            border_color="#999999",
            fg_color="#FFFFFF",
            button_color="#E1E1E1",
            button_hover_color="#D0D0D0",
            dropdown_fg_color="#FFFFFF",
            font=ctk.CTkFont(size=11),
            dropdown_font=ctk.CTkFont(size=11)
        )
        self.printer_combo.pack(fill="x", pady=(0, 5))
        
        # Label "Ready"
        ready_label = ctk.CTkLabel(
            main_frame,
            text="Ready",
            font=ctk.CTkFont(size=10),
            text_color="#555555",
            anchor="w"
        )
        ready_label.pack(fill="x", pady=(0, 10))
        
        # Link "Printer Properties"
        properties_label = ctk.CTkLabel(
            main_frame,
            text="Printer Properties",
            font=ctk.CTkFont(size=10, underline=True),
            text_color="#0066CC",
            anchor="e",
            cursor="hand2"
        )
        properties_label.pack(fill="x", pady=(0, 15))
        properties_label.bind("<Button-1>", lambda e: self.show_properties())
        
        # Frame de botones
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        # Botón Print
        btn_print = ctk.CTkButton(
            buttons_frame,
            text="Print",
            width=80,
            height=28,
            fg_color="#0078D4",
            hover_color="#006ABC",
            corner_radius=4,
            font=ctk.CTkFont(size=11),
            command=self.on_print
        )
        btn_print.pack(side="right", padx=(5, 0))
        
        # Botón Cancel
        btn_cancel = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            width=80,
            height=28,
            fg_color="#E1E1E1",
            hover_color="#D0D0D0",
            text_color="#000000",
            corner_radius=4,
            font=ctk.CTkFont(size=11),
            command=self.on_cancel
        )
        btn_cancel.pack(side="right")
    
    def load_printers(self):
        """Carga la lista de impresoras disponibles"""
        printers = []
        
        # Intentar obtener impresoras reales
        if PRINT_MANAGER_AVAILABLE:
            printers = print_manager.get_available_printers()
        
        # Si no hay impresoras o no está disponible, usar impresoras por defecto
        if not printers:
            printers = [
                "Microsoft Print to PDF",
                "OneNote (Desktop)",
                "Fax",
                "Microsoft XPS Document Writer"
            ]
        
        # Actualizar combo
        self.printer_combo.configure(values=printers)
        
        # Seleccionar la primera impresora
        if printers:
            self.printer_combo.set(printers[0])
            self.selected_printer = printers[0]
    
    def show_properties(self):
        """Muestra las propiedades de la impresora (simulado)"""
        messagebox.showinfo(
            "Printer Properties",
            f"Propiedades de la impresora:\n{self.printer_combo.get()}\n\n"
            "Esta es una simulación del diálogo de propiedades."
        )
    
    def on_print(self):
        """Acción al presionar Print"""
        self.selected_printer = self.printer_combo.get()
        self.result = "print"
        
        # Mostrar mensaje de simulación
        messagebox.showinfo(
            "Impresión Simulada",
            f"Documento enviado a:\n{self.selected_printer}\n\n"
            "Ahora se abrirá el PDF para que puedas imprimirlo realmente."
        )
        
        # Abrir el PDF
        import os
        if platform.system() == 'Windows':
            os.startfile(self.pdf_path)
        
        self.destroy()
    
    def on_cancel(self):
        """Acción al presionar Cancel"""
        self.result = "cancel"
        self.destroy()
    
    @staticmethod
    def show_dialog(parent, pdf_path):
        """
        Muestra el diálogo de impresora y retorna el resultado
        
        Args:
            parent: Ventana padre
            pdf_path: Ruta del PDF a imprimir
            
        Returns:
            tuple: (resultado, impresora_seleccionada)
        """
        dialog = PrinterDialog(parent, pdf_path)
        parent.wait_window(dialog)
        return dialog.result, dialog.selected_printer
