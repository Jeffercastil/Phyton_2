@echo off
chcp 65001 >nul
echo ==========================================
echo  EXPORTAR DATOS Y SUBIR A RAILWAY
echo ==========================================
echo.

:: Verificar Python
echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado
    pause
    exit /b 1
)
echo ✅ Python encontrado
echo.

:: Paso 1: Exportar datos
echo ==========================================
echo PASO 1: Exportando datos de SQL Server
echo ==========================================
echo.
python exportar_directo.py
if errorlevel 1 (
    echo ❌ Error exportando datos
    pause
    exit /b 1
)

echo.
echo ✅ Datos exportados correctamente
echo.

:: Verificar que existe el archivo
if not exist "datos_exportados.json" (
    echo ❌ No se encontro datos_exportados.json
    pause
    exit /b 1
)

:: Paso 2: Subir a GitHub
echo ==========================================
echo PASO 2: Subiendo a GitHub
echo ==========================================
echo.

echo Agregando archivos...
git add datos_exportados.json
git add exportar_directo.py
git add EXPORTAR_Y_SUBIR.bat

echo.
echo Creando commit...
git commit -m "Datos exportados de SQL Server - %date%"

echo.
echo Subiendo a GitHub...
git push

if errorlevel 1 (
    echo ❌ Error subiendo a GitHub
    echo Intenta manualmente:
    echo   git add datos_exportados.json
    echo   git commit -m "Datos exportados"
    echo   git push
    pause
    exit /b 1
)

echo.
echo ==========================================
echo ✅ TODO COMPLETADO
echo ==========================================
echo.
echo Ahora debes hacer en Railway:
echo.
echo 1. Ve a https://railway.app/dashboard
echo 2. Entra a tu proyecto "python2-production"
echo 3. Click en "New" → "Database" → "Add PostgreSQL"
echo 4. Espera 10 segundos a que se cree
echo 5. Railway hara deploy automatico con tus datos
echo.
echo Tu app estara en:
echo https://python2-production.up.railway.app
echo.
pause
