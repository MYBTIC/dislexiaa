# Backend - Django REST API

## 🚀 Instalación y configuración

```bash
# 1. Crear el entorno virtual (solo la primera vez)
python -m venv .venv

# 2. Activar entorno (Windows)
.venv\Scripts\activate
# (GitBash)
source .venv/Scripts/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar migraciones (solo la primera vez o después de cambios en modelos)
python manage.py migrate

# 5. Iniciar el servidor de desarrollo
python manage.py runserver
```

## 📋 Endpoints disponibles

El servidor corre en: `http://127.0.0.1:8000/`

### 🎮 Juego de Anagramas
```
GET http://127.0.0.1:8000/api/juego1/
```
Devuelve 2 palabras aleatorias para el modo anagrama.

### 🔤 Juego de Sílabas
```
GET http://127.0.0.1:8000/api/juego2/
```
Devuelve 1 palabra aleatoria para el modo sílabas.

### 💬 Generar Oración (con Gemini AI)
```
POST http://127.0.0.1:8000/api/oracion/
Content-Type: application/json

{
  "palabra": "casa"
}
```
Genera una oración simple usando Google Gemini AI con la palabra proporcionada.

## 🔧 Configuración

- **Base de datos**: SQLite (local, archivo `db.sqlite3`)
- **API Key de Gemini**: Configurada en `Dislexia/settings.py`
- **CORS**: Habilitado para todos los orígenes (desarrollo)

## ⚠️ Notas importantes

1. La ruta raíz `/` no tiene contenido - es normal ver un 404
2. El admin de Django está en: `http://127.0.0.1:8000/admin/`
3. Todas las rutas de la API están bajo `/api/`
4. El límite de Google Gemini es ~20 peticiones diarias (versión gratuita)
