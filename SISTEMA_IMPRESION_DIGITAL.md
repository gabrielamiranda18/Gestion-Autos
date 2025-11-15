# 🖨️ Sistema de Impresión Digital - AutoGest

## 📋 Descripción General

El sistema de impresión digital implementado en AutoGest permite interactuar con el **Subsistema de Impresión (Spooler)** del sistema operativo para gestionar la impresión de documentos PDF de manera profesional.

## ✨ Características Implementadas

### 1. **Generación de Documentos Imprimibles**
- ✅ Conversión de datos a formato PDF utilizando ReportLab
- ✅ Diseño profesional con tablas, imágenes y estilos personalizados
- ✅ Soporte para fichas de autos, comprobantes de venta y listados de clientes

### 2. **Diálogo de Impresión Nativo del Sistema**
- ✅ Invoca la ventana estándar del sistema operativo Windows/macOS/Linux
- ✅ Permite seleccionar impresoras físicas y virtuales (Microsoft Print to PDF, etc.)
- ✅ Configuración de parámetros: páginas, copias, orientación, calidad

### 3. **Gestión Multiplataforma**
- ✅ **Windows**: Usa `os.startfile()` con verbo 'print' + pywin32 para funciones avanzadas
- ✅ **macOS**: Abre con Preview para mostrar diálogo de impresión
- ✅ **Linux**: Compatible con Evince (GNOME) y Okular (KDE)

### 4. **Flujo de Trabajo Intuitivo**
Cuando el usuario presiona el botón "🖨️ Imprimir":

1. **Genera el PDF** con los datos seleccionados
2. **Muestra diálogo de opciones**:
   - **Sí**: Abre el diálogo nativo de impresión del sistema operativo
   - **No**: Solo abre el PDF para visualización
   - **Cancelar**: Cierra sin hacer nada

## 🔧 Componentes Técnicos

### **Módulo `print_manager.py`**
Gestor central de impresión digital que:

```python
from utils.print_manager import print_manager

# Obtener impresoras disponibles
printers = print_manager.get_available_printers()
# Resultado: ['HP OfficeJet Pro', 'Microsoft Print to PDF', 'Canon Pixma', ...]

# Obtener impresora predeterminada
default = print_manager.get_default_printer()
# Resultado: 'HP OfficeJet Pro'

# Invocar diálogo de impresión
print_manager.print_pdf_with_dialog('output/documento.pdf')
# Abre la ventana nativa del sistema operativo
```

### **Integración en `printer.py`**
El generador de PDFs ahora incluye:

```python
# Generar PDF
output_path = pdf_generator.generate_auto_report(auto_data, 'auto.pdf')

# Opción 1: Solo abrir para ver
pdf_generator.open_pdf(output_path)

# Opción 2: Invocar diálogo de impresión (NUEVO)
pdf_generator.print_pdf(output_path)
```

### **Actualización de Vistas**
Todas las vistas (autos, clientes, ventas) ahora ofrecen:

```python
def generar_pdf(self):
    # Genera el PDF
    output_path = pdf_generator.generate_auto_report(...)
    
    # Pregunta al usuario qué desea hacer
    respuesta = messagebox.askyesnocancel(
        "PDF Generado",
        "¿Desea imprimir el documento?\n\n"
        "Sí = Abrir diálogo de impresión\n"
        "No = Solo ver el PDF\n"
        "Cancelar = Cerrar"
    )
    
    if respuesta is True:  # Imprimir
        pdf_generator.print_pdf(output_path)
    elif respuesta is False:  # Ver
        pdf_generator.open_pdf(output_path)
```

## 🎯 Cómo Funciona el Proceso de Impresión

### **Paso 1: Generar Documento**
El sistema toma los datos del registro seleccionado y genera un PDF profesional:

- **Autos**: Ficha técnica con imagen, marca, modelo, precio, etc.
- **Ventas**: Comprobante con datos del cliente, auto y monto
- **Clientes**: Lista completa de todos los clientes

### **Paso 2: Mostrar Diálogo de Opciones**
Se presenta un cuadro de mensaje con 3 opciones:
- ✅ **Sí**: Imprimir (invoca diálogo del sistema)
- 📄 **No**: Solo ver el PDF
- ❌ **Cancelar**: No hacer nada

### **Paso 3: Invocar Subsistema de Impresión**

#### En Windows:
```python
# Usa os.startfile() con verbo 'print'
os.startfile(pdf_path, 'print')
```
Esto abre el PDF con el visor predeterminado (Adobe Reader, Edge, etc.) que muestra su propio diálogo de impresión con:
- Lista de impresoras disponibles
- Configuración de páginas y copias
- Opciones de calidad y color
- **Microsoft Print to PDF** para guardar como archivo

#### En macOS:
```python
# Abre con Preview
subprocess.run(['open', '-a', 'Preview', pdf_path])
```

#### En Linux:
```python
# Intenta con Evince o Okular
subprocess.run(['evince', '--preview', pdf_path])
```

### **Paso 4: Gestión por el Spooler**
El sistema operativo se encarga de:
1. Poner el trabajo en la **cola de impresión**
2. Traducir el PDF para el modelo específico de impresora
3. Enviar los datos a la impresora física o guardar como archivo

## 📦 Dependencias Instaladas

```txt
pywin32==306  # Solo en Windows
```

Esta librería permite:
- Enumerar impresoras instaladas
- Obtener la impresora predeterminada
- Enviar trabajos directamente al spooler
- Invocar diálogos nativos de Windows

## 🚀 Casos de Uso

### **1. Imprimir Ficha de Auto**
```
Usuario → Selecciona auto → Clic en 🖨️ Imprimir
         ↓
Sistema → Genera PDF → Pregunta "¿Imprimir?"
         ↓
Usuario → Selecciona "Sí"
         ↓
Sistema → Abre diálogo de impresión de Windows
         ↓
Usuario → Selecciona impresora → Configura → Imprime
```

### **2. Guardar Comprobante como PDF Digital**
```
Usuario → Genera comprobante de venta
         ↓
Sistema → Pregunta "¿Imprimir?"
         ↓
Usuario → Selecciona "Sí"
         ↓
Sistema → Abre diálogo de impresión
         ↓
Usuario → Selecciona "Microsoft Print to PDF"
         ↓
Sistema → Guarda como archivo PDF
```

### **3. Solo Ver sin Imprimir**
```
Usuario → Clic en 🖨️ Imprimir
         ↓
Sistema → Pregunta "¿Imprimir?"
         ↓
Usuario → Selecciona "No"
         ↓
Sistema → Abre PDF en visor para ver solamente
```

## 🔍 Ventajas del Sistema Implementado

### **1. Profesionalismo**
- ✅ Interacción con el sistema operativo como aplicaciones enterprise (Word, Excel, etc.)
- ✅ No depende de impresoras específicas
- ✅ Soporte para impresoras virtuales (PDF, XPS, etc.)

### **2. Flexibilidad**
- ✅ Usuario decide qué hacer: imprimir, ver o cancelar
- ✅ Puede seleccionar cualquier impresora instalada
- ✅ Puede guardar como PDF sin necesidad de impresora física

### **3. Multiplataforma**
- ✅ Funciona en Windows, macOS y Linux
- ✅ Usa APIs nativas de cada sistema operativo
- ✅ Fallback inteligente si faltan dependencias

### **4. Control Total**
- ✅ Usuario configura páginas, copias, orientación
- ✅ Puede ver vista previa antes de imprimir
- ✅ Gestión de cola de impresión por el sistema operativo

## 📝 Notas Técnicas

### **Subsistema de Impresión (Spooler)**
El spooler es un gestor de colas que:
- Recibe trabajos de impresión de múltiples aplicaciones
- Los almacena temporalmente
- Los procesa en orden
- Los traduce al lenguaje de cada impresora (PostScript, PCL, etc.)
- Los envía al dispositivo físico o virtual

### **Impresión Digital vs Física**
- **Digital**: Guardar como PDF usando "Microsoft Print to PDF"
- **Física**: Enviar a impresora real (HP, Canon, Epson, etc.)
- **Ambas**: Usan el mismo diálogo y subsistema

### **Formatos Soportados**
- ✅ PDF (generado por ReportLab)
- ✅ PostScript (si la impresora lo soporta)
- ✅ PCL (Printer Command Language)

## 🎉 Resultado Final

Ahora AutoGest ofrece una experiencia de impresión profesional comparable a Microsoft Word u otras aplicaciones enterprise, permitiendo a los usuarios:

1. Generar documentos PDF de calidad
2. Visualizarlos antes de imprimir
3. Invocar el diálogo nativo del sistema operativo
4. Seleccionar entre impresoras físicas y virtuales
5. Configurar todos los parámetros de impresión
6. Guardar como PDF digital sin necesidad de impresora física

---

**Desarrollado para AutoGest - Sistema de Gestión de Venta de Autos**
