"""
Vista para la gestión de autos
Incluye tabla, formularios y operaciones CRUD
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from controller.auto_controller import AutoController
from utils.paths import path_manager
from utils.printer import pdf_generator
from utils.image_loader import ImageLoader
from PIL import Image, ImageTk
from pathlib import Path
import os

class AutoView(ctk.CTkFrame):
    """Vista de gestión de autos"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="#F5F7FA")
        
        self.selected_auto = None
        self.selected_image_path = None
        self.selected_row_frame = None  # Para resaltar la fila seleccionada
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Crear componentes
        self.create_header()
        self.create_table()
        self.create_buttons()
        
        # Cargar datos
        self.load_autos()
    
    def create_header(self):
        """Crea el encabezado de la vista"""
        header_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=10)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(2, weight=1)
        
        # Contenido del header con padding
        content_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        content_frame.pack(fill="both", padx=20, pady=15)
        content_frame.grid_columnconfigure(2, weight=1)
        
        # Configuración del grid para el content_frame
        content_frame.grid_columnconfigure(1, weight=1)  # La columna del medio se expande
        
        # Barra de búsqueda
        self.search_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Buscar auto...",
            width=300,
            height=40,
            border_width=1,
            border_color="#E5E7EB",
            fg_color="#F9FAFB",
            corner_radius=8,
            font=ctk.CTkFont(family="Inter", size=13)
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.search_autos)
        
        # Frame para los botones (alineados a la derecha)
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.grid(row=0, column=2, sticky="e")
        
        btn_nuevo = ctk.CTkButton(
            buttons_frame,
            text="➕ Nuevo Auto",
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
        """Crea la tabla de autos"""
        table_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=10)
        table_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(1, weight=1)
        
        headers_frame = ctk.CTkFrame(table_frame, fg_color="#F9FAFB", corner_radius=0, height=45)
        headers_frame.grid(row=0, column=0, sticky="ew")
        headers_frame.grid_propagate(False)
        
        headers = ["Imagen", "ID", "Marca", "Modelo", "Año", "Color", "Transmisión", "Precio", "Acciones"]
        weights = [2, 1, 2, 2, 1, 2, 2, 2, 1]
        
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
        
        # Contenedor con scroll
        self.table_scroll = ctk.CTkScrollableFrame(table_frame, fg_color="#FFFFFF")
        self.table_scroll.grid(row=1, column=0, sticky="nsew")
        self.table_scroll.grid_columnconfigure(0, weight=1)
    
    def create_buttons(self):
        """Crea los botones de acción"""
        # Los botones ahora están en el encabezado
        pass
    
    def load_autos(self):
        """Carga los autos en la tabla"""
        # Limpiar tabla
        for widget in self.table_scroll.winfo_children():
            widget.destroy()
        
        # Obtener autos
        success, result = AutoController.obtener_todos()
        
        if not success:
            messagebox.showerror("Error", result)
            return
        
        # Mostrar autos
        for i, auto in enumerate(result):
            row_frame = ctk.CTkFrame(
                self.table_scroll,
                fg_color="#FFFFFF" if i % 2 == 0 else "#F9FAFB",
                corner_radius=0,
                height=70
            )
            row_frame.grid(row=i, column=0, sticky="ew", pady=1)
            row_frame.grid_propagate(False)
            row_frame.grid_columnconfigure(0, weight=1)
            
            # Configurar cursor para toda la fila
            row_frame.configure(cursor="hand2")
            
            # Aplicar eventos de clic a toda la fila y sus hijos
            self.bind_click_recursive(row_frame, auto, row_frame)
            
            # Eventos hover
            row_frame.bind("<Enter>", lambda e, rf=row_frame: rf.configure(fg_color="#DBEAFE") if rf != self.selected_row_frame else None)
            row_frame.bind("<Leave>", lambda e, rf=row_frame, idx=i: rf.configure(
                fg_color="#BFDBFE" if rf == self.selected_row_frame else ("#FFFFFF" if idx % 2 == 0 else "#F9FAFB")
            ))
            
            # Contenedor principal de la fila
            data_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            data_frame.pack(fill="both", expand=True, padx=10, pady=5)
            
            weights = [2, 1, 2, 2, 1, 2, 2, 2, 1]
            
            # Configurar columnas del data_frame
            for col, weight in enumerate(weights):
                data_frame.grid_columnconfigure(col, weight=weight)
            
            # Celda para imagen
            img_cell = ctk.CTkFrame(data_frame, fg_color="transparent", height=60)
            img_cell.grid(row=0, column=0, sticky="nsew", padx=5)
            img_cell.grid_propagate(False)
            
            # Imagen del auto centrada
            img_frame = ctk.CTkFrame(img_cell, fg_color="#F3F4F6", width=60, height=60, corner_radius=8)
            img_frame.place(relx=0.5, rely=0.5, anchor="center")
            img_frame.pack_propagate(False)
            
            # Cargar imagen desde URL de Cloudinary (optimizada con caché)
            imagen_cargada = None
            if auto.get('imagen'):  # La columna 'imagen' ahora contiene la URL de Cloudinary
                # Usar caché para evitar descargas repetidas
                imagen_cargada = ImageLoader.load_from_url(auto['imagen'], size=(50, 50), use_cache=True)
            
            if imagen_cargada:
                try:
                    photo = ImageTk.PhotoImage(imagen_cargada)
                    img_label = ctk.CTkLabel(img_frame, image=photo, text="")
                    img_label.image = photo
                    img_label.pack(expand=True)
                except Exception:
                    img_label = ctk.CTkLabel(img_frame, text="🚗", font=ctk.CTkFont(size=20))
                    img_label.pack(expand=True)
            else:
                img_label = ctk.CTkLabel(img_frame, text="🚗", font=ctk.CTkFont(size=20))
                img_label.pack(expand=True)
            
            # Resto de datos
            values = [
                auto['id_auto'],
                auto['marca'],
                auto['modelo'],
                auto['anio'],
                auto['color'],
                auto['transmision'],
                f"${auto['precio']:,.2f}"
            ]
            
            # Crear celdas centradas para los datos
            for j, value in enumerate(values):
                cell_frame = ctk.CTkFrame(data_frame, fg_color="transparent", height=60)
                cell_frame.grid(row=0, column=j+1, sticky="nsew", padx=5)
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
            actions_frame = ctk.CTkFrame(data_frame, fg_color="transparent", height=60)
            actions_frame.grid(row=0, column=len(values)+1, sticky="nsew", padx=5)
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
                command=lambda a=auto: self.show_form(mode="editar", auto=a)
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
            icon_edit_label.bind("<Button-1>", lambda e, a=auto: self.show_form(mode="editar", auto=a))
            
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
                command=lambda a=auto: self.eliminar_auto(a)
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
            icon_delete_label.bind("<Button-1>", lambda e, a=auto: self.eliminar_auto(a))
    
    def bind_click_recursive(self, widget, auto, row_frame):
        """Vincula eventos de clic a un widget y todos sus hijos recursivamente"""
        # Excluir botones de acción del binding recursivo
        widget_class = widget.winfo_class()
        if 'Button' in widget_class:
            return
        
        # Vincular el evento de clic
        widget.bind("<Button-1>", lambda e: self.select_auto(auto, row_frame))
        
        # Aplicar recursivamente a todos los hijos
        for child in widget.winfo_children():
            self.bind_click_recursive(child, auto, row_frame)
    
    def select_auto(self, auto, row_frame=None):
        """Selecciona un auto de la tabla con resaltado visual"""
        # Restaurar color de la fila previamente seleccionada
        if self.selected_row_frame:
            # Obtener el índice de la fila para saber qué color usar
            try:
                idx = list(self.table_scroll.winfo_children()).index(self.selected_row_frame)
                self.selected_row_frame.configure(fg_color="#FFFFFF" if idx % 2 == 0 else "#F9FAFB")
            except:
                pass
        
        # Seleccionar el nuevo auto
        self.selected_auto = auto
        self.selected_row_frame = row_frame
        
        # Resaltar la nueva fila seleccionada
        if row_frame:
            row_frame.configure(fg_color="#BFDBFE")  # Azul claro persistente
        
        print(f"✓ Auto seleccionado: {auto['marca']} {auto['modelo']} (ID: {auto['id_auto']})")
    
    def search_autos(self, event=None):
        """Busca autos por criterio"""
        criterio = self.search_entry.get().strip()
        
        if not criterio:
            self.load_autos()
            return
        
        # Limpiar tabla
        for widget in self.table_scroll.winfo_children():
            widget.destroy()
        
        # Buscar autos
        success, result = AutoController.buscar_autos(criterio)
        
        if not success:
            messagebox.showerror("Error", result)
            return
        
        # Mostrar resultados
        for i, auto in enumerate(result):
            row_frame = ctk.CTkFrame(
                self.table_scroll,
                fg_color="#FFFFFF" if i % 2 == 0 else "#F9FAFB",
                corner_radius=0
            )
            row_frame.grid(row=i, column=0, sticky="ew", pady=1)
            row_frame.grid_columnconfigure(0, weight=1)
            
            row_frame.bind("<Button-1>", lambda e, a=auto: self.select_auto(a))
            row_frame.bind("<Enter>", lambda e, rf=row_frame: rf.configure(fg_color="#DBEAFE"))
            row_frame.bind("<Leave>", lambda e, rf=row_frame, idx=i: rf.configure(
                fg_color="#FFFFFF" if idx % 2 == 0 else "#F9FAFB"
            ))
            
            data_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            data_frame.pack(fill="x", padx=5, pady=8)
            
            weights = [1, 2, 2, 1, 2, 2, 2, 2]
            values = [
                auto['id_auto'],
                auto['modelo'],
                auto['anio'],
                auto['color'],
                auto['transmision'],
                auto['combustible'],
                f"${auto['precio']:,.2f}"
            ]
            
            for j, (value, weight) in enumerate(zip(values, weights)):
                data_frame.grid_columnconfigure(j, weight=weight)
                label = ctk.CTkLabel(
                    data_frame,
                    text=str(value),
                    font=ctk.CTkFont(family="Inter", size=12),
                    text_color="#1F2937"
                )
                label.grid(row=0, column=j, padx=10, sticky="w")
                label.bind("<Button-1>", lambda e, a=auto: self.select_auto(a))
    
    def show_form_nuevo(self):
        """Muestra el formulario para crear un nuevo auto"""
        self.show_form(mode="nuevo")
    
    def show_form_editar(self):
        """Muestra el formulario para editar un auto"""
        if not self.selected_auto:
            messagebox.showwarning("Advertencia", "Debe seleccionar un auto para editar")
            return
        
        self.show_form(mode="editar", auto=self.selected_auto)
    
    def show_form(self, mode="nuevo", auto=None):
        """Muestra el formulario de auto"""
        form_window = ctk.CTkToplevel(self)
        form_window.title("Nuevo Auto" if mode == "nuevo" else "Editar Auto")
        
        # Calcular tamaño dinámico (80% de la altura de pantalla, máx 750px)
        screen_height = form_window.winfo_screenheight()
        window_height = min(int(screen_height * 0.8), 750)
        window_width = 650
        
        form_window.geometry(f"{window_width}x{window_height}")
        form_window.resizable(True, True)  # Permitir redimensionar
        form_window.minsize(600, 500)  # Tamaño mínimo
        
        if mode == "editar" and auto and auto.get('imagen_path'):
            self.selected_image_path = auto['imagen_path']
            if os.path.exists(self.selected_image_path):
                # Cargar la imagen existente después de que se cree el formulario
                form_window.after(100, lambda: self.update_image_preview(self.selected_image_path))
        
        # Centrar ventana
        form_window.transient(self)
        form_window.grab_set()
        
        # Centrar en la pantalla
        form_window.update_idletasks()
        screen_width = form_window.winfo_screenwidth()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        form_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Contenedor principal
        main_frame = ctk.CTkFrame(form_window, fg_color="#F5F7FA")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="Nuevo Auto" if mode == "nuevo" else "Editar Auto",
            font=ctk.CTkFont(family="Inter", size=22, weight="bold"),
            text_color="#1F2937"
        )
        title.pack(pady=(0, 20))
        
        # Formulario
        form_frame = ctk.CTkFrame(main_frame, fg_color="#FFFFFF", corner_radius=10)
        form_frame.pack(fill="both", expand=True)
        
        # Scroll para el formulario
        scroll_frame = ctk.CTkScrollableFrame(form_frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Campos
        fields = [
            ("Marca:", "marca"),
            ("Modelo:", "modelo"),
            ("Año:", "anio"),
            ("Precio:", "precio"),
            ("Color:", "color"),
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
            
            # Prellenar si es edición
            if mode == "editar" and auto:
                entry.insert(0, str(auto[field_name]))
            
            # Enfoque automático en el primer campo
            if i == 0:
                entry.focus()
        
        # Transmisión
        label_trans = ctk.CTkLabel(
            scroll_frame,
            text="Transmisión:",
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color="#6B7280",
            anchor="w"
        )
        label_trans.pack(anchor="w", pady=(10, 5))
        
        transmision_var = ctk.StringVar(value="Manual" if mode == "nuevo" else auto['transmision'])
        transmision_combo = ctk.CTkComboBox(
            scroll_frame,
            values=["Manual", "Automática"],
            variable=transmision_var,
            height=40,
            border_width=1,
            border_color="#E5E7EB",
            fg_color="#F9FAFB",
            button_color="#3B82F6",
            button_hover_color="#2563EB",
            corner_radius=8,
            font=ctk.CTkFont(family="Inter", size=13)
        )
        transmision_combo.pack(fill="x")
        
        # Combustible
        label_comb = ctk.CTkLabel(
            scroll_frame,
            text="Combustible:",
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color="#6B7280",
            anchor="w"
        )
        label_comb.pack(anchor="w", pady=(10, 5))
        
        combustible_var = ctk.StringVar(value="Gasolina" if mode == "nuevo" else auto['combustible'])
        combustible_combo = ctk.CTkComboBox(
            scroll_frame,
            values=["Gasolina", "Diésel", "Eléctrico", "Híbrido"],
            variable=combustible_var,
            height=40,
            border_width=1,
            border_color="#E5E7EB",
            fg_color="#F9FAFB",
            button_color="#3B82F6",
            button_hover_color="#2563EB",
            corner_radius=8,
            font=ctk.CTkFont(family="Inter", size=13)
        )
        combustible_combo.pack(fill="x")
        
        # Imagen
        image_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        image_frame.pack(fill="x", pady=(20, 10))
        
        # Preview de imagen
        self.preview_frame = ctk.CTkFrame(
            image_frame, 
            fg_color="#F3F4F6",
            width=200,
            height=200,
            corner_radius=10
        )
        self.preview_frame.pack(side="left", padx=10)
        self.preview_frame.pack_propagate(False)
        
        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="Vista previa\nde imagen",
            font=ctk.CTkFont(family="Inter", size=12),
            text_color="#9CA3AF"
        )
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Controles de imagen
        controls_frame = ctk.CTkFrame(image_frame, fg_color="transparent")
        controls_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        label_img = ctk.CTkLabel(
            controls_frame,
            text="Imagen del Vehículo:",
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color="#6B7280",
            anchor="w"
        )
        label_img.pack(anchor="w", pady=(0, 10))
        
        self.selected_image_path = None
        
        btn_imagen = ctk.CTkButton(
            controls_frame,
            text="📸 Seleccionar Imagen",
            command=lambda: self.select_image(form_window),
            height=40,
            fg_color="#6366F1",
            hover_color="#4F46E5",
            corner_radius=8,
            font=ctk.CTkFont(family="Inter", size=13)
        )
        btn_imagen.pack(fill="x")
        
        # Botones
        buttons_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        btn_guardar = ctk.CTkButton(
            buttons_frame,
            text="  Guardar",
            command=lambda: self.save_auto(mode, entries, transmision_var, combustible_var, form_window, auto),
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
    
    def select_image(self, parent):
        """Abre el diálogo para seleccionar una imagen"""
        filetypes = (
            ("Imágenes", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("Todos los archivos", "*.*")
        )
        
        filename = filedialog.askopenfilename(
            parent=parent,
            title="Seleccionar imagen del auto",
            filetypes=filetypes
        )
        
        if filename:
            self.selected_image_path = filename
            self.update_image_preview(filename)
    
    def update_image_preview(self, image_path):
        """Actualiza la vista previa de la imagen"""
        try:
            # Limpiar preview anterior
            for widget in self.preview_frame.winfo_children():
                widget.destroy()
                
            # Cargar y mostrar nueva imagen
            img = Image.open(image_path)
            img = img.resize((180, 180), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            preview = ctk.CTkLabel(self.preview_frame, image=photo, text="")
            preview.image = photo
            preview.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")
            self.selected_image_path = None
    
    def save_auto(self, mode, entries, transmision_var, combustible_var, window, auto=None):
        """Guarda el auto (crear o actualizar)"""
        # Obtener valores
        marca = entries['marca'].get().strip()
        modelo = entries['modelo'].get().strip()
        anio = entries['anio'].get().strip()
        precio = entries['precio'].get().strip()
        color = entries['color'].get().strip()
        transmision = transmision_var.get()
        combustible = combustible_var.get()
        
        if mode == "nuevo":
            success, result = AutoController.crear_auto(
                marca, modelo, anio, precio, color, transmision, combustible, self.selected_image_path
            )
        else:
            success, result = AutoController.actualizar_auto(
                auto['id_auto'], marca, modelo, anio, precio, color, transmision, combustible, self.selected_image_path
            )
        
        if success:
            messagebox.showinfo("Éxito", "Auto guardado correctamente")
            window.destroy()
            self.load_autos()
        else:
            messagebox.showerror("Error", result)
    
    def eliminar_auto(self, auto):
        """Elimina el auto seleccionado"""
        
        # Confirmar eliminación
        confirm = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de eliminar el auto {auto['marca']} {auto['modelo']}?"
        )
        
        if not confirm:
            return
        
        # Eliminar imagen de Cloudinary si existe
        if auto.get('cloudinary_id'):
            from utils.cloudinary_service import CloudinaryService
            CloudinaryService.delete_image(auto['cloudinary_id'])
        
        success, result = AutoController.eliminar_auto(auto['id_auto'])
        
        if success:
            messagebox.showinfo("Éxito", "Auto eliminado correctamente")
            self.selected_auto = None
            self.load_autos()
        else:
            messagebox.showerror("Error", result)
    
    def generar_pdf(self):
        """Genera un PDF del auto seleccionado e invoca el diálogo de impresión"""
        if not self.selected_auto:
            messagebox.showwarning("Advertencia", "Debe seleccionar un auto para generar el PDF")
            return
        
        try:
            filename = f"auto_{self.selected_auto['id_auto']}_{self.selected_auto['marca']}_{self.selected_auto['modelo']}.pdf"
            output_path = pdf_generator.generate_auto_report(self.selected_auto, filename)
            
            # Preguntar qué acción desea realizar
            respuesta = messagebox.askyesnocancel(
                "PDF Generado",
                f"PDF generado correctamente en:\n{output_path}\n\n"
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
            # Si es None (Cancelar), no hacer nada
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {str(e)}")
