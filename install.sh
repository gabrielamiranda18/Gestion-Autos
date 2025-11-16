#!/bin/bash

echo "=========================================="
echo "🐧 Instalador de AutoGest para Linux"
echo "=========================================="
echo ""

# Detectar distribución de Linux
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    DISTRO="unknown"
fi

echo "📦 Distribución detectada: $DISTRO"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado."
    echo "Instalando Python 3..."
    
    case $DISTRO in
        ubuntu|debian|linuxmint)
            sudo apt update
            sudo apt install python3 python3-pip python3-venv python3-tk -y
            ;;
        fedora|rhel|centos)
            sudo dnf install python3 python3-pip python3-tkinter -y
            ;;
        arch|manjaro)
            sudo pacman -S python python-pip tk --noconfirm
            ;;
        opensuse*)
            sudo zypper install python3 python3-pip python3-tk -y
            ;;
        *)
            echo "⚠️  Distribución no reconocida. Por favor instala Python manualmente:"
            echo "  - Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv python3-tk"
            echo "  - Fedora/RHEL: sudo dnf install python3 python3-pip python3-tkinter"
            echo "  - Arch: sudo pacman -S python python-pip tk"
            exit 1
            ;;
    esac
fi

echo "✅ Python $(python3 --version) encontrado"
echo ""

# Verificar si MySQL/MariaDB está instalado
if ! command -v mysql &> /dev/null; then
    echo "⚠️  MySQL/MariaDB no está instalado."
    echo "Instalando MariaDB Server..."
    
    case $DISTRO in
        ubuntu|debian|linuxmint)
            sudo apt update
            sudo apt install mariadb-server -y
            ;;
        fedora|rhel|centos)
            sudo dnf install mariadb-server -y
            ;;
        arch|manjaro)
            sudo pacman -S mariadb --noconfirm
            ;;
        opensuse*)
            sudo zypper install mariadb -y
            ;;
        *)
            echo "⚠️  Por favor instala MariaDB manualmente para tu distribución"
            ;;
    esac
    
    # Iniciar MariaDB (el servicio se llama mariadb en Fedora)
    sudo systemctl start mariadb 2>/dev/null || sudo systemctl start mysql 2>/dev/null
    sudo systemctl enable mariadb 2>/dev/null || sudo systemctl enable mysql 2>/dev/null
    echo "✅ MariaDB instalado y configurado"
else
    echo "✅ MySQL/MariaDB encontrado"
fi

echo ""

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv

echo "✅ Entorno virtual creado"
echo ""

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

echo "✅ Dependencias instaladas"
echo ""

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p cache output

# Configurar .env
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Archivo .env creado desde .env.example"
        echo "⚠️  Edita .env con tus credenciales: nano .env"
    fi
else
    echo "✅ Archivo .env ya existe"
fi

echo ""
echo "========================================="
echo "✅ Instalación completada!"
echo "========================================="
echo ""
echo "📋 Próximos pasos:"
echo ""
echo "1. Configura MariaDB:"
echo "   sudo mysql -u root < database/venta_autos_db.sql"
echo ""
echo "2. Edita .env con tus credenciales:"
echo "   nano .env"
echo "   Configura: DB_USER=root y DB_PASSWORD= (vacío)"
echo ""
echo "3. Ejecuta la aplicación:"
echo "   ./run.sh"
echo ""

# Dar permisos de ejecución a run.sh
chmod +x run.sh
