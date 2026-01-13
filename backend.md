```bash
# 1. Crear el entorno virtual (solo la primera vez)
python -m venv .venv

# 2. Activar entorno (Windows)
.venv\Scripts\activate
# (GitBash)
source .venv/Scripts/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Iniciar el servidor de desarrollo
python manage.py runserver
```