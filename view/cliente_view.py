"""
Vista para la gestión de clientes
Incluye tabla, formularios y operaciones CRUD
"""
import customtkinter as ctk
from tkinter import messagebox
from controller.cliente_controller import ClienteController
from utils.printer import pdf_generator

class ClienteView(ctk.CTkFrame):
    """Vista de gestión de clientes"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="#F4F6F7")
        
        self.selected_cliente = None
        self.selected_row_frame = None  # Para resaltar la fila seleccionada
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Crear componentes
        self.create_header()
        self.create_table()
        self.create_buttons()
        
        # Cargar datos
        self.load_clientes()
    
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
            placeholder_text="Buscar cliente...",
            width=300,
            height=40,
            border_width=1,
            border_color="#E5E7EB",
            fg_color="#F9FAFB",
            corner_radius=8,
            font=ctk.CTkFont(family="Inter", size=13)
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.search_clientes)
        
        # Frame para los botones (alineados a la derecha)
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.grid(row=0, column=2, sticky="e")
        
        btn_nuevo = ctk.CTkButton(
            buttons_frame,
            text="➕ Nuevo Cliente",
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
        """Crea la tabla de clientes"""
        table_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=10)
        table_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(1, weight=1)
        
        headers_frame = ctk.CTkFrame(table_frame, fg_color="#F9FAFB", corner_radius=0, height=45)
        headers_frame.grid(row=0, column=0, sticky="ew")
        headers_frame.grid_propagate(False)
        
        headers = ["ID", "Nombre", "Teléfono", "Correo", "Dirección", "Acciones"]
        weights = [1, 3, 2, 3, 3, 1]
        
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
    
    def load_clientes(self):
        """Carga los clientes en la tabla"""
        for widget in self.table_scroll.winfo_children():
            widget.destroy()
        
        success, result = ClienteController.obtener_todos()
        
        if not success:
            messagebox.showerror("Error", result)
            return
        
        for i, cliente in enumerate(result):
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
            self.bind_click_recursive(row_frame, cliente, row_frame)
            
            # Eventos hover
            row_frame.bind("<Enter>", lambda e, rf=row_frame: rf.configure(fg_color="#DBEAFE") if rf != self.selected_row_frame else None)
            row_frame.bind("<Leave>", lambda e, rf=row_frame, idx=i: rf.configure(
                fg_color="#BFDBFE" if rf == self.selected_row_frame else ("#FFFFFF" if idx % 2 == 0 else "#F9FAFB")
            ))
            
            data_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            data_frame.pack(fill="both", expand=True, padx=10, pady=5)
            
            weights = [1, 3, 2, 3, 3, 1]
            values = [
                cliente['id_cliente'],
                cliente['nombre'],
                cliente['telefono'] or "N/A",
                cliente['correo'] or "N/A",
                cliente['direccion'] or "N/A"
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
            
            # Botón Editar con diseño moderno
            btn_editar = ctk.CTkButton(
                buttons_container,
                text="",
                width=40,
                height=40,
                fg_color="#6366F1",
                hover_color="#4F46E5",
                corner_radius=10,
                border_width=0,
                command=lambda c=cliente: self.show_form(mode="editar", cliente=c)
            )
            btn_editar.pack(side="left", padx=4)
            
            # Ícono de editar (lápiz) con mejor diseño
            icon_edit_label = ctk.CTkLabel(
                btn_editar,
                text="✎",
                font=ctk.CTkFont(family="Segoe UI Symbol", size=18, weight="bold"),
                text_color="#FFFFFF"
            )
            icon_edit_label.place(relx=0.5, rely=0.5, anchor="center")
            icon_edit_label.configure(cursor="hand2")
            icon_edit_label.bind("<Button-1>", lambda e, c=cliente: self.show_form(mode="editar", cliente=c))
            
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
                command=lambda c=cliente: self.eliminar_cliente(c)
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
            icon_delete_label.bind("<Button-1>", lambda e, c=cliente: self.eliminar_cliente(c))
    
    def bind_click_recursive(self, widget, cliente, row_frame):
        """Vincula eventos de clic a un widget y todos sus hijos recursivamente"""
        # Excluir botones de acción del binding recursivo
        widget_class = widget.winfo_class()
        if 'Button' in widget_class:
            return
        
        # Vincular el evento de clic
        widget.bind("<Button-1>", lambda e: self.select_cliente(cliente, row_frame))
        
        # Aplicar recursivamente a todos los hijos
        for child in widget.winfo_children():
            self.bind_click_recursive(child, cliente, row_frame)
    
    def select_cliente(self, cliente, row_frame=None):
        """Selecciona un cliente de la tabla con resaltado visual"""
        # Restaurar color de la fila previamente seleccionada
        if self.selected_row_frame:
            try:
                idx = list(self.table_scroll.winfo_children()).index(self.selected_row_frame)
                self.selected_row_frame.configure(fg_color="#FFFFFF" if idx % 2 == 0 else "#F9FAFB")
            except:
                pass
        
        # Seleccionar el nuevo cliente
        self.selected_cliente = cliente
        self.selected_row_frame = row_frame
        
        # Resaltar la nueva fila seleccionada
        if row_frame:
            row_frame.configure(fg_color="#BFDBFE")
        
        print(f"✓ Cliente seleccionado: {cliente['nombre']} (ID: {cliente['id_cliente']})")
    
    def search_clientes(self, event=None):
        """Busca clientes por criterio"""
        criterio = self.search_entry.get().strip()
        
        if not criterio:
            self.load_clientes()
            return
        
        # Limpiar tabla
        for widget in self.table_scroll.winfo_children():
            widget.destroy()
        
        # Buscar clientes
        success, result = ClienteController.buscar_clientes(criterio)
        
        if not success:
            messagebox.showerror("Error", result)
            return
            
            # Mostrar resultados
            for i, cliente in enumerate(result):
                row_frame = ctk.CTkFrame(
                    self.table_scroll,
                    fg_color="#FFFFFF" if i % 2 == 0 else "#F9FAFB",
                    corner_radius=0,
                    height=50
                )
                row_frame.grid(row=i, column=0, sticky="ew", pady=1)
                row_frame.grid_propagate(False)
                row_frame.grid_columnconfigure(0, weight=1)
                
                data_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
                data_frame.pack(fill="both", expand=True, padx=10, pady=5)
                
                weights = [1, 3, 2, 3, 3, 1]
                values = [
                    cliente['id_cliente'],
                    cliente['nombre'],
                    cliente['telefono'] or "N/A",
                    cliente['correo'] or "N/A",
                    cliente['direccion'] or "N/A"
                ]
                
                # Configurar columnas
                for col, weight in enumerate(weights[:-1]):
                    data_frame.grid_columnconfigure(col, weight=weight, minsize=50)
                
                # Crear celdas
                for j, (value, weight) in enumerate(zip(values, weights[:-1])):
                    cell_frame = ctk.CTkFrame(data_frame, fg_color="transparent", height=35)
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
                actions_frame = ctk.CTkFrame(data_frame, fg_color="transparent", height=35)
                actions_frame.grid(row=0, column=len(values), sticky="nsew", padx=5)
                actions_frame.grid_propagate(False)
                
                buttons_container = ctk.CTkFrame(actions_frame, fg_color="transparent")
                buttons_container.place(relx=0.5, rely=0.5, anchor="center")
                
                # Botón Editar con diseño moderno
                btn_editar = ctk.CTkButton(
                    buttons_container,
                    text="",
                    width=40,
                    height=40,
                    fg_color="#6366F1",
                    hover_color="#4F46E5",
                    corner_radius=10,
                    border_width=0,
                    command=lambda c=cliente: self.show_form(mode="editar", cliente=c)
                )
                btn_editar.pack(side="left", padx=4)
                
                # Ícono de editar (lápiz) con mejor diseño
                icon_edit_label = ctk.CTkLabel(
                    btn_editar,
                    text="✎",
                    font=ctk.CTkFont(family="Segoe UI Symbol", size=18, weight="bold"),
                    text_color="#FFFFFF"
                )
                icon_edit_label.place(relx=0.5, rely=0.5, anchor="center")
                icon_edit_label.configure(cursor="hand2")
                icon_edit_label.bind("<Button-1>", lambda e, c=cliente: self.show_form(mode="editar", cliente=c))
                
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
                    command=lambda c=cliente: self.eliminar_cliente(c)
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
                icon_delete_label.bind("<Button-1>", lambda e, c=cliente: self.eliminar_cliente(c))
            
    def show_form_nuevo(self):
        """Muestra el formulario para crear un nuevo cliente"""
        self.show_form(mode="nuevo")
    
    def show_form_editar(self):
        """Muestra el formulario para editar un cliente"""
        if not self.selected_cliente:
            messagebox.showwarning("Advertencia", "Debe seleccionar un cliente para editar")
            return
        
        self.show_form(mode="editar", cliente=self.selected_cliente)
    
    def show_form(self, mode="nuevo", cliente=None):
        """Muestra el formulario de cliente"""
        form_window = ctk.CTkToplevel(self)
        form_window.title("Nuevo Cliente" if mode == "nuevo" else "Editar Cliente")
        
        # Calcular tamaño dinámico (70% de la altura de pantalla, máx 600px)
        screen_height = form_window.winfo_screenheight()
        window_height = min(int(screen_height * 0.7), 600)
        window_width = 550
        
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
        
        main_frame = ctk.CTkFrame(form_window, fg_color="#F5F7FA")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            main_frame,
            text="Nuevo Cliente" if mode == "nuevo" else "Editar Cliente",
            font=ctk.CTkFont(family="Inter", size=22, weight="bold"),
            text_color="#1F2937"
        )
        title.pack(pady=(0, 20))
        
        form_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF", corner_radius=10)
        form_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        scroll_frame = ctk.CTkScrollableFrame(form_frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        fields = [
            ("Nombre:", "nombre"),
            ("Teléfono:", "telefono"),
            ("Correo:", "correo"),
            ("Dirección:", "direccion"),
        ]
        
        entries = {}
        
        for i, (label_text, field_name) in enumerate(fields):
            label = ctk.CTkLabel(
                scroll_frame,
                text=label_text,
                font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
                text_color="#6B7280",
                anchor="w"
            )
            label.pack(anchor="w", pady=(15 if i == 0 else 10, 5))
            
            entry = ctk.CTkEntry(
                scroll_frame,
                height=40,
                border_width=1,
                border_color="#E5E7EB",
                fg_color="#F9FAFB",
                corner_radius=8,
                font=ctk.CTkFont(family="Inter", size=13)
            )
            entry.pack(fill="x")
            entries[field_name] = entry
            
            if mode == "editar" and cliente:
                value = cliente[field_name] or ""
                entry.insert(0, str(value))
            
            if i == 0:
                entry.focus()
        
        buttons_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        btn_guardar = ctk.CTkButton(
            buttons_frame,
            text="  Guardar",
            command=lambda: self.save_cliente(mode, entries, form_window, cliente),
            font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
            height=45,
            width=140,
            fg_color="#10B981",
            hover_color="#059669",
            corner_radius=10
        )
        btn_guardar.pack(side="left", padx=10)
        
        btn_cancelar = ctk.CTkButton(
            buttons_frame,
            text="  Cancelar",
            command=form_window.destroy,
            font=ctk.CTkFont(family="Inter", size=14),
            height=45,
            width=140,
            fg_color="#6B7280",
            hover_color="#4B5563",
            corner_radius=10
        )
        btn_cancelar.pack(side="left", padx=10)
    
    def save_cliente(self, mode, entries, window, cliente=None):
        """Guarda el cliente (crear o actualizar)"""
        # Obtener valores
        nombre = entries['nombre'].get().strip()
        telefono = entries['telefono'].get().strip()
        correo = entries['correo'].get().strip()
        direccion = entries['direccion'].get().strip()
        
        if mode == "nuevo":
            success, result = ClienteController.crear_cliente(nombre, telefono, correo, direccion)
        else:
            success, result = ClienteController.actualizar_cliente(
                cliente['id_cliente'], nombre, telefono, correo, direccion
            )
        
        if success:
            messagebox.showinfo("Éxito", "Cliente guardado correctamente")
            window.destroy()
            self.load_clientes()
        else:
            messagebox.showerror("Error", result)
    
    def eliminar_cliente(self, cliente):
        """Elimina el cliente seleccionado"""
        # Confirmar eliminación
        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de eliminar al cliente {cliente['nombre']}?"
        )
        
        if not confirm:
            return
        
        success, result = ClienteController.eliminar_cliente(cliente['id_cliente'])
        
        if success:
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
            self.load_clientes()
        else:
            messagebox.showerror("Error", result)
    
    def generar_pdf(self):
        """Genera un PDF con la lista de clientes e invoca el diálogo de impresión"""
        try:
            # Obtener todos los clientes
            success, result = ClienteController.obtener_todos()
            
            if not success:
                messagebox.showerror("Error", f"No se pudieron obtener los clientes: {result}")
                return
            
            clientes = result
            
            filename = "lista_clientes.pdf"
            output_path = pdf_generator.generate_cliente_report(filename, clientes)
            
            # Preguntar qué acción desea realizar
            respuesta = messagebox.askyesnocancel(
                "PDF Generado",
                f"Lista de clientes generada correctamente en:\n{output_path}\n\n"
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
