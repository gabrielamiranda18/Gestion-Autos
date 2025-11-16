"""
Vista para la gestión de ventas
Incluye tabla, formularios y operaciones CRUD
"""
import customtkinter as ctk
from tkinter import messagebox
from controller.venta_controller import VentaController
from controller.auto_controller import AutoController
from controller.cliente_controller import ClienteController
from utils.printer import pdf_generator
from datetime import datetime

class VentaView(ctk.CTkFrame):
    """Vista de gestión de ventas"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="#F4F6F7")
        
        self.selected_venta = None
        self.selected_row_frame = None  # Para resaltar la fila seleccionada
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Crear componentes
        self.create_header()
        self.create_table()
        self.create_buttons()
        
        # Cargar datos
        self.load_ventas()
    
    def create_header(self):
        """Crea el encabezado de la vista"""
        header_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=10)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(2, weight=1)
        
        # Contenido del header con padding
        content_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        content_frame.pack(fill="both", padx=20, pady=15)
        content_frame.grid_columnconfigure(1, weight=1)  # Columna del medio expansible
        
        # Barra de búsqueda
        self.search_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Buscar venta...",
            width=300,
            height=40,
            border_width=1,
            border_color="#E5E7EB",
            fg_color="#F9FAFB",
            corner_radius=8,
            font=ctk.CTkFont(family="Inter", size=13)
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 10))
        
        # Frame para los botones (alineados a la derecha)
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.grid(row=0, column=2, sticky="e")
        
        btn_nuevo = ctk.CTkButton(
            buttons_frame,
            text="➕ Nueva Venta",
            command=self.show_form_nuevo,
            width=130,
            height=40,
            fg_color="#10B981",
            hover_color="#059669",
            corner_radius=8
        )
        btn_nuevo.pack(side="left", padx=(0, 10))
        
        btn_imprimir = ctk.CTkButton(
            buttons_frame,
            text="🖨️ Imprimir",
            command=self.generar_pdf,
            width=130,
            height=40,
            fg_color="#6366F1",
            hover_color="#4F46E5",
            corner_radius=8
        )
        btn_imprimir.pack(side="left", padx=(0, 10))
    
    def create_table(self):
        """Crea la tabla de ventas"""
        table_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=10)
        table_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(1, weight=1)
        
        headers_frame = ctk.CTkFrame(table_frame, fg_color="#F9FAFB", corner_radius=0, height=45)
        headers_frame.grid(row=0, column=0, sticky="ew")
        headers_frame.grid_propagate(False)
        
        headers = ["ID", "Cliente", "Auto", "Fecha", "Monto", "Método de Pago", "Acciones"]
        weights = [1, 3, 3, 2, 2, 2, 1]
        
        # Configurar columnas del header
        for i, weight in enumerate(weights):
            headers_frame.grid_columnconfigure(i, weight=weight)
        
        # Crear encabezados con celdas para alineación perfecta
        for i, header in enumerate(headers):
            header_cell = ctk.CTkFrame(headers_frame, fg_color="transparent", height=45)
            header_cell.grid(row=0, column=i, sticky="nsew", padx=5)
            header_cell.grid_propagate(False)
            
            label = ctk.CTkLabel(
                header_cell,
                text=header,
                font=ctk.CTkFont(family="Inter", size=13, weight="bold"),
                text_color="#1F2937",
                anchor="center"
            )
            label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.table_scroll = ctk.CTkScrollableFrame(table_frame, fg_color="#FFFFFF")
        self.table_scroll.grid(row=1, column=0, sticky="nsew")
        self.table_scroll.grid_columnconfigure(0, weight=1)
    
    def create_buttons(self):
        """Crea los botones de acción"""
        # Los botones ahora están en el encabezado
        pass
    
    def load_ventas(self):
        """Carga las ventas en la tabla"""
        for widget in self.table_scroll.winfo_children():
            widget.destroy()
        
        success, result = VentaController.obtener_todas()
        
        if not success:
            messagebox.showerror("Error", result)
            return
        
        for i, venta in enumerate(result):
            row_frame = ctk.CTkFrame(
                self.table_scroll,
                fg_color="#FFFFFF" if i % 2 == 0 else "#F9FAFB",
                corner_radius=0,
                height=50
            )
            row_frame.grid(row=i, column=0, sticky="ew", pady=1)
            row_frame.grid_propagate(False)
            row_frame.grid_columnconfigure(0, weight=1)
            
            # Configurar cursor para toda la fila
            row_frame.configure(cursor="hand2")
            
            # Aplicar eventos de clic a toda la fila y sus hijos
            self.bind_click_recursive(row_frame, venta, row_frame)
            
            # Eventos hover
            row_frame.bind("<Enter>", lambda e, rf=row_frame: rf.configure(fg_color="#DBEAFE") if rf != self.selected_row_frame else None)
            row_frame.bind("<Leave>", lambda e, rf=row_frame, idx=i: rf.configure(
                fg_color="#BFDBFE" if rf == self.selected_row_frame else ("#FFFFFF" if idx % 2 == 0 else "#F9FAFB")
            ))
            
            data_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            data_frame.pack(fill="both", expand=True, padx=10, pady=5)
            
            weights = [1, 3, 3, 2, 2, 2, 1]
            auto_info = f"{venta['auto_marca']} {venta['auto_modelo']} ({venta['auto_anio']})"
            values = [
                venta['id_venta'],
                venta['cliente_nombre'],
                auto_info,
                str(venta['fecha_venta']),
                f"${venta['monto']:,.2f}",
                venta['metodo_pago']
            ]
            
            # Configurar columnas
            for col, weight in enumerate(weights):
                data_frame.grid_columnconfigure(col, weight=weight)
            
            # Crear celdas centradas para los datos
            for j, value in enumerate(values):
                cell_frame = ctk.CTkFrame(data_frame, fg_color="transparent", height=40)
                cell_frame.grid(row=0, column=j, sticky="nsew", padx=5)
                cell_frame.grid_propagate(False)
                
                label = ctk.CTkLabel(
                    cell_frame,
                    text=str(value),
                    font=ctk.CTkFont(family="Inter", size=12),
                    text_color="#374151",
                    anchor="center"
                )
                label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Frame para botones de acción con diseño profesional
            actions_frame = ctk.CTkFrame(data_frame, fg_color="transparent", height=40)
            actions_frame.grid(row=0, column=len(values), sticky="nsew", padx=5)
            actions_frame.grid_propagate(False)
            
            buttons_container = ctk.CTkFrame(actions_frame, fg_color="transparent")
            buttons_container.place(relx=0.5, rely=0.5, anchor="center")
            
            # Botón Eliminar con diseño moderno
            btn_eliminar = ctk.CTkButton(
                buttons_container,
                text="",
                width=40,
                height=40,
                fg_color="#EF4444",
                hover_color="#DC2626",
                corner_radius=10,
                border_width=0,
                command=lambda v=venta: self.eliminar_venta(v)
            )
            btn_eliminar.pack(side="left", padx=4)
            
            # Ícono de eliminar (papelera) con mejor diseño
            icon_delete_label = ctk.CTkLabel(
                btn_eliminar,
                text="🗑",
                font=ctk.CTkFont(family="Segoe UI Emoji", size=18),
                text_color="#FFFFFF"
            )
            icon_delete_label.place(relx=0.5, rely=0.5, anchor="center")
            icon_delete_label.configure(cursor="hand2")
            icon_delete_label.bind("<Button-1>", lambda e, v=venta: self.eliminar_venta(v))
    
    def bind_click_recursive(self, widget, venta, row_frame):
        """Vincula eventos de clic a un widget y todos sus hijos recursivamente"""
        # Excluir botones de acción del binding recursivo
        widget_class = widget.winfo_class()
        if 'Button' in widget_class:
            return
        
        # Vincular el evento de clic
        widget.bind("<Button-1>", lambda e: self.select_venta(venta, row_frame))
        
        # Aplicar recursivamente a todos los hijos
        for child in widget.winfo_children():
            self.bind_click_recursive(child, venta, row_frame)
    
    def select_venta(self, venta, row_frame=None):
        """Selecciona una venta de la tabla con resaltado visual"""
        # Restaurar color de la fila previamente seleccionada
        if self.selected_row_frame:
            try:
                idx = list(self.table_scroll.winfo_children()).index(self.selected_row_frame)
                self.selected_row_frame.configure(fg_color="#FFFFFF" if idx % 2 == 0 else "#F9FAFB")
            except:
                pass
        
        # Seleccionar la nueva venta
        self.selected_venta = venta
        self.selected_row_frame = row_frame
        
        # Resaltar la nueva fila seleccionada
        if row_frame:
            row_frame.configure(fg_color="#BFDBFE")
        
        print(f"✓ Venta seleccionada: ID {venta['id_venta']} - Cliente: {venta['cliente_nombre']}")
    
    def show_form_nuevo(self):
        """Muestra el formulario para crear una nueva venta"""
        form_window = ctk.CTkToplevel(self)
        form_window.title("Nueva Venta")
        
        # Calcular tamaño dinámico (65% de la altura de pantalla, máx 550px)
        screen_height = form_window.winfo_screenheight()
        window_height = min(int(screen_height * 0.65), 550)
        window_width = 500
        
        form_window.geometry(f"{window_width}x{window_height}")
        form_window.resizable(True, True)  # Permitir redimensionar
        form_window.minsize(450, 400)  # Tamaño mínimo
        
        form_window.transient(self)
        form_window.grab_set()
        
        # Centrar en la pantalla
        form_window.update_idletasks()
        screen_width = form_window.winfo_screenwidth()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        form_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Contenedor principal
        main_frame = ctk.CTkFrame(form_window, fg_color="#F4F6F7")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="Nueva Venta",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#2C3E50"
        )
        title.pack(pady=(0, 20))
        
        # Formulario
        form_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF", corner_radius=10)
        form_frame.pack(fill="both", expand=True)
        
        # Scroll para el formulario
        scroll_frame = ctk.CTkScrollableFrame(form_frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Obtener autos y clientes
        success_autos, autos = AutoController.obtener_todos()
        success_clientes, clientes = ClienteController.obtener_todos()
        
        if not success_autos or not success_clientes:
            messagebox.showerror("Error", "No se pudieron cargar los datos necesarios")
            form_window.destroy()
            return
        
        # Cliente
        label_cliente = ctk.CTkLabel(
            scroll_frame,
            text="Cliente:",
            font=ctk.CTkFont(size=12),
            text_color="#2E2E2E"
        )
        label_cliente.pack(anchor="w", padx=0, pady=(5, 5))
        
        clientes_dict = {f"{c['nombre']} (ID: {c['id_cliente']})": c['id_cliente'] for c in clientes}
        cliente_var = ctk.StringVar()
        cliente_combo = ctk.CTkComboBox(
            scroll_frame,
            values=list(clientes_dict.keys()),
            variable=cliente_var,
            height=35
        )
        cliente_combo.pack(fill="x", padx=0)
        
        # Auto
        label_auto = ctk.CTkLabel(
            scroll_frame,
            text="Auto:",
            font=ctk.CTkFont(size=12),
            text_color="#2E2E2E"
        )
        label_auto.pack(anchor="w", padx=0, pady=(10, 5))
        
        autos_dict = {f"{a['marca']} {a['modelo']} {a['anio']} - ${a['precio']:,.2f}": a['id_auto'] for a in autos}
        auto_var = ctk.StringVar()
        auto_combo = ctk.CTkComboBox(
            scroll_frame,
            values=list(autos_dict.keys()),
            variable=auto_var,
            height=35
        )
        auto_combo.pack(fill="x", padx=0)
        
        # Monto
        label_monto = ctk.CTkLabel(
            scroll_frame,
            text="Monto:",
            font=ctk.CTkFont(size=12),
            text_color="#2E2E2E"
        )
        label_monto.pack(anchor="w", padx=0, pady=(10, 5))
        
        monto_entry = ctk.CTkEntry(scroll_frame, height=35)
        monto_entry.pack(fill="x", padx=0)
        
        # Método de pago
        label_metodo = ctk.CTkLabel(
            scroll_frame,
            text="Método de Pago:",
            font=ctk.CTkFont(size=12),
            text_color="#2E2E2E"
        )
        label_metodo.pack(anchor="w", padx=0, pady=(10, 5))
        
        metodo_var = ctk.StringVar(value="Efectivo")
        metodo_combo = ctk.CTkComboBox(
            scroll_frame,
            values=["Efectivo", "Tarjeta", "Transferencia"],
            variable=metodo_var,
            height=35
        )
        metodo_combo.pack(fill="x", padx=0)
        
        # Fecha
        label_fecha = ctk.CTkLabel(
            scroll_frame,
            text="Fecha (YYYY-MM-DD):",
            font=ctk.CTkFont(size=12),
            text_color="#2E2E2E"
        )
        label_fecha.pack(anchor="w", padx=0, pady=(10, 5))
        
        fecha_entry = ctk.CTkEntry(scroll_frame, height=35)
        fecha_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        fecha_entry.pack(fill="x", padx=0)
        
        # Botones
        buttons_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        btn_guardar = ctk.CTkButton(
            buttons_frame,
            text="Guardar",
            command=lambda: self.save_venta(
                clientes_dict, cliente_var, autos_dict, auto_var,
                monto_entry, metodo_var, fecha_entry, form_window
            ),
            font=ctk.CTkFont(size=14),
            height=40,
            width=120,
            fg_color="#27AE60"
        )
        btn_guardar.pack(side="left", padx=10)
        
        btn_cancelar = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            command=form_window.destroy,
            font=ctk.CTkFont(size=14),
            height=40,
            width=120,
            fg_color="#95A5A6"
        )
        btn_cancelar.pack(side="left", padx=10)
    
    def save_venta(self, clientes_dict, cliente_var, autos_dict, auto_var, monto_entry, metodo_var, fecha_entry, window):
        """Guarda la venta"""
        # Obtener valores
        cliente_key = cliente_var.get()
        auto_key = auto_var.get()
        monto = monto_entry.get().strip()
        metodo_pago = metodo_var.get()
        fecha = fecha_entry.get().strip()
        
        if not cliente_key or not auto_key:
            messagebox.showerror("Error", "Debe seleccionar un cliente y un auto")
            return
        
        id_cliente = clientes_dict[cliente_key]
        id_auto = autos_dict[auto_key]
        
        success, result = VentaController.crear_venta(id_auto, id_cliente, monto, metodo_pago, fecha)
        
        if success:
            # Destruir ventana primero para evitar que se sobreponga
            window.destroy()
            # Recargar datos
            self.load_ventas()
            # Mostrar mensaje después
            messagebox.showinfo("Éxito", "Venta registrada correctamente")
        else:
            messagebox.showerror("Error", result)
    
    def eliminar_venta(self, venta):
        """Elimina la venta seleccionada"""
        
        # Confirmar eliminación
        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de eliminar la venta ID {venta['id_venta']}?"
        )
        
        if not confirm:
            return
        
        success, result = VentaController.eliminar_venta(venta['id_venta'])
        
        if success:
            messagebox.showinfo("Éxito", "Venta eliminada correctamente")
            self.selected_venta = None
            self.load_ventas()
        else:
            messagebox.showerror("Error", result)
    
    def generar_pdf(self):
        """Genera un PDF de la venta seleccionada e invoca el diálogo de impresión"""
        if not self.selected_venta:
            messagebox.showwarning("Advertencia", "Debe seleccionar una venta para generar el PDF")
            return
        
        try:
            filename = f"venta_{self.selected_venta['id_venta']}_comprobante.pdf"
            output_path = pdf_generator.generate_venta_report(self.selected_venta, filename)
            
            # Preguntar qué acción desea realizar
            respuesta = messagebox.askyesnocancel(
                "Comprobante Generado",
                f"Comprobante PDF generado correctamente en:\n{output_path}\n\n"
                "¿Desea abrir el PDF para imprimir?\n\n"
                "Sí = Mostrar diálogo de impresora\n"
                "No = Solo ver el PDF\n"
                "Cancelar = Cerrar este mensaje"
            )
            
            if respuesta is True:  # Sí - Mostrar diálogo de impresora
                from utils.printer_dialog import PrinterDialog
                result, printer = PrinterDialog.show_dialog(self, output_path)
            elif respuesta is False:  # No - Solo ver
                pdf_generator.open_pdf(output_path)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {str(e)}")
