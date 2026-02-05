# 🚀 Inicio Rápido - Despliegue en 5 Pasos

## Resumen Ultra Rápido

Tu proyecto se despliega en **2 plataformas gratuitas**:
- **Backend** → Render.com
- **Frontend** → Vercel.com

**Tiempo total:** 30-45 minutos

---

## 📌 PASO 1: GitHub (5 minutos)

```powershell
# En la carpeta del proyecto
cd "C:\Users\Maxip\OneDrive\Documentos\Prepolitecinca\SeptimoSemestre\Usabilidad y Accesibilidad\Proyecto"

# Subir cambios a GitHub
git add .
git commit -m "Preparar para despliegue"
git push origin main
```

Si no tienes repositorio en GitHub:
1. Ve a https://github.com/new
2. Crea un repo nuevo (sin README)
3. Ejecuta:
```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

---

## 📌 PASO 2: Backend en Render (15 minutos)

### 2.1 Crear Web Service
1. Ve a https://render.com → Regístrate con GitHub
2. Dashboard → **New +** → **Web Service**
3. Conecta tu repositorio de GitHub

### 2.2 Configuración
| Campo | Valor |
|-------|-------|
| Name | `dislexia-backend` |
| Environment | `Docker` |
| Branch | `main` |
| Dockerfile Path | `./Dockerfile` |

### 2.3 Variables de Entorno
Agrega estas variables (clic en "Add Environment Variable"):

```
SECRET_KEY = (dejar vacío - se auto-genera)
DEBUG = False
ALLOWED_HOSTS = .onrender.com
GEMINI_API_KEY = (opcional - déjalo vacío si no tienes)
CORS_ALLOWED_ORIGINS = https://tu-app.vercel.app
```

### 2.4 Desplegar
- Clic en **"Create Web Service"**
- Espera 5-10 minutos
- Copia tu URL: `https://TU-BACKEND.onrender.com`

### 2.5 Probar
Abre en el navegador:
```
https://TU-BACKEND.onrender.com/api/juego1/?cantidad=3
```
Deberías ver JSON con palabras ✅

---

## 📌 PASO 3: Frontend en Vercel (10 minutos)

### 3.1 Importar Proyecto
1. Ve a https://vercel.com → Regístrate con GitHub
2. Dashboard → **Add New...** → **Project**
3. Busca tu repositorio → **Import**

### 3.2 Configuración

| Campo | Valor |
|-------|-------|
| Project Name | `juego-palabras-dislexia` |
| Framework Preset | `Vite` |
| Root Directory | `frontend` ⚠️ IMPORTANTE |
| Build Command | `npm run build` |
| Output Directory | `dist` |

### 3.3 Variable de Entorno

Agrega esta variable (clic en "Add"):

```
VITE_API_URL = https://TU-BACKEND.onrender.com
```

⚠️ Usa la URL de tu backend de Render (Paso 2.4)

### 3.4 Desplegar
- Clic en **"Deploy"**
- Espera 2-5 minutos
- Copia tu URL: `https://TU-APP.vercel.app`

---

## 📌 PASO 4: Conectar Frontend y Backend (5 minutos)

### 4.1 Actualizar CORS en Render
1. Ve a tu servicio en Render
2. Navega a **"Environment"**
3. Edita `CORS_ALLOWED_ORIGINS`
4. Reemplaza con tu URL de Vercel:
   ```
   https://TU-APP.vercel.app
   ```
5. **Save Changes**
6. Espera 1-2 minutos que redesplegue

---

## 📌 PASO 5: Verificar (5 minutos)

### 5.1 Probar el Frontend
Abre tu app en Vercel: `https://TU-APP.vercel.app`

✅ Checklist:
- [ ] La página carga
- [ ] Modo Anagrama funciona
- [ ] Modo Sílabas funciona
- [ ] Las imágenes cargan
- [ ] No hay errores en consola (F12)

### 5.2 Probar el Backend
Abre estos endpoints:

```
https://TU-BACKEND.onrender.com/api/juego1/?cantidad=3
https://TU-BACKEND.onrender.com/api/juego2/?cantidad=3
```

Ambos deben devolver JSON con datos ✅

---

## 🎉 ¡Listo!

Tu aplicación está en producción. Ahora puedes compartir la URL:

```
🌐 https://TU-APP.vercel.app
```

---

## 🚨 Problemas Comunes

### El backend tarda mucho en responder
**Causa:** Render se "duerme" después de 15 min sin uso (plan gratuito)
**Solución:** Espera 30 segundos en la primera petición. Luego funciona normal.

### Errores de CORS
**Síntoma:** "blocked by CORS policy" en la consola
**Solución:** 
1. Verifica que `CORS_ALLOWED_ORIGINS` en Render tenga la URL exacta de Vercel
2. Sin `/` al final
3. Con `https://` (no `http://`)

### Frontend muestra página en blanco
**Solución:**
1. Verifica que el **Root Directory** sea `frontend`
2. Verifica que `VITE_API_URL` esté configurada correctamente
3. Abre DevTools (F12) y revisa errores en la consola

### Build falla en Render
**Solución:**
1. Revisa los logs completos en Render
2. Verifica que `Dockerfile` y `requirements_production.txt` existan
3. Verifica que `runtime.txt` tenga una versión válida de Python

---

## 📚 Más Información

- **Guía completa detallada:** `GUIA_DESPLIEGUE.md`
- **Checklist pre-despliegue:** `CHECKLIST_DESPLIEGUE.md`
- **Documentación backend:** `backend.md`
- **Documentación frontend:** `frontend.md`

---

## 🔧 Redesplegar Cambios

Cada vez que hagas cambios en el código:

```powershell
git add .
git commit -m "Descripción del cambio"
git push origin main
```

Render y Vercel redesplegarán automáticamente ✅

---

## 💰 Costos

**TODO ES GRATIS** 🎉

- ✅ Render Free: 750 horas/mes
- ✅ Vercel Hobby: Despliegues ilimitados
- ✅ Google Gemini API: 1500 peticiones/día

Más que suficiente para tu proyecto.

---

**¿Listo para empezar? ¡Comienza con el PASO 1!** 🚀
