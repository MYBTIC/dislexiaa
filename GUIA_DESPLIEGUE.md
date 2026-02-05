# 🚀 Guía Completa de Despliegue - Juego de Palabras

Esta guía te llevará paso a paso para desplegar tu aplicación en producción.

## 📋 Resumen del Despliegue

Tu proyecto se desplegará en **DOS plataformas separadas**:
- **Backend (Django API)** → Render.com (GRATIS)
- **Frontend (React)** → Vercel.com (GRATIS)

**Tiempo estimado:** 30-45 minutos

---

## 🎯 PARTE 1: Preparar el Código

### Paso 1.1: Verificar que el código esté actualizado en GitHub

```powershell
# 1. Abrir PowerShell en la carpeta del proyecto
cd "C:\Users\Maxip\OneDrive\Documentos\Prepolitecinca\SeptimoSemestre\Usabilidad y Accesibilidad\Proyecto"

# 2. Ver el estado de tu repositorio
git status

# 3. Agregar todos los cambios
git add .

# 4. Hacer commit de los cambios
git commit -m "Preparar proyecto para despliegue en producción"

# 5. Subir a GitHub
git push origin main
```

**Nota:** Si no tienes un repositorio en GitHub, créalo primero:
1. Ve a https://github.com/new
2. Crea un repositorio (ej: `juego-palabras-dislexia`)
3. NO inicialices con README (ya tienes código)
4. Sigue las instrucciones para conectar tu repositorio local

### Paso 1.2: Verificar archivos de configuración

✅ Tu proyecto YA tiene estos archivos listos:
- ✅ `render.yaml` - Configuración de Render.com
- ✅ `build.sh` - Script de construcción
- ✅ `runtime.txt` - Versión de Python
- ✅ `requirements.txt` - Dependencias Python
- ✅ `Dockerfile` - Imagen Docker
- ✅ `frontend/vercel.json` - Configuración de Vercel
- ✅ `frontend/package.json` - Dependencias Node.js

---

## 🔧 PARTE 2: Desplegar el Backend en Render.com

### Paso 2.1: Crear cuenta en Render.com

1. Ve a https://render.com
2. Haz clic en **"Get Started"**
3. Regístrate con tu cuenta de **GitHub** (recomendado)
4. Autoriza a Render para acceder a tus repositorios

### Paso 2.2: Crear un nuevo Web Service

1. En el dashboard de Render, haz clic en **"New +"**
2. Selecciona **"Web Service"**
3. Conecta tu repositorio de GitHub:
   - Busca: `Dislexia` o el nombre de tu repositorio
   - Haz clic en **"Connect"**

### Paso 2.3: Configurar el Web Service

Usa estos valores exactos:

| Campo | Valor |
|-------|-------|
| **Name** | `dislexia-backend` (o el nombre que prefieras) |
| **Environment** | `Docker` |
| **Region** | `Oregon (US West)` (o el más cercano a ti) |
| **Branch** | `main` |
| **Root Directory** | `.` (dejar en blanco) |
| **Dockerfile Path** | `./Dockerfile` |
| **Docker Context** | `.` |

### Paso 2.4: Configurar Variables de Entorno

En la sección **"Environment Variables"**, agrega estas variables:

| Key | Value | Notas |
|-----|-------|-------|
| `SECRET_KEY` | (dejar vacío) | Render lo generará automáticamente |
| `DEBUG` | `False` | Importante para producción |
| `ALLOWED_HOSTS` | `.onrender.com` | Permite el dominio de Render |
| `GEMINI_API_KEY` | Tu API key | OPCIONAL - Si no la tienes, déjala vacía |
| `CORS_ALLOWED_ORIGINS` | `https://tuapp.vercel.app` | Lo actualizaremos después |

**Cómo agregar variables:**
1. Haz clic en **"Add Environment Variable"**
2. Ingresa el nombre (Key) y valor (Value)
3. Repite para cada variable

**Nota sobre GEMINI_API_KEY:**
- Si NO tienes una API key, déjala en blanco
- El backend funcionará con datos de respaldo
- Para obtener una API key: https://makersuite.google.com/app/apikey

### Paso 2.5: Crear la Base de Datos (OPCIONAL)

Si prefieres usar PostgreSQL en lugar de SQLite:

1. En el dashboard, haz clic en **"New +"** → **"PostgreSQL"**
2. Configura:
   - **Name:** `dislexia-db`
   - **Database:** `dislexia`
   - **User:** `dislexia_user`
   - **Region:** El mismo que tu Web Service
   - **Plan:** Free (0MB - suficiente para desarrollo)
3. Haz clic en **"Create Database"**
4. Vuelve a tu Web Service y agrega la variable:
   - **Key:** `DATABASE_URL`
   - **Value:** Selecciona "From Database" → `dislexia-db` → Connection String

**Nota:** SQLite funcionará bien para este proyecto. PostgreSQL es opcional.

### Paso 2.6: Desplegar el Backend

1. Revisa toda la configuración
2. Haz clic en **"Create Web Service"**
3. Render comenzará a construir tu aplicación:
   - ⏳ **Building...** (5-10 minutos)
   - ⏳ **Deploying...**
   - ✅ **Live** (cuando esté listo)

4. **Espera a que aparezca el estado "Live"**

### Paso 2.7: Obtener la URL del Backend

1. Una vez desplegado, verás una URL como:
   ```
   https://dislexia-backend.onrender.com
   ```
2. **Copia esta URL** - la necesitarás para el frontend
3. Prueba que funcione visitando:
   ```
   https://tu-backend.onrender.com/api/juego1/?cantidad=3
   ```
   Deberías ver un JSON con palabras

### Paso 2.8: Verificar el Backend (Testing)

Abre estos endpoints en tu navegador para verificar:

✅ **Juego de Anagramas:**
```
https://tu-backend.onrender.com/api/juego1/?cantidad=3
```

✅ **Juego de Sílabas:**
```
https://tu-backend.onrender.com/api/juego2/?cantidad=3
```

Si ves JSON con datos, ¡tu backend está funcionando! 🎉

---

## 🎨 PARTE 3: Desplegar el Frontend en Vercel

### Paso 3.1: Crear cuenta en Vercel

1. Ve a https://vercel.com
2. Haz clic en **"Sign Up"**
3. Regístrate con tu cuenta de **GitHub** (recomendado)
4. Autoriza a Vercel para acceder a tus repositorios

### Paso 3.2: Configurar la URL del Backend

Antes de desplegar, debes actualizar la configuración del frontend:

1. Abre el archivo `frontend/src/config/api.js` en tu editor
2. Encuentra esta línea:
   ```javascript
   const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
   ```
3. Déjala como está (usaremos variables de entorno)

### Paso 3.3: Importar el Proyecto

1. En el dashboard de Vercel, haz clic en **"Add New..."** → **"Project"**
2. Busca tu repositorio de GitHub
3. Haz clic en **"Import"**

### Paso 3.4: Configurar el Proyecto

| Campo | Valor |
|-------|-------|
| **Project Name** | `juego-palabras-dislexia` (o el que prefieras) |
| **Framework Preset** | `Vite` (detectado automáticamente) |
| **Root Directory** | `frontend` ⚠️ **MUY IMPORTANTE** |
| **Build Command** | `npm run build` (por defecto) |
| **Output Directory** | `dist` (por defecto) |
| **Install Command** | `npm install` (por defecto) |

### Paso 3.5: Configurar Variables de Entorno

En la sección **"Environment Variables"**, agrega:

| Name | Value |
|------|-------|
| `VITE_API_URL` | `https://tu-backend.onrender.com` |

⚠️ **Importante:** Reemplaza `tu-backend.onrender.com` con la URL real de tu backend de Render.

**Ejemplo:**
```
VITE_API_URL = https://dislexia-backend-k7h2.onrender.com
```

### Paso 3.6: Desplegar el Frontend

1. Revisa toda la configuración
2. Haz clic en **"Deploy"**
3. Vercel construirá tu aplicación:
   - ⏳ **Building...** (2-5 minutos)
   - ⏳ **Deploying...**
   - ✅ **Ready** (cuando esté listo)

### Paso 3.7: Obtener la URL del Frontend

1. Una vez desplegado, verás una URL como:
   ```
   https://juego-palabras-dislexia.vercel.app
   ```
2. **Copia esta URL**
3. Vercel también te dará URLs de preview para cada deploy

### Paso 3.8: Probar el Frontend

1. Abre la URL de tu frontend en el navegador
2. Verifica que:
   - ✅ La página carga correctamente
   - ✅ Los juegos funcionan
   - ✅ Las imágenes se muestran
   - ✅ Se pueden jugar ambos modos

---

## 🔄 PARTE 4: Conectar Backend y Frontend (CORS)

### Paso 4.1: Actualizar CORS en el Backend

1. Ve a tu servicio en Render.com
2. Navega a **"Environment"**
3. Edita la variable `CORS_ALLOWED_ORIGINS`
4. Reemplaza con la URL de tu frontend de Vercel:
   ```
   https://juego-palabras-dislexia.vercel.app
   ```
5. Haz clic en **"Save Changes"**
6. Render redesplegará automáticamente (1-2 minutos)

### Paso 4.2: Verificar la Conexión

1. Abre tu frontend en Vercel
2. Abre las **DevTools** del navegador (F12)
3. Ve a la pestaña **"Network"**
4. Juega un juego
5. Verifica que las peticiones a la API respondan con código **200 OK**

Si ves errores de CORS, verifica que:
- ✅ La URL en `CORS_ALLOWED_ORIGINS` sea correcta
- ✅ No haya espacios extra
- ✅ Use `https://` (no `http://`)
- ✅ No tenga `/` al final

---

## 🎉 PARTE 5: Verificación Final

### Checklist de Funcionalidad

Prueba tu aplicación en producción:

✅ **Backend Funcionando:**
- [ ] `/api/juego1/` devuelve palabras con imágenes
- [ ] `/api/juego2/` devuelve palabras con sílabas
- [ ] `/api/oracion/` genera oraciones (POST)
- [ ] No hay errores 500

✅ **Frontend Funcionando:**
- [ ] La página carga sin errores
- [ ] El modo Anagrama funciona
- [ ] El modo Sílabas funciona
- [ ] Las imágenes se cargan correctamente
- [ ] Los sonidos funcionan (si aplica)
- [ ] La configuración se guarda

✅ **Conexión Backend-Frontend:**
- [ ] No hay errores de CORS en la consola
- [ ] Las peticiones a la API responden con datos
- [ ] Los juegos se actualizan correctamente

---

## 🔧 PARTE 6: Configuración Opcional - API de Google Gemini

Si quieres habilitar la generación dinámica de oraciones con IA:

### Paso 6.1: Obtener API Key de Google Gemini

1. Ve a https://makersuite.google.com/app/apikey
2. Inicia sesión con tu cuenta de Google
3. Haz clic en **"Create API Key"**
4. Copia la API key generada

### Paso 6.2: Agregar la API Key en Render

1. Ve a tu servicio en Render.com
2. Navega a **"Environment"**
3. Edita la variable `GEMINI_API_KEY`
4. Pega tu API key
5. Haz clic en **"Save Changes"**

**Límites de la API Gratuita:**
- ~15-20 peticiones por minuto
- Suficiente para uso normal del juego

---

## 🚨 Solución de Problemas Comunes

### Problema 1: Backend no despliega (Build Fails)

**Síntomas:**
- Error durante el build en Render
- Logs muestran errores de dependencias

**Soluciones:**
1. Verifica que `requirements.txt` esté actualizado
2. Verifica que `runtime.txt` tenga una versión válida de Python
3. Revisa los logs completos en Render para ver el error específico

### Problema 2: Frontend muestra errores 404

**Síntomas:**
- Página en blanco
- Errores en la consola del navegador

**Soluciones:**
1. Verifica que el **Root Directory** sea `frontend`
2. Verifica que `vercel.json` tenga la configuración de rewrites
3. Limpia caché y redespliega

### Problema 3: Errores de CORS

**Síntomas:**
```
Access to XMLHttpRequest at 'https://...' from origin 'https://...' has been blocked by CORS policy
```

**Soluciones:**
1. Verifica que `CORS_ALLOWED_ORIGINS` tenga la URL exacta de tu frontend
2. NO incluyas `/` al final de la URL
3. Usa `https://` (no `http://`)
4. Guarda los cambios y espera a que Render redesplegue

### Problema 4: Base de datos no funciona

**Síntomas:**
- Errores relacionados con SQLite
- "Unable to open database file"

**Soluciones:**
1. Si usas SQLite, es normal que se resetee en cada deploy
2. Considera usar PostgreSQL de Render (ver Paso 2.5)
3. O ejecuta migraciones después de cada deploy

### Problema 5: Imágenes no cargan

**Síntomas:**
- Las imágenes no se muestran en el juego
- Errores 404 en imágenes

**Soluciones:**
1. Verifica que Unsplash API esté funcionando
2. Revisa los logs del backend
3. Verifica que las URLs de imágenes sean válidas

### Problema 6: Render dice "Service Unavailable"

**Síntomas:**
- 503 Service Unavailable
- El servicio no responde

**Causas comunes:**
- Render free tier se duerme después de 15 minutos sin uso
- Primera petición después de inactividad tarda ~30 segundos

**Soluciones:**
1. Espera 30-60 segundos y recarga
2. El servicio "despertará" automáticamente
3. Considera usar un servicio de "keep-alive" (opcional)

---

## 📊 Monitoreo y Mantenimiento

### Ver Logs en Render

1. Ve a tu servicio en Render.com
2. Haz clic en **"Logs"**
3. Aquí verás todos los logs del backend en tiempo real
4. Útil para depurar errores

### Ver Logs en Vercel

1. Ve a tu proyecto en Vercel.com
2. Haz clic en la pestaña **"Logs"**
3. Selecciona un deployment
4. Verás logs de build y runtime

### Redesplegar Manualmente

**En Render:**
1. Ve a tu servicio
2. Haz clic en **"Manual Deploy"** → **"Deploy latest commit"**

**En Vercel:**
1. Ve a tu proyecto
2. Haz clic en **"Deployments"**
3. Selecciona un deployment y haz clic en **"Redeploy"**

### Actualizar el Código

Cada vez que hagas cambios y los subas a GitHub:

```powershell
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

**Auto-despliegue:**
- ✅ Render redesplegará automáticamente
- ✅ Vercel redesplegará automáticamente

---

## 📝 URLs Importantes

Guarda estas URLs para referencia:

| Servicio | URL | Uso |
|----------|-----|-----|
| **Backend (Render)** | `https://tu-backend.onrender.com` | API REST |
| **Frontend (Vercel)** | `https://tu-app.vercel.app` | Aplicación web |
| **API Juego 1** | `https://tu-backend.onrender.com/api/juego1/` | Endpoint anagramas |
| **API Juego 2** | `https://tu-backend.onrender.com/api/juego2/` | Endpoint sílabas |
| **API Oraciones** | `https://tu-backend.onrender.com/api/oracion/` | Endpoint oraciones |
| **GitHub Repo** | `https://github.com/usuario/repo` | Código fuente |
| **Render Dashboard** | `https://dashboard.render.com` | Panel de control |
| **Vercel Dashboard** | `https://vercel.com/dashboard` | Panel de control |

---

## 💰 Costos y Límites

### Render.com (Plan Free)

✅ **Gratis incluye:**
- 750 horas de servicio por mes
- 512 MB RAM
- 1 GB de almacenamiento
- HTTPS automático
- Auto-despliegue desde GitHub

⚠️ **Limitaciones:**
- El servicio se "duerme" después de 15 min sin uso
- Primera petición tras inactividad tarda ~30 seg
- Se resetea cada mes (horas vuelven a 750)

### Vercel (Plan Hobby - Free)

✅ **Gratis incluye:**
- 100 GB de ancho de banda por mes
- Despliegues ilimitados
- HTTPS automático
- CDN global
- Preview deployments

⚠️ **Limitaciones:**
- Solo para proyectos personales (no comerciales)
- Límite de 100 GB/mes (más que suficiente)

### Google Gemini API (Free Tier)

✅ **Gratis incluye:**
- 15 peticiones por minuto
- 1500 peticiones por día
- 1M peticiones por mes

**Nota:** Para este proyecto, el uso gratuito es más que suficiente.

---

## 🎯 Próximos Pasos (Opcional)

Una vez tu app esté en producción, considera:

### 1. Dominio Personalizado

**Para el Frontend (Vercel):**
1. Compra un dominio (ej: en Namecheap, Google Domains)
2. En Vercel, ve a **Settings** → **Domains**
3. Agrega tu dominio y sigue las instrucciones
4. Actualiza los DNS de tu dominio

**Para el Backend (Render):**
1. En Render, ve a **Settings** → **Custom Domain**
2. Agrega tu dominio (ej: api.tudominio.com)
3. Actualiza los DNS de tu dominio
4. Render manejará el certificado SSL automáticamente

### 2. Monitoreo y Analytics

- **Vercel Analytics:** Habilítalo en Settings → Analytics
- **Render Metrics:** Visibles en el dashboard
- **Google Analytics:** Agrégalo al frontend para métricas de usuarios

### 3. Mejoras de Rendimiento

- **Caching:** Configura headers de cache en el backend
- **CDN:** Vercel ya usa CDN global
- **Optimización de imágenes:** Considera usar Vercel Image Optimization

### 4. Seguridad

- **Rate Limiting:** Agrega límites de peticiones en Django
- **HTTPS Only:** Ya configurado automáticamente
- **Variables de entorno:** NUNCA las subas a GitHub

---

## 📚 Recursos Adicionales

### Documentación Oficial

- **Render.com:** https://render.com/docs
- **Vercel:** https://vercel.com/docs
- **Django REST Framework:** https://www.django-rest-framework.org/
- **Vite:** https://vitejs.dev/guide/
- **React:** https://react.dev/

### Tutoriales Útiles

- Render Django Deploy: https://render.com/docs/deploy-django
- Vercel React Deploy: https://vercel.com/docs/frameworks/vite
- Docker con Render: https://render.com/docs/docker

### Soporte

- **Render Community:** https://community.render.com/
- **Vercel Discord:** https://vercel.com/discord
- **Stack Overflow:** Busca con tags: `django`, `react`, `render`, `vercel`

---

## ✅ Checklist Final

Antes de considerar el despliegue completo:

- [ ] Código subido a GitHub
- [ ] Backend desplegado en Render
- [ ] Frontend desplegado en Vercel
- [ ] CORS configurado correctamente
- [ ] Variables de entorno configuradas
- [ ] API funcionando (prueba los 3 endpoints)
- [ ] Frontend funcionando (prueba ambos juegos)
- [ ] No hay errores en las consolas
- [ ] Imágenes cargando correctamente
- [ ] Documentación actualizada con URLs reales

---

## 🎉 ¡Felicidades!

Si llegaste hasta aquí y completaste todos los pasos, ¡tu aplicación está en producción! 🚀

Ahora puedes compartir la URL de Vercel con cualquier persona y ellos podrán usar tu juego de palabras desde cualquier lugar del mundo.

**URLs para compartir:**
```
🌐 Aplicación Web: https://tu-app.vercel.app
🔧 API Backend: https://tu-backend.onrender.com/api/juego1/
```

---

## 📞 Contacto y Soporte

Si necesitas ayuda adicional:

1. **Revisa los logs** en Render y Vercel primero
2. **Busca el error** en Stack Overflow
3. **Consulta la documentación** oficial
4. **Pregunta en los foros** de las comunidades

**Recuerda:** La primera vez que alguien acceda a tu app después de inactividad, puede tardar ~30 segundos mientras Render "despierta" el servicio. ¡Es normal en el plan gratuito!

---

**Última actualización:** Febrero 2026
**Versión:** 1.0.0
