#!/bin/bash
# Script de inicio para Linux/macOS
# Hace el script ejecutable con: chmod +x run.sh

echo "=============================================="
echo "  AutoGest - Sistema de Gestión de Autos"
echo "=============================================="
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "⚠️  No se encontró el entorno virtual."
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Verificar dependencias
echo "Verificando dependencias..."
pip install -q -r requirements.txt

# Ejecutar aplicación
echo ""
echo "Iniciando aplicación..."
echo ""
python3 run.py

# Desactivar entorno virtual al salir
deactivate
