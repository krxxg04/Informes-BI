@echo off
echo ================================================
echo   PREPARAR PROYECTO PARA GITHUB Y DEPLOYMENT
echo ================================================
echo.

REM Verificar si Git esta instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git no esta instalado
    echo Descargalo de: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/5] Inicializando repositorio Git...
git init

echo.
echo [2/5] Agregando archivos al staging...
git add .

echo.
echo [3/5] Creando commit inicial...
git commit -m "Initial commit - Sistema de Generacion de Informes"

echo.
echo [4/5] Configurando rama principal...
git branch -M main

echo.
echo ================================================
echo   LISTO PARA SUBIR A GITHUB
echo ================================================
echo.
echo PROXIMOS PASOS:
echo.
echo 1. Ve a https://github.com/new
echo 2. Crea un nuevo repositorio (nombre sugerido: sistema-informes)
echo 3. NO marques "Initialize with README"
echo 4. Copia el comando que aparece: git remote add origin...
echo 5. Pegalo aqui y presiona Enter
echo.
echo Ejemplo:
echo git remote add origin https://github.com/TU-USUARIO/sistema-informes.git
echo.
set /p remote="Pega aqui el comando de GitHub y presiona Enter: "
%remote%

echo.
echo [5/5] Subiendo codigo a GitHub...
git push -u origin main

echo.
echo ================================================
echo   CODIGO SUBIDO A GITHUB EXITOSAMENTE!
echo ================================================
echo.
echo AHORA PUEDES DEPLOYAR:
echo.
echo RENDER.COM (Recomendado):
echo   1. Ve a https://render.com
echo   2. Sign up with GitHub
echo   3. New ^> Web Service
echo   4. Conecta tu repositorio
echo   5. Usa estas configuraciones:
echo      - Build Command: pip install -r requirements.txt
echo      - Start Command: gunicorn app.main:app
echo      - Plan: Free
echo   6. Click "Create Web Service"
echo.
echo RAILWAY.APP (Alternativa):
echo   1. Ve a https://railway.app
echo   2. Sign up with GitHub
echo   3. New Project ^> Deploy from GitHub
echo   4. Selecciona tu repo
echo   5. Listo! Se deploya automaticamente
echo.
echo Mira DEPLOYMENT.md para instrucciones detalladas
echo.
pause
