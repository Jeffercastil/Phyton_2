# Sistema de Movimientos - Despliegue Railway

## Archivos de Configuración Creados

- `requirements.txt` - Dependencias de Python
- `Procfile` - Comando de inicio para Gunicorn
- `runtime.txt` - Versión de Python
- `railway.json` - Configuración de Railway

## Pasos para Desplegar en Railway

### 1. Crear Proyecto en Railway
1. Ve a https://railway.com/dashboard
2. Haz clic en **"New Project"**
3. Selecciona **"Deploy from GitHub repo"**
4. Elige tu repositorio `Phyton_2`

### 2. Configurar Variables de Entorno
En la sección **"Variables"** del proyecto, agrega:

```
SECRET_KEY=tu-clave-secreta-generada
DEBUG=False
```

Para generar SECRET_KEY:
```python
import secrets
print(secrets.token_urlsafe(50))
```

### 3. Agregar Base de Datos PostgreSQL
1. Haz clic en **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway configurará automáticamente `DATABASE_URL`

### 4. Desplegar
Railway desplegará automáticamente cuando detecte cambios en el repositorio.

## Solución de Problemas

### Error: "No module named 'X'"
Asegúrate de que todas las dependencias estén en `requirements.txt`

### Error de archivos estáticos
WhiteNoise está configurado para servir archivos estáticos automáticamente.

### Error de base de datos
Verifica que la variable `DATABASE_URL` esté configurada correctamente.

## Ver Logs
Ve a la pestaña **"Logs"** en el panel de Railway para ver los errores.
