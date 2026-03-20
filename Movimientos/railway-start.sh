#!/bin/bash
set -e

echo "=========================================="
echo "Iniciando aplicación Django en Railway"
echo "=========================================="
echo ""

# Mostrar variables de entorno
echo "Variables de entorno:"
echo "  PORT=$PORT"
echo "  DATABASE_URL configurada: $([ -n \"$DATABASE_URL\" ] \u0026\u0026 echo 'SÍ' || echo 'NO')"
echo ""

# Verificar PORT
if [ -z "$PORT" ]; then
    echo "⚠️  PORT no definido, usando 8000"
    export PORT=8000
fi

# Verificar DATABASE_URL
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL no está configurada"
    echo "Crea PostgreSQL en Railway: New → Database → Add PostgreSQL"
    exit 1
fi

echo "✅ Configuración correcta"
echo ""

# Crear tablas e importar datos si existe el archivo JSON
if [ -f "datos_exportados.json" ]; then
    echo "📥 Archivo datos_exportados.json encontrado"
    echo "🔄 Creando tablas e importando datos..."
    python importar_a_postgres.py || echo "⚠️  Advertencia: Algunos datos no se pudieron importar"
    echo ""
fi

# Aplicar migraciones de Django (por si faltan tablas del sistema)
echo "📦 Aplicando migraciones de Django..."
python manage.py migrate --noinput || echo "⚠️  Algunas migraciones fallaron (puede ser normal)"
echo ""

# Recolectar archivos estáticos
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear || echo "⚠️  Algunos archivos estáticos no se pudieron recolectar"
echo ""

# Iniciar gunicorn
echo "🚀 Iniciando servidor Gunicorn en puerto $PORT..."
exec gunicorn Movimientos.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --threads 2 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile -
