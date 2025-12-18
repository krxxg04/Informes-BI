@echo off
echo ===============================================
echo   Sistema de Generacion de Informes
echo ===============================================
echo.
echo Iniciando el servidor...
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.8 o superior desde python.org
    pause
    exit /b 1
)

REM Instalar dependencias si es necesario
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Instalando dependencias...
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM Iniciar la aplicacion
echo.
echo ===============================================
echo   Servidor iniciado correctamente!
echo   Abre tu navegador en: http://localhost:5000
echo ===============================================
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python app\main.py

pause
