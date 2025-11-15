# 🌍 Instalación Multiplataforma - AutoGest

Esta aplicación es completamente compatible con **Windows**, **Linux** y **macOS**.

---

## 📋 Requisitos Previos

### Todos los Sistemas:
- Python 3.8 o superior
- MySQL 5.7 o superior
- Conexión a internet (para Cloudinary)

### Windows:
- Python instalado desde [python.org](https://www.python.org/downloads/)
- MySQL instalado desde [mysql.com](https://dev.mysql.com/downloads/installer/)

### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
sudo apt install mysql-server
```

### Linux (Fedora/RHEL):
```bash
sudo dnf install python3 python3-pip
sudo dnf install mysql-server
```

### macOS:
```bash
# Instalar Homebrew si no lo tienes
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python y MySQL
brew install python3
brew install mysql
```

---

## 🚀 Instalación Rápida

### Windows:

1. **Clonar o descargar el proyecto**
2. **Ejecutar el script de inicio:**
   ```cmd
   run.bat
   ```
   
   El script automáticamente:
   - Crea el entorno virtual si no existe
   - Instala las dependencias
   - Inicia la aplicación

### Linux / macOS:

1. **Clonar o descargar el proyecto**
2. **Hacer ejecutable el script:**
   ```bash
   chmod +x run.sh
   ```
3. **Ejecutar el script:**
   ```bash
   ./run.sh
   ```
   
   El script automáticamente:
   - Crea el entorno virtual si no existe
   - Instala las dependencias
   - Inicia la aplicación

---

## 🔧 Instalación Manual

### 1. Crear Entorno Virtual

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar Dependencias

**Todos los sistemas:**
```bash
pip install -r requirements.txt
```

### 3. Configurar MySQL

**Editar credenciales en `.env`:**
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=venta_autos_db
```

### 4. Crear Base de Datos

**Windows (CMD/PowerShell):**
```cmd
mysql -u root -p < database\venta_autos_db.sql
mysql -u root -p < database\migration_cloudinary.sql
```

**Linux/macOS:**
```bash
mysql -u root -p < database/venta_autos_db.sql
mysql -u root -p < database/migration_cloudinary.sql
```

### 5. Configurar Cloudinary

**Todos los sistemas:**
```bash
python setup_cloudinary.py
```

### 6. Ejecutar Aplicación

**Todos los sistemas:**
```bash
python run.py
```

O directamente:
```bash
python main.py
```

---

## 🐧 Instrucciones Específicas para Linux

### Solución de Problemas Comunes:

#### Tkinter no instalado:
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

#### Permisos de MySQL:
```bash
sudo systemctl start mysql
sudo mysql_secure_installation
```

#### Abrir PDFs automáticamente:
```bash
# Instalar visor de PDF
sudo apt install evince  # o xdg-utils
```

---

## 🍎 Instrucciones Específicas para macOS

### Configuración de MySQL:
```bash
# Iniciar MySQL
brew services start mysql

# Configurar seguridad
mysql_secure_installation
```

### Permisos de Seguridad:
Si aparece un mensaje de seguridad al abrir la aplicación:
1. Ve a **Preferencias del Sistema** → **Seguridad y Privacidad**
2. Permite la ejecución de la aplicación

---

## 📁 Estructura de Rutas Multiplataforma

La aplicación usa `pathlib` para rutas, compatible con todos los sistemas:

```python
# Windows: D:\Proyects\Gestion-Autos\output\reporte.pdf
# Linux: /home/user/Gestion-Autos/output/reporte.pdf
# macOS: /Users/user/Gestion-Autos/output/reporte.pdf
```

---

## 🔍 Verificar Instalación

**Todos los sistemas:**
```bash
python run.py
```

El script verificará:
- ✅ Versión de Python
- ✅ Dependencias instaladas
- ✅ Archivo .env configurado
- ✅ Base de datos accesible

---

## 📦 Dependencias por Sistema

### Windows:
- Todas las dependencias se instalan vía pip
- No requiere compiladores adicionales

### Linux:
Algunas dependencias pueden requerir paquetes del sistema:
```bash
sudo apt install python3-dev libmysqlclient-dev  # Ubuntu/Debian
sudo dnf install python3-devel mysql-devel       # Fedora
```

### macOS:
```bash
brew install mysql-client
export PATH="/usr/local/opt/mysql-client/bin:$PATH"
```

---

## 🎨 Interfaz Gráfica

CustomTkinter funciona en todos los sistemas operativos con apariencia nativa:

- **Windows**: Tema Windows moderno
- **Linux**: Tema GTK/Qt según el escritorio
- **macOS**: Tema macOS nativo

---

## 🔐 Variables de Entorno (.env)

El archivo `.env` funciona igual en todos los sistemas:

```env
# Cloudinary
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret

# MySQL
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=venta_autos_db
```

---

## 🚨 Solución de Problemas por Sistema

### Windows:

**Error: "Python no reconocido"**
```cmd
# Agregar Python al PATH durante la instalación
# O usar:
py -3 -m venv venv
```

**Error de permisos:**
```cmd
# Ejecutar como administrador
```

### Linux:

**Error: "Permission denied"**
```bash
chmod +x run.sh
```

**Error: "No module named 'tkinter'"**
```bash
sudo apt install python3-tk
```

**MySQL socket error:**
```bash
sudo systemctl start mysql
```

### macOS:

**Error: "command not found: mysql"**
```bash
brew install mysql
brew services start mysql
```

**Error de certificados SSL:**
```bash
/Applications/Python\ 3.x/Install\ Certificates.command
```

---

## 📊 Pruebas Multiplataforma

Para verificar compatibilidad:

```bash
# Verificar Python
python --version  # o python3 --version en Linux/macOS

# Verificar MySQL
mysql --version

# Verificar dependencias
pip list

# Test de Cloudinary
python test_cloudinary.py
```

---

## 🎯 Ejecución en Producción

### Windows (Servidor):
```cmd
pythonw main.py  # Sin ventana de consola
```

### Linux (Servidor):
```bash
nohup python3 main.py &  # En background
```

### macOS:
```bash
python3 main.py &  # En background
```

---

## 📝 Notas Importantes

1. **Rutas**: La aplicación usa `pathlib` - las rutas se manejan automáticamente
2. **PDFs**: Se abren con el visor predeterminado de cada sistema
3. **MySQL**: Puerto por defecto 3306 en todos los sistemas
4. **Cloudinary**: Funciona igual en todos los sistemas (requiere internet)

---

## ✅ Checklist de Compatibilidad

- ✅ Python 3.8+ instalado
- ✅ MySQL funcionando
- ✅ Dependencias instaladas (`pip install -r requirements.txt`)
- ✅ Archivo `.env` configurado
- ✅ Base de datos creada
- ✅ Migraciones ejecutadas
- ✅ Cloudinary configurado

---

## 🆘 Soporte

Si encuentras problemas específicos de tu sistema operativo:

1. Revisa los logs en la consola
2. Verifica las versiones de Python y MySQL
3. Asegúrate de que todas las dependencias estén instaladas
4. Consulta la documentación específica de tu sistema

---

**¡La aplicación está lista para funcionar en cualquier plataforma!** 🎉
