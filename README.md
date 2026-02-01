# 🎮 Juego de Palabras - Sistema de Dislexia

Aplicación web educativa para ayudar a niños con dislexia mediante juegos interactivos de palabras.

## 📁 Estructura del Proyecto

```
USABILIDAD/
├── backend (Django)
│   ├── Dislexia/          # Configuración del proyecto
│   ├── api/               # API REST
│   ├── manage.py
│   └── db.sqlite3         # Base de datos SQLite
│
├── frontend (React + Vite)
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── data/          # Datos de prueba
│   │   └── App.jsx        # Componente principal
│   └── package.json
│
└── README.md              # Este archivo
```

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.11+ (recomendado: 3.13)
- Node.js 22.12+ (o 20.19+)
- Git Bash (para Windows)

### 1️⃣ Backend (Django)

```bash
# Activar entorno virtual
source .venv/Scripts/activate

# Instalar dependencias (primera vez)
pip install -r requirements.txt

# Ejecutar migraciones (primera vez)
python manage.py migrate

# Iniciar servidor backend
python manage.py runserver
```

El backend estará disponible en: **http://127.0.0.1:8000/**

### 2️⃣ Frontend (React)

```bash
# Entrar a la carpeta frontend
cd frontend

# Instalar dependencias (primera vez)
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará disponible en: **http://localhost:5173/**

## 🎯 Modos de Juego

### 1. Modo Anagrama
- Los niños reorganizan letras desordenadas para formar palabras
- Pueden escribir directamente con el teclado o hacer clic en las letras
- Se muestran imágenes de referencia

### 2. Modo Sílabas
- Los niños completan palabras eligiendo la sílaba correcta
- Ejercicio de reconocimiento silábico

### 3. Repetición de Oración
- Después de completar una palabra, se genera una oración
- Los niños deben repetir la oración usando reconocimiento de voz
- Usa Google Gemini AI para generar oraciones apropiadas

## 🔧 API Endpoints

### Backend (Django REST)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/juego1/` | Obtiene 2 palabras aleatorias para anagramas |
| GET | `/api/juego2/` | Obtiene 1 palabra aleatoria para sílabas |
| POST | `/api/oracion/` | Genera una oración con Gemini AI |

### Ejemplo de uso del API

```bash
# Obtener palabras para anagrama
curl http://127.0.0.1:8000/api/juego1/

# Generar oración
curl -X POST http://127.0.0.1:8000/api/oracion/ \
  -H "Content-Type: application/json" \
  -d '{"palabra": "casa"}'
```

## 🛠️ Tecnologías Utilizadas

### Backend
- Django 6.0
- Django REST Framework
- Google Gemini AI (google-genai)
- SQLite

### Frontend
- React 18
- Vite
- Axios (llamadas HTTP)
- Web Speech API (reconocimiento de voz)

## ⚠️ Solución de Problemas

### Backend

**Error: "Tenant or user not found" (PostgreSQL/Supabase)**
- Solución: Cambié la configuración a SQLite en `settings.py`
- SQLite es más simple para desarrollo local

**Warning: "google.generativeai deprecated"**
- Solución: Actualizado a `google-genai` (nuevo paquete oficial)

**Error 404 en la raíz `/`**
- Esto es normal - usa las rutas `/api/juego1/`, `/api/juego2/`, `/api/oracion/`

### Frontend

**Pantalla en blanco**
- Verifica que el servidor esté corriendo: `npm run dev`
- Revisa la consola del navegador (F12) por errores
- Asegúrate de que todos los componentes existen

**Error: "Module not found"**
- Ejecuta: `npm install`
- Verifica que todos los archivos de componentes existan

### Versión de Node.js

**Warning: "Vite requires Node.js version..."**
- Actualiza Node.js a 22.12+ o 20.19+
- Descarga desde: https://nodejs.org/

## 📝 Notas de Desarrollo

1. **Base de datos**: Actualmente usa SQLite para simplificar el desarrollo. Los datos se resetean al borrar `db.sqlite3`.

2. **Google Gemini API**: 
   - Límite gratuito: ~20 peticiones/día
   - Si se excede, devuelve una oración predeterminada

3. **CORS**: Habilitado para todos los orígenes en desarrollo. En producción, configurar dominios específicos.

4. **Reconocimiento de voz**: Funciona mejor en Google Chrome (usa Web Speech API).

## 👨‍💻 Comandos Útiles

```bash
# Ver migraciones pendientes
python manage.py showmigrations

# Crear superusuario para el admin
python manage.py createsuperuser

# Acceder al admin de Django
# http://127.0.0.1:8000/admin/

# Ver logs del servidor en tiempo real
# (ya se muestran automáticamente con runserver)

# Verificar instalación de paquetes
pip list
npm list --depth=0
```

## 📚 Documentación Adicional

- [backend.md](./backend.md) - Detalles del backend Django
- [frontend.md](./frontend.md) - Detalles del frontend React

## 🤝 Contribuir

Para agregar nuevas palabras al juego:
1. Accede al admin: `http://127.0.0.1:8000/admin/`
2. Agrega registros en `PalabraModo1` (anagramas) o `PalabraModo2` (sílabas)

---

**Autor**: Maximiliano Madrid  
**Fecha**: Enero 2026  
**Proyecto**: POLI - Usabilidad

