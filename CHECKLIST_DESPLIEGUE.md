# ✅ Checklist Pre-Despliegue

## Verificación antes de desplegar

### 🔍 Verificaciones Locales

```powershell
# 1. Asegúrate de estar en la carpeta del proyecto
cd "C:\Users\Maxip\OneDrive\Documentos\Prepolitecinca\SeptimoSemestre\Usabilidad y Accesibilidad\Proyecto"

# 2. Verifica que el backend funcione localmente
.venv\Scripts\Activate.ps1
python manage.py runserver
# Abre: http://127.0.0.1:8000/api/juego1/?cantidad=3
# Debe devolver JSON con palabras

# 3. Verifica que el frontend funcione localmente (en otra terminal)
cd frontend
npm install
npm run dev
# Abre: http://localhost:5173
# Los juegos deben funcionar

# 4. Si todo funciona, continúa con el despliegue
```

### 📋 Archivos Necesarios (Ya configurados ✅)

- [x] `requirements.txt` - Dependencias Python
- [x] `requirements_production.txt` - Dependencias para producción
- [x] `runtime.txt` - Versión de Python
- [x] `Dockerfile` - Imagen Docker
- [x] `render.yaml` - Configuración Render
- [x] `build.sh` - Script de construcción
- [x] `frontend/vercel.json` - Configuración Vercel
- [x] `frontend/package.json` - Dependencias Node.js
- [x] `frontend/src/config/api.js` - Configuración API

### 🔐 Información que Necesitarás

Prepara esta información antes de empezar:

1. **Cuenta de GitHub**
   - Usuario: _______________
   - Repositorio: _______________
   - URL del repo: https://github.com/_______________/_______________

2. **API Key de Google Gemini (OPCIONAL)**
   - Si la tienes: _______________
   - Si no, déjala vacía (el backend usa datos de respaldo)
   - Obtenerla en: https://makersuite.google.com/app/apikey

3. **URLs que obtendrás durante el despliegue:**
   - Backend (Render): https://_______________.onrender.com
   - Frontend (Vercel): https://_______________.vercel.app

### 🚀 Orden de Despliegue

Sigue este orden exacto:

1. **Primero:** Subir código a GitHub
2. **Segundo:** Desplegar Backend en Render (obtén la URL)
3. **Tercero:** Desplegar Frontend en Vercel (usa la URL del backend)
4. **Cuarto:** Actualizar CORS en Render (usa la URL del frontend)
5. **Quinto:** Probar que todo funcione

### 📝 Comandos Git Importantes

```powershell
# Ver estado del repositorio
git status

# Ver en qué rama estás
git branch

# Ver el repositorio remoto configurado
git remote -v

# Si NO tienes un repositorio configurado:
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main

# Si YA tienes un repositorio configurado:
git add .
git commit -m "Preparar para despliegue en producción"
git push origin main
```

### ⚠️ Problemas Comunes y Soluciones Rápidas

#### Error: "No such file or directory: 'requirements.txt'"
**Solución:** Verifica que estés en la carpeta raíz del proyecto (donde está manage.py)

#### Error: "Port 8000 is already in use"
**Solución:** 
```powershell
# Encontrar el proceso que usa el puerto 8000
netstat -ano | findstr :8000
# Matar el proceso (reemplaza PID con el número que aparece)
taskkill /PID <PID> /F
```

#### Error: "npm: command not found"
**Solución:** Instala Node.js desde https://nodejs.org

#### Error de permisos en PowerShell
**Solución:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 🎯 URLs para Probar Después del Despliegue

Backend (Render):
- [ ] `https://tu-backend.onrender.com/api/juego1/?cantidad=3`
- [ ] `https://tu-backend.onrender.com/api/juego2/?cantidad=3`

Frontend (Vercel):
- [ ] `https://tu-frontend.vercel.app/`
- [ ] Modo Anagrama funciona
- [ ] Modo Sílabas funciona
- [ ] Las imágenes cargan
- [ ] No hay errores en la consola (F12)

### 📞 Recursos de Ayuda

- **Guía completa:** Ver `GUIA_DESPLIEGUE.md`
- **Documentación Backend:** Ver `backend.md`
- **Documentación Frontend:** Ver `frontend.md`
- **Render Docs:** https://render.com/docs
- **Vercel Docs:** https://vercel.com/docs

### 🎉 ¿Listo para Empezar?

Si marcaste todas las verificaciones locales, ¡estás listo para desplegar!

**Siguiente paso:** Abre `GUIA_DESPLIEGUE.md` y sigue la **PARTE 1: Preparar el Código**
