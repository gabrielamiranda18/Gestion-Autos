@echo off
REM Script de inicio para Windows

echo ==============================================
echo   AutoGest - Sistema de Gestion de Autos
echo ==============================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\" (
    echo Advertencia: No se encontro el entorno virtual.
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar dependencias
echo Verificando dependencias...
pip install -q -r requirements.txt

REM Ejecutar aplicación
echo.
echo Iniciando aplicacion...
echo.
python run.py

REM Pausa al finalizar (opcional)
pause
