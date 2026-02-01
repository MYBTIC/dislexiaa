# Backend - Django REST API

## 🚀 Instalación y configuración

### 1. Configurar el entorno virtual e instalar dependencias

```bash
# 1. Crear el entorno virtual (solo la primera vez)
python -m venv .venv

# 2. Activar entorno (Windows PowerShell)
.venv\Scripts\Activate.ps1
# (Windows CMD)
.venv\Scripts\activate.bat
# (GitBash)
source .venv/Scripts/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar la API de Google Gemini (OPCIONAL)

La aplicación puede funcionar sin API key usando palabras y oraciones de respaldo. Si quieres usar la generación dinámica con IA:

1. **Obtén tu API key** en [Google AI Studio](https://makersuite.google.com/app/apikey)

2. **Configura la key** en `Dislexia/settings.py`:
   ```python
   GEMINI_API_KEY = 'tu-api-key-aqui'
   ```

**Nota:** Sin API key configurada, el sistema usará automáticamente palabras y oraciones predefinidas. La aplicación funcionará perfectamente.

### 3. Ejecutar migraciones y servidor

```bash
# 4. Ejecutar migraciones (solo la primera vez o después de cambios en modelos)
python manage.py migrate

# 5. Iniciar el servidor de desarrollo
python manage.py runserver
```

## 📋 Endpoints disponibles

El servidor corre en: `http://127.0.0.1:8000/`

### 🎮 Juego de Anagramas
```
GET http://127.0.0.1:8000/api/juego1/?cantidad=3
```
Devuelve palabras aleatorias para el modo anagrama.
- **Parámetro opcional:** `cantidad` (2-8, por defecto 3)

### 🔤 Juego de Sílabas
```
GET http://127.0.0.1:8000/api/juego2/?cantidad=3
```
Devuelve palabras aleatorias para el modo sílabas.
- **Parámetro opcional:** `cantidad` (2-8, por defecto 3)
- **Mejora reciente:** Imágenes verificadas y consistentes con URLs directas de Unsplash

### 💬 Generar Oración (mejorado con IA + Coherencia Lógica)
```
POST http://127.0.0.1:8000/api/oracion/
Content-Type: application/json

{
  "palabra": "gato"
}
```
Genera una oración simple, natural, gramaticalmente correcta **y lógicamente coherente** para niños usando Google Gemini AI.

**Características:**
- ✅ Gramática perfecta con artículos correctos (el/la/un/una)
- ✅ **Concordancia de género perfecta** (favorita/favorito, nueva/nuevo, hermosa/hermoso, etc.)
- ✅ **COHERENCIA LÓGICA** - Usa características reales de cada palabra
- ✅ **23+ palabras con oraciones específicas verificadas** manualmente
- ✅ Lenguaje apropiado para niños de 7-12 años
- ✅ Oraciones de 5-10 palabras
- ✅ Sistema inteligente de respaldo con oraciones por categorías
- ✅ Detección automática de género de la palabra

**Ejemplos de coherencia lógica:**
- 🐢 "La tortuga camina despacio por el jardín" (tortugas son lentas)
- 🐇 "El conejo salta muy rápido" (conejos son rápidos)
- 🦋 "La mariposa vuela entre las flores" (mariposas vuelan)
- 🐠 "El pez nada en el agua" (peces nadan)
- ☀️ "El sol brilla en el cielo" (el sol da luz)

**Mejoras recientes:**
- ❌ Antes: "La tortuga corre muy rápido" (incorrecto)
- ✅ Ahora: "La tortuga camina despacio por el jardín" (correcto)

## 🎨 Sistema de Imágenes

El sistema ahora utiliza un **mapeo directo de URLs específicas de Unsplash** para garantizar que las imágenes coincidan exactamente con las palabras:

- **50+ palabras** con imágenes verificadas manualmente
- URLs directas con IDs específicos de Unsplash
- Incluye variantes con y sin tildes (ej: "león" y "leon")
- Imagen de respaldo genérica para palabras no mapeadas
- **Gemini genera las palabras, el backend asigna las imágenes correctas**

**Ventajas:**
- ✅ Imágenes consistentes y precisas
- ✅ No requiere API key adicional de Unsplash
- ✅ Carga rápida sin llamadas a APIs externas
- ✅ Fácil de expandir agregando más URLs al diccionario

## 🔧 Configuración

- **Base de datos**: SQLite (local, archivo `db.sqlite3`)
- **API Key de Gemini**: OPCIONAL - Configurable en `Dislexia/settings.py`
  - Con API key: Genera palabras y oraciones dinámicamente con IA
  - Sin API key: Usa palabras y oraciones predefinidas (funciona igual de bien)
- **CORS**: Habilitado para todos los orígenes (desarrollo)

## ⚠️ Notas importantes

1. **El proyecto funciona sin necesidad de configurar la API key de Gemini**
   - Si `GEMINI_API_KEY` está vacía, usa contenido de respaldo automáticamente
   - No afecta la funcionalidad del juego
2. La ruta raíz `/` no tiene contenido - es normal ver un 404
3. El admin de Django está en: `http://127.0.0.1:8000/admin/`
4. Todas las rutas de la API están bajo `/api/`
5. El límite de Google Gemini es ~20 peticiones diarias (versión gratuita)
