# 🔄 MIGRACIÓN: SQL Server → PostgreSQL (Railway)

## 📋 RESUMEN DEL PROCESO

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│  SQL Server     │────▶│  Archivo     │────▶│  PostgreSQL     │
│  (Tu PC Local)  │     │  JSON        │     │  (Railway)      │
└─────────────────┘     └──────────────┘     └─────────────────┘
```

---

## PASO 1: Exportar datos de SQL Server (En tu PC)

### 1.1 Instalar pyodbc (si no lo tienes)
```bash
pip install pyodbc
```

### 1.2 Ejecutar el script de exportación
```bash
python exportar_sql_server.py
```

Esto creará un archivo `datos_exportados.json` con toda tu información.

### 1.3 Verificar que se creó el archivo
Busca el archivo `datos_exportados.json` en la carpeta del proyecto.

---

## PASO 2: Configurar PostgreSQL en Railway

### 2.1 Crear la base de datos PostgreSQL
1. Ve a https://railway.app/dashboard
2. Entra a tu proyecto "python2-production"
3. Click en **"New"** → **"Database"** → **"Add PostgreSQL"**
4. Espera a que se cree (aparecerá un servicio nuevo)

### 2.2 Vincular la base de datos
Railway automáticamente:
- ✅ Crea la variable `DATABASE_URL`
- ✅ Vincula la base de datos a tu servicio

### 2.3 Configurar variables de entorno
Ve a tu servicio → pestaña **"Variables"** y agrega:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `SECRET_KEY` | `django-insecure-tu-clave-aqui` | Clave secreta de Django |
| `DEBUG` | `False` | Modo producción |

Para generar SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

## PASO 3: Subir archivos a Railway

### 3.1 Agregar archivos al commit
```bash
git add exportar_sql_server.py importar_a_postgresql.py datos_exportados.json
git commit -m "Datos exportados de SQL Server"
git push
```

### 3.2 Subir a Railway
Railway detectará automáticamente el push y hará deploy.

---

## PASO 4: Importar datos en Railway

### 4.1 Abrir consola de Railway
1. Ve a https://railway.app/dashboard
2. Entra a tu servicio
3. Click en pestaña **"Deploy"**
4. Busca el botón **"Shell"** o **"Console"**

### 4.2 Ejecutar migraciones de Django
```bash
python manage.py migrate
```

### 4.3 Importar los datos
```bash
python importar_a_postgresql.py
```

Verás mensajes como:
```
✅ Creado usuario: jeff
✅ Deuda creada: Tarjeta de Crédito
✅ Transacción creada
...
```

---

## PASO 5: Verificar que todo funciona

### 5.1 Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 5.2 Reiniciar el servicio
En Railway Dashboard → tu servicio → click en **"Restart"**

### 5.3 Probar la aplicación
Visita tu URL de Railway (ej: `https://python2-production.up.railway.app`)

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### Error: "No module named pyodbc"
**Solución:** pyodbc solo se necesita en tu PC local, no en Railway.

### Error: "DATABASE_URL no está configurada"
**Solución:** Asegúrate de haber creado PostgreSQL en Railway (Paso 2.1)

### Error: "datos_exportados.json no encontrado"
**Solución:** Ejecuta primero `python exportar_sql_server.py` en tu PC

### Error: "Usuario ya existe"
**Esto es normal** - el script omite usuarios duplicados.

---

## 📊 ESTRUCTURA DE DATOS

Las tablas se crearán automáticamente en PostgreSQL:

| Tabla | Descripción |
|-------|-------------|
| `auth_user` | Usuarios del sistema |
| `base_deuda` | Deudas registradas |
| `base_transaccion` | Transacciones (ingresos/gastos) |
| `base_perfil` | Perfiles de usuario |

---

## ⚠️ NOTAS IMPORTANTES

1. **Contraseñas:** Los usuarios importados tendrán contraseña `temporal123`. Deben cambiarla.

2. **IDs:** Los IDs de los registros cambiarán en PostgreSQL (es normal).

3. **Fechas:** Se mantienen las fechas originales.

4. **Montos:** Se mantienen los valores exactos.

5. **Relaciones:** Las relaciones entre tablas se preservan.

---

## ✅ CHECKLIST

- [ ] Ejecutar `python exportar_sql_server.py` en PC
- [ ] Verificar que existe `datos_exportados.json`
- [ ] Crear PostgreSQL en Railway
- [ ] Configurar variables de entorno (SECRET_KEY)
- [ ] Hacer push a GitHub
- [ ] Esperar deploy en Railway
- [ ] Ejecutar `python manage.py migrate` en Railway
- [ ] Ejecutar `python importar_a_postgresql.py` en Railway
- [ ] Probar la aplicación

---

## 🆘 ¿NECESITAS AYUDA?

Si tienes problemas, revisa:
1. Los logs en Railway Dashboard → Logs
2. Que PostgreSQL esté creado y vinculado
3. Que el archivo `datos_exportados.json` exista
