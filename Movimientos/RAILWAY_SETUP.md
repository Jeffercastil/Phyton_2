# INSTRUCCIONES PARA RAILWAY - Sistema de Movimientos

## ⚠️ PROBLEMA ACTUAL
Railway muestra "Application failed to respond" porque NO hay base de datos configurada.
Tu SQL Server local NO es accesible desde internet.

## ✅ SOLUCIÓN PASO A PASO

### Paso 1: Agregar PostgreSQL en Railway (GRATIS)
1. Ve a https://railway.app y haz login
2. Entra a tu proyecto "python2-production"
3. Click en el botón **"New"** (esquina superior derecha)
4. Selecciona **"Database"**
5. Selecciona **"Add PostgreSQL"**
6. Espera a que se cree (toma unos segundos)

### Paso 2: Vincular la base de datos al servicio
1. Verás que aparece un nuevo servicio "PostgreSQL"
2. Railway automáticamente crea la variable `DATABASE_URL` en tu servicio
3. NO necesitas hacer nada manual - Railway lo hace automáticamente

### Paso 3: Configurar variables de entorno (si es necesario)
Ve a tu servicio → pestaña **"Variables"** y asegúrate de tener:

```
DATABASE_URL=postgresql://... (Railway la genera automáticamente)
SECRET_KEY=tu-clave-secreta-aqui (genera una nueva para producción)
DEBUG=False
PORT=8000 (Railway la configura automáticamente)
```

Para generar una SECRET_KEY nueva, ejecuta en tu computadora:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### Paso 4: Hacer Deploy
1. En tu computadora, haz commit de los cambios:
```bash
git add .
git commit -m "Configuración Railway con PostgreSQL"
git push
```

2. Railway detectará automáticamente el push y hará deploy

### Paso 5: Verificar logs
En Railway Dashboard:
1. Ve a tu servicio
2. Click en pestaña **"Deploy"** o **"Logs"**
3. Deberías ver mensajes como:
   - "✅ Configuración correcta"
   - "📦 Aplicando migraciones..."
   - "✅ Migraciones aplicadas correctamente"
   - "🚀 Iniciando servidor Gunicorn..."

## 🔧 ARCHIVOS CREADOS/ACTUALIZADOS

| Archivo | Descripción |
|---------|-------------|
| `railway.json` | Configuración del deploy en Railway |
| `railway-start.sh` | Script de inicio con verificaciones |
| `Procfile` | Configuración del servidor web |

## 🐛 SI SIGUE FALLANDO

### Error: "DATABASE_URL no está configurada"
**Solución:** Asegúrate de haber agregado PostgreSQL y que esté vinculado al servicio.

### Error: "Application failed to respond"
**Solución:** Revisa los logs en Railway Dashboard → Logs. El script ahora muestra mensajes detallados.

### Error de migraciones
Si hay errores de migraciones, ejecuta localmente:
```bash
python manage.py makemigrations
python manage.py migrate
git add .
git commit -m "Fix migraciones"
git push
```

## 📊 ESTRUCTURA DE LA BASE DE DATOS

Las tablas que se crearán automáticamente:
- `auth_user` - Usuarios del sistema
- `base_deuda` - Deudas registradas
- `base_transaccion` - Transacciones (ingresos/gastos)
- `base_perfil` - Perfiles de usuario
- Tablas de Django (sessions, admin, etc.)

## 🌐 URL DE LA APLICACIÓN

Una vez funcionando, tu app estará en:
`https://python2-production.up.railway.app`

O en el dominio que Railway te asigne.

---

**¿Necesitas ayuda?** Revisa los logs en Railway Dashboard → Logs para ver el error exacto.
