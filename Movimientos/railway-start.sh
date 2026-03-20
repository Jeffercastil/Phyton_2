#!/bin/bash
set -e

echo "=========================================="
echo "Iniciando aplicación Django en Railway"
echo "=========================================="
echo ""

# Mostrar variables de entorno disponibles (ocultando contraseñas)
echo "Variables de entorno:"
echo "  PORT=$PORT"
echo "  RAILWAY_ENVIRONMENT=$RAILWAY_ENVIRONMENT"
echo "  DATABASE_URL está configurada: $([ -n "$DATABASE_URL" ] && echo 'SÍ' || echo 'NO')"
echo ""

# Verificar que PORT esté definido
if [ -z "$PORT" ]; then
    echo "⚠️  ADVERTENCIA: PORT no está definido, usando 8000 por defecto"
    export PORT=8000
fi

# Verificar que DATABASE_URL esté definido
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL no está configurada"
    echo ""
    echo "Para que la aplicación funcione en Railway, debes:"
    echo "1. Ir al Dashboard de Railway"
    echo "2. Click en 'New' → 'Database' → 'Add PostgreSQL'"
    echo "3. Vincular la base de datos a tu servicio"
    echo ""
    echo "La variable DATABASE_URL se configurará automáticamente."
    exit 1
fi

echo "✅ Configuración correcta"
echo ""

# Aplicar migraciones
echo "📦 Aplicando migraciones de base de datos..."
python manage.py migrate --noinput
if [ $? -eq 0 ]; then
    echo "✅ Migraciones aplicadas correctamente"
else
    echo "❌ Error aplicando migraciones"
    exit 1
fi
echo ""

# Recolectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear
if [ $? -eq 0 ]; then
    echo "✅ Archivos estáticos recolectados"
else
    echo "⚠️  Advertencia: No se pudieron recolectar todos los archivos estáticos"
fi
echo ""

# Verificar que el puerto esté disponible
echo "🔍 Verificando configuración del servidor..."
echo "  Puerto: $PORT"
echo "  Bind: 0.0.0.0:$PORT"
echo ""

# Iniciar gunicorn
echo "🚀 Iniciando servidor Gunicorn..."
echo "=========================================="
exec gunicorn Movimientos.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --threads 2 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile - \
    --capture-output \
    --enable-stdio-inheritance
