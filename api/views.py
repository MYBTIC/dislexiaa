from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .models import PalabraModo1, PalabraModo2
from .serializers import PalabraModo1Serializer, PalabraModo2Serializer
import json
import random
import requests
from io import BytesIO
from PIL import Image
import base64

# Importar Google Generative AI de forma segura
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    genai = None  # Definir como None si no está disponible
    GENAI_AVAILABLE = False
    print("⚠️ Google Generative AI no disponible. Usando datos de respaldo.")

# ========== PALABRAS GARANTIZADAS (SIN VALIDACIÓN IA) ==========
# Estas 10 palabras tienen imágenes verificadas manualmente y NO requieren validación con IA
PALABRAS_GARANTIZADAS = {
    "gato": {
        "imagen": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=400&fit=crop",
        "silabas": ["ga", "to"]
    },
    "perro": {
        "imagen": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=400&fit=crop",
        "silabas": ["pe", "rro"]
    },
    "casa": {
        "imagen": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=400&h=400&fit=crop",
        "silabas": ["ca", "sa"]
    },
    "flor": {
        "imagen": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400&h=400&fit=crop",
        "silabas": ["flor"]
    },
    "sol": {
        "imagen": "https://images.unsplash.com/photo-1496450681664-3df85efbd29f?w=400&h=400&fit=crop",
        "silabas": ["sol"]
    },
    "luna": {
        "imagen": "https://images.unsplash.com/photo-1532693322450-2cb5c511067d?w=400&h=400&fit=crop",
        "silabas": ["lu", "na"]
    },
    "mesa": {
        "imagen": "https://images.unsplash.com/photo-1530018607912-eff2daa1bac4?w=400&h=400&fit=crop",
        "silabas": ["me", "sa"]
    },
    "libro": {
        "imagen": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&h=400&fit=crop",
        "silabas": ["li", "bro"]
    },
    "manzana": {
        "imagen": "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400&h=400&fit=crop",
        "silabas": ["man", "za", "na"]
    },
    "arbol": {
        "imagen": "https://images.unsplash.com/photo-1541516160071-4bb0c5af65ba?w=400&h=400&fit=crop",
        "silabas": ["ar", "bol"]
    }
}

# Configurar Gemini
def get_gemini_client():
    """Obtiene el cliente de Gemini configurado"""
    if not GENAI_AVAILABLE:
        return None

    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if api_key and api_key.strip():
        try:
            genai.configure(api_key=api_key)
            return genai  # Retorna el módulo configurado
        except Exception as e:
            print(f"⚠️ Error configurando Gemini: {e}")
            return None
    return None

def validar_imagen_con_palabra(client, imagen_url, palabra):
    """
    Valida que una imagen corresponda a la palabra usando Gemini Vision.
    Retorna True si coincide, False si no.
    VALIDACIÓN MUY RIGUROSA - No acepta aproximaciones.
    """
    try:
        # Descargar la imagen
        response = requests.get(imagen_url, timeout=15)
        if response.status_code != 200:
            print(f"❌ Error descargando imagen para '{palabra}': HTTP {response.status_code}")
            return False

        # Crear prompt de validación ULTRA ESTRICTO con ejemplos específicos
        prompt = f"""Eres un validador EXTREMADAMENTE RIGUROSO de imágenes para educación infantil.

TAREA: Determina si esta imagen muestra un/una {palabra.upper()} de manera INEQUÍVOCA.

⚠️ REGLAS CRÍTICAS - NO HAY EXCEPCIONES:

1. Responde "SI" SOLO si puedes identificar CLARAMENTE y SIN DUDAS un/una {palabra}
2. Responde "NO" si hay CUALQUIER duda o si muestra algo diferente
3. NO aceptes animales similares (ej: si busco ZORRO, un FLAMENCO es NO)
4. NO aceptes objetos relacionados pero diferentes (ej: si busco PELOTA, una MOCHILA es NO)
5. La imagen debe mostrar EXACTAMENTE lo que dice la palabra, no algo parecido
6. Si la imagen está borrosa, lejana o no es clara → NO

📋 EJEMPLOS DE VALIDACIÓN ESTRICTA:
- Palabra: "zorro" → Veo un FLAMENCO → Respuesta: NO
- Palabra: "zorro" → Veo un ZORRO → Respuesta: SI
- Palabra: "pelota" → Veo una MOCHILA → Respuesta: NO
- Palabra: "pelota" → Veo una PELOTA → Respuesta: SI
- Palabra: "gato" → Veo un PERRO → Respuesta: NO
- Palabra: "gato" → Veo un GATO → Respuesta: SI
- Palabra: "elefante" → Veo un RINOCERONTE → Respuesta: NO
- Palabra: "caballo" → Veo una CEBRA → Respuesta: NO

🎯 INSTRUCCIONES FINALES:
- Analiza la imagen con MÁXIMA ATENCIÓN
- Identifica QUÉ EXACTAMENTE muestra la imagen
- Compara con la palabra "{palabra}"
- Si NO coinciden EXACTAMENTE → NO
- Si coinciden perfectamente → SI

Responde ÚNICAMENTE con: SI o NO (una sola palabra, nada más)"""

        # Guardar imagen temporalmente
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(response.content)
            tmp_path = tmp_file.name

        # Subir imagen a Gemini usando el nuevo API
        uploaded_file = client.files.upload(path=tmp_path)

        # Usar Gemini Vision con temperatura baja para respuestas consistentes
        vision_response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=[uploaded_file, prompt],
            config=types.GenerateContentConfig(
                temperature=0.1,  # Baja temperatura para consistencia
                top_p=0.8,
            )
        )

        # Limpiar archivo temporal
        import os
        os.unlink(tmp_path)

        respuesta = vision_response.text.strip().upper()
        es_valida = "SI" in respuesta or "YES" in respuesta

        # Log detallado de la validación
        resultado = '✅ VÁLIDA' if es_valida else '❌ INVÁLIDA'
        print(f"🔍 Validación para '{palabra}': {respuesta} → {resultado}")

        return es_valida

    except Exception as e:
        print(f"❌ Error validando imagen para '{palabra}': {e}")
        return False


def obtener_imagen_validada_del_diccionario(client, palabra):
    """
    Obtiene una imagen validada del diccionario estático IMAGENES_UNSPLASH.
    Valida CADA imagen antes de aceptarla.
    Retorna la primera imagen que pase la validación o None.
    """
    if palabra not in IMAGENES_UNSPLASH:
        print(f"⚠️ Palabra '{palabra}' no está en el diccionario de imágenes")
        return None

    urls_disponibles = IMAGENES_UNSPLASH[palabra]

    # Asegurar que sea una lista
    if isinstance(urls_disponibles, str):
        urls_disponibles = [urls_disponibles]

    print(f"\n🔍 Validando imágenes del diccionario para '{palabra}' ({len(urls_disponibles)} disponibles)...")

    # Probar cada imagen del diccionario
    for idx, url in enumerate(urls_disponibles, 1):
        print(f"   Probando imagen {idx}/{len(urls_disponibles)}...")

        try:
            if validar_imagen_con_palabra(client, url, palabra):
                print(f"   ✅ ¡Imagen {idx} VALIDADA para '{palabra}'!")
                return url
            else:
                print(f"   ❌ Imagen {idx} NO coincide con '{palabra}', probando siguiente...")
        except Exception as e:
            print(f"   ⚠️ Error validando imagen {idx}: {e}")
            continue

    print(f"❌ Ninguna imagen del diccionario pasó la validación para '{palabra}'")
    return None


def buscar_imagen_validada_unsplash(client, palabra, max_intentos=5):
    """
    Busca una imagen en Unsplash que realmente corresponda a la palabra.
    Usa IA para validar cada imagen antes de aceptarla.
    Retorna la URL de la imagen validada o None si no encuentra ninguna.
    """
    try:
        # Traducir búsquedas comunes para mejorar resultados
        terminos_busqueda = {
            'pelota': ['soccer ball', 'football ball', 'sports ball'],
            'gato': ['cat face', 'domestic cat', 'kitten'],
            'perro': ['dog face', 'puppy dog', 'domestic dog'],
            'casa': ['small house', 'cottage', 'home exterior'],
            'mesa': ['wooden table', 'dining table', 'furniture table'],
            'zapato': ['shoe', 'sneaker', 'footwear'],
            'pato': ['duck bird', 'mallard duck'],
            'conejo': ['rabbit bunny', 'cute rabbit'],
            'elefante': ['elephant', 'african elephant'],
            'caballo': ['horse', 'brown horse'],
            'pajaro': ['bird', 'songbird'],
            'pez': ['fish', 'goldfish'],
            'leon': ['lion', 'male lion'],
            'tigre': ['tiger', 'bengal tiger'],
            'oso': ['bear', 'brown bear'],
            'mariposa': ['butterfly', 'colorful butterfly'],
            'tortuga': ['turtle', 'tortoise'],
            'vaca': ['cow', 'dairy cow'],
            'gallina': ['chicken', 'hen'],
            'oveja': ['sheep', 'lamb'],
            'zorro': ['fox', 'red fox', 'wild fox'],
            'lobo': ['wolf', 'gray wolf', 'wild wolf'],
            'mono': ['monkey', 'primate'],
            'jirafa': ['giraffe', 'tall giraffe'],
            'cebra': ['zebra', 'striped zebra'],
            'hipopotamo': ['hippopotamus', 'hippo'],
            'rinoceronte': ['rhinoceros', 'rhino'],
            'cocodrilo': ['crocodile', 'alligator'],
            'serpiente': ['snake', 'serpent'],
            'aguila': ['eagle', 'bald eagle'],
            'buho': ['owl', 'barn owl'],
            'cisne': ['swan', 'white swan'],
            'delfin': ['dolphin', 'bottlenose dolphin'],
            'ballena': ['whale', 'blue whale'],
            'tiburon': ['shark', 'great white shark'],
            'sol': ['sun', 'sunset sun', 'sunrise'],
            'luna': ['moon', 'full moon'],
            'flor': ['flower', 'blooming flower'],
            'estrella': ['star', 'night stars'],
            'nube': ['cloud', 'white cloud'],
            'arbol': ['tree', 'oak tree'],
            'montana': ['mountain', 'mountain peak'],
            'rio': ['river', 'flowing river'],
            'playa': ['beach', 'sandy beach'],
            'mar': ['ocean', 'sea water'],
            'manzana': ['apple', 'red apple'],
            'pan': ['bread', 'fresh bread'],
            'agua': ['water', 'glass of water'],
            'leche': ['milk', 'glass of milk'],
            'queso': ['cheese', 'yellow cheese'],
            'naranja': ['orange fruit', 'orange citrus'],
            'platano': ['banana', 'yellow banana'],
            'uva': ['grapes', 'grape bunch'],
            'pera': ['pear', 'green pear'],
            'sandia': ['watermelon', 'watermelon slice'],
            'ventana': ['window', 'open window'],
            'silla': ['chair', 'wooden chair'],
        }

        palabra_normalizada = palabra.lower().strip()
        terminos = terminos_busqueda.get(palabra_normalizada, [palabra])

        print(f"\n🔍 Buscando imagen validada para '{palabra}'...")

        for termino in terminos:
            print(f"  → Probando término de búsqueda: '{termino}'")

            # Buscar en Unsplash (usando IDs aleatorios de búsqueda)
            # Nota: Unsplash requiere API key para búsquedas, por ahora usamos URLs directas
            # pero con validación IA
            base_urls = [
                f"https://source.unsplash.com/400x400/?{termino.replace(' ', ',')}",
                f"https://source.unsplash.com/featured/400x400/?{termino.replace(' ', ',')}",
            ]

            for intento, base_url in enumerate(base_urls):
                if intento >= max_intentos:
                    break

                # Agregar timestamp para obtener diferentes imágenes
                import time
                url_con_cache = f"{base_url}&t={int(time.time())}{intento}"

                print(f"    → Intento {intento + 1}: Validando imagen...")

                # Validar la imagen con IA
                if validar_imagen_con_palabra(client, url_con_cache, palabra):
                    print(f"    ✅ ¡Imagen VÁLIDA encontrada para '{palabra}'!")
                    # Obtener la URL final después de la redirección
                    try:
                        final_response = requests.get(url_con_cache, timeout=10, allow_redirects=True)
                        return final_response.url
                    except:
                        return url_con_cache

        print(f"  ❌ No se encontró imagen válida para '{palabra}' después de {max_intentos} intentos")
        return None

    except Exception as e:
        print(f"Error buscando imagen para '{palabra}': {e}")
        return None

def obtener_palabras_validadas(client, cantidad, tipo_juego='anagrama'):
    """
    Genera palabras con VALIDACIÓN RIGUROSA de imágenes usando IA.
    Valida TODAS las imágenes antes de aceptarlas para evitar errores.
    """
    max_intentos = 8  # Aumentamos intentos para compensar validación estricta
    palabras_validas = []

    for intento in range(max_intentos):
        if len(palabras_validas) >= cantidad:
            break

        # Generar palabras según el tipo de juego
        if tipo_juego == 'anagrama':
            palabras_candidatas = generar_palabras_anagrama_raw(client, cantidad)
        else:  # silabas
            palabras_candidatas = generar_palabras_silabas_raw(client, cantidad)

        for palabra_data in palabras_candidatas:
            if len(palabras_validas) >= cantidad:
                break

            nombre = palabra_data['nombre'].lower().strip()

            # Intentar obtener imagen VALIDADA del diccionario
            imagen_validada = obtener_imagen_validada_del_diccionario(client, nombre)

            if imagen_validada:
                # Imagen del diccionario pasó la validación rigurosa
                palabra_data['imagen'] = imagen_validada
                palabra_data['validada'] = True
                palabras_validas.append(palabra_data)
                print(f"✅ Palabra '{nombre}' agregada con imagen VALIDADA del diccionario")
            else:
                # Si no hay imagen válida en el diccionario, buscar en Unsplash
                print(f"🔍 Buscando imagen alternativa en Unsplash para '{nombre}'...")
                imagen_unsplash = buscar_imagen_validada_unsplash(client, nombre, max_intentos=3)

                if imagen_unsplash:
                    palabra_data['imagen'] = imagen_unsplash
                    palabra_data['validada'] = True
                    palabras_validas.append(palabra_data)
                    print(f"✅ Palabra '{nombre}' agregada con imagen de Unsplash VALIDADA")
                else:
                    print(f"❌ No se pudo validar ninguna imagen para '{nombre}', saltando...")

    return palabras_validas

def generar_palabras_anagrama_raw(client, cantidad):
    """
    Genera palabras para anagrama seleccionando ALEATORIAMENTE del pool disponible.
    NO usa IA para evitar repetición - selección 100% aleatoria.
    """
    # Pool completo de palabras disponibles (las que tienen imágenes)
    palabras_disponibles = [
        # Animales variados
        "pato", "conejo", "elefante", "caballo", "pajaro", "pez", "leon", "tigre",
        "oso", "mariposa", "tortuga", "vaca", "gallina", "oveja", "lobo", "zorro",
        "mono", "jirafa", "cebra", "delfin", "foca", "rana", "abeja",
        # Objetos variados
        "pelota", "zapato", "ventana", "silla", "puerta", "reloj", "libro", "lapiz",
        "cama", "sofa", "lampara", "espejo", "llave", "vaso", "plato", "taza",
        "bolsa", "caja", "peine", "jabon",
        # Naturaleza
        "estrella", "nube", "arbol", "montana", "rio", "playa", "mar", "lago",
        "bosque", "roca", "arena", "tierra", "cielo", "viento", "lluvia", "nieve",
        # Alimentos
        "manzana", "pan", "agua", "leche", "queso", "naranja", "platano", "uva",
        "pera", "sandia", "fresa", "limon", "mango", "carne", "pollo", "huevo",
        "arroz", "sopa", "jugo", "miel"
    ]

    # Filtrar solo palabras que existen en IMAGENES_UNSPLASH
    palabras_con_imagen = [p for p in palabras_disponibles if p in IMAGENES_UNSPLASH]

    # Seleccionar aleatoriamente
    palabras_seleccionadas = random.sample(palabras_con_imagen, min(cantidad, len(palabras_con_imagen)))

    # Convertir a formato esperado
    resultado = [{"nombre": palabra} for palabra in palabras_seleccionadas]

    print(f"✅ Palabras seleccionadas aleatoriamente: {[p['nombre'] for p in resultado]}")

    return resultado

def dividir_en_silabas_simple(palabra):
    """
    Divide una palabra en sílabas de forma simple.
    Reglas básicas del español.
    """
    # Diccionario de divisiones conocidas (más confiable)
    silabas_conocidas = {
        "pato": ["pa", "to"],
        "conejo": ["co", "ne", "jo"],
        "elefante": ["e", "le", "fan", "te"],
        "caballo": ["ca", "ba", "llo"],
        "pajaro": ["pa", "ja", "ro"],
        "pez": ["pez"],
        "leon": ["le", "on"],
        "tigre": ["ti", "gre"],
        "oso": ["o", "so"],
        "mariposa": ["ma", "ri", "po", "sa"],
        "tortuga": ["tor", "tu", "ga"],
        "vaca": ["va", "ca"],
        "gallina": ["ga", "lli", "na"],
        "oveja": ["o", "ve", "ja"],
        "lobo": ["lo", "bo"],
        "zorro": ["zo", "rro"],
        "mono": ["mo", "no"],
        "jirafa": ["ji", "ra", "fa"],
        "cebra": ["ce", "bra"],
        "delfin": ["del", "fin"],
        "foca": ["fo", "ca"],
        "rana": ["ra", "na"],
        "abeja": ["a", "be", "ja"],
        "pelota": ["pe", "lo", "ta"],
        "zapato": ["za", "pa", "to"],
        "ventana": ["ven", "ta", "na"],
        "silla": ["si", "lla"],
        "puerta": ["puer", "ta"],
        "reloj": ["re", "loj"],
        "libro": ["li", "bro"],
        "lapiz": ["la", "piz"],
        "cama": ["ca", "ma"],
        "sofa": ["so", "fa"],
        "lampara": ["lam", "pa", "ra"],
        "espejo": ["es", "pe", "jo"],
        "llave": ["lla", "ve"],
        "vaso": ["va", "so"],
        "plato": ["pla", "to"],
        "taza": ["ta", "za"],
        "bolsa": ["bol", "sa"],
        "caja": ["ca", "ja"],
        "peine": ["pei", "ne"],
        "jabon": ["ja", "bon"],
        "estrella": ["es", "tre", "lla"],
        "nube": ["nu", "be"],
        "arbol": ["ar", "bol"],
        "montana": ["mon", "ta", "na"],
        "rio": ["ri", "o"],
        "playa": ["pla", "ya"],
        "mar": ["mar"],
        "lago": ["la", "go"],
        "bosque": ["bos", "que"],
        "roca": ["ro", "ca"],
        "arena": ["a", "re", "na"],
        "tierra": ["tie", "rra"],
        "cielo": ["cie", "lo"],
        "viento": ["vien", "to"],
        "lluvia": ["llu", "via"],
        "nieve": ["nie", "ve"],
        "manzana": ["man", "za", "na"],
        "pan": ["pan"],
        "agua": ["a", "gua"],
        "leche": ["le", "che"],
        "queso": ["que", "so"],
        "naranja": ["na", "ran", "ja"],
        "platano": ["pla", "ta", "no"],
        "uva": ["u", "va"],
        "pera": ["pe", "ra"],
        "sandia": ["san", "di", "a"],
        "fresa": ["fre", "sa"],
        "limon": ["li", "mon"],
        "mango": ["man", "go"],
        "carne": ["car", "ne"],
        "pollo": ["po", "llo"],
        "huevo": ["hue", "vo"],
        "arroz": ["a", "rroz"],
        "sopa": ["so", "pa"],
        "jugo": ["ju", "go"],
        "miel": ["miel"],
    }

    return silabas_conocidas.get(palabra.lower(), [palabra])

def generar_opciones_silaba(silaba_correcta):
    """Genera 3 opciones incorrectas similares a la sílaba correcta"""
    vocales = ['a', 'e', 'i', 'o', 'u']
    consonantes = ['b', 'c', 'd', 'f', 'g', 'j', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'z']

    opciones = [silaba_correcta]

    # Generar 3 variaciones
    for _ in range(3):
        if len(silaba_correcta) == 1:
            # Para sílabas de 1 letra, cambiar por otra vocal o consonante
            if silaba_correcta in vocales:
                nueva = random.choice([v for v in vocales if v != silaba_correcta])
            else:
                nueva = random.choice([c for c in consonantes if c != silaba_correcta])
        else:
            # Para sílabas más largas, cambiar la vocal
            nueva = list(silaba_correcta)
            for i, char in enumerate(nueva):
                if char in vocales:
                    nueva[i] = random.choice([v for v in vocales if v != char])
                    break
            nueva = ''.join(nueva)

        if nueva not in opciones:
            opciones.append(nueva)

    # Asegurar que tengamos exactamente 4 opciones
    while len(opciones) < 4:
        opciones.append(silaba_correcta + random.choice(vocales))

    return opciones[:4]

def generar_palabras_silabas_raw(client, cantidad):
    """
    Genera palabras para sílabas seleccionando ALEATORIAMENTE del pool disponible.
    NO usa IA - división silábica desde diccionario conocido.
    """
    # Pool de palabras con 2-4 sílabas
    palabras_disponibles = [
        "pato", "conejo", "elefante", "caballo", "pajaro", "leon", "tigre", "oso",
        "mariposa", "tortuga", "vaca", "gallina", "oveja", "lobo", "zorro", "mono",
        "jirafa", "cebra", "delfin", "foca", "rana", "abeja",
        "pelota", "zapato", "ventana", "silla", "puerta", "reloj", "libro", "lapiz",
        "cama", "sofa", "lampara", "espejo", "llave", "vaso", "plato", "taza",
        "bolsa", "caja", "peine", "jabon",
        "estrella", "nube", "arbol", "montana", "rio", "playa", "lago",
        "bosque", "roca", "arena", "tierra", "cielo", "viento", "lluvia", "nieve",
        "manzana", "leche", "queso", "naranja", "platano", "uva", "pera",
        "sandia", "fresa", "limon", "mango", "carne", "pollo", "huevo",
        "sopa", "jugo"
    ]

    # Filtrar solo palabras que existen en IMAGENES_UNSPLASH
    palabras_con_imagen = [p for p in palabras_disponibles if p in IMAGENES_UNSPLASH]

    # Seleccionar aleatoriamente
    palabras_seleccionadas = random.sample(palabras_con_imagen, min(cantidad, len(palabras_con_imagen)))

    # Generar estructura completa
    resultado = []
    for palabra in palabras_seleccionadas:
        silabas = dividir_en_silabas_simple(palabra)

        # Seleccionar una sílaba para ocultar (evitar la primera si es muy corta)
        if len(silabas) == 1:
            silaba_oculta_idx = 0
        else:
            # Preferir sílabas del medio o final
            silaba_oculta_idx = random.randint(0, len(silabas) - 1)

        silaba_correcta = silabas[silaba_oculta_idx]
        opciones = generar_opciones_silaba(silaba_correcta)
        random.shuffle(opciones)

        resultado.append({
            "nombre": palabra,
            "silabas": silabas,
            "silaba_oculta": silaba_oculta_idx,
            "opciones": opciones
        })

    print(f"✅ Palabras de sílabas seleccionadas: {[p['nombre'] for p in resultado]}")

    return resultado


def obtener_imagen_palabra(palabra, client=None):
    """
    Obtiene la URL de imagen para una palabra con variación aleatoria.
    Confía en el mapeo directo para mejor performance.
    """
    # Normalizar la palabra (quitar tildes y convertir a minúsculas)
    palabra_normalizada = palabra.lower().strip()

    # Buscar en el mapeo directo
    if palabra_normalizada in IMAGENES_UNSPLASH:
        urls_disponibles = IMAGENES_UNSPLASH[palabra_normalizada]

        # Asegurar que sea una lista
        if not isinstance(urls_disponibles, list):
            urls_disponibles = [urls_disponibles]

        # Seleccionar aleatoriamente
        url_seleccionada = random.choice(urls_disponibles)
        print(f"✅ Imagen seleccionada para '{palabra}': {url_seleccionada[:60]}...")
        return url_seleccionada

    # Imagen de respaldo genérica
    print(f"⚠️ Palabra '{palabra}' no encontrada, usando imagen de respaldo")
    return "https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=400&h=400&fit=crop"

# Lista de categorías para palabras de niños
CATEGORIAS_PALABRAS = [
    "animales domésticos", "animales de granja", "frutas", "verduras",
    "colores", "juguetes", "partes del cuerpo", "ropa", "alimentos",
    "objetos de la casa", "medios de transporte", "naturaleza"
]

# Palabras de respaldo por si falla la API
PALABRAS_RESPALDO_ANAGRAMA = [
    {"nombre": "gato", "imagen": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400", "palabra_dividida_letras": "g-a-t-o"},
    {"nombre": "perro", "imagen": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400", "palabra_dividida_letras": "p-e-r-r-o"},
    {"nombre": "casa", "imagen": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=400", "palabra_dividida_letras": "c-a-s-a"},
    {"nombre": "mesa", "imagen": "https://images.unsplash.com/photo-1530018607912-eff2daa1bac4?w=400", "palabra_dividida_letras": "m-e-s-a"},
    {"nombre": "luna", "imagen": "https://images.unsplash.com/photo-1532693322450-2cb5c511067d?w=400", "palabra_dividida_letras": "l-u-n-a"},
    {"nombre": "sol", "imagen": "https://images.unsplash.com/photo-1496450681664-3df85efbd29f?w=400", "palabra_dividida_letras": "s-o-l"},
    {"nombre": "flor", "imagen": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400", "palabra_dividida_letras": "f-l-o-r"},
    {"nombre": "pato", "imagen": "https://images.unsplash.com/photo-1459682687441-7761439a709d?w=400", "palabra_dividida_letras": "p-a-t-o"},
]

PALABRAS_RESPALDO_SILABAS = [
    {"nombre": "mariposa", "imagen": "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=400", "silabas": ["ma", "ri", "po", "sa"], "silaba_oculta": 2, "opciones": ["po", "pe", "pa", "pi"]},
    {"nombre": "elefante", "imagen": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=400", "silabas": ["e", "le", "fan", "te"], "silaba_oculta": 1, "opciones": ["le", "la", "lo", "li"]},
    {"nombre": "conejo", "imagen": "https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400", "silabas": ["co", "ne", "jo"], "silaba_oculta": 1, "opciones": ["ne", "na", "no", "ni"]},
    {"nombre": "tortuga", "imagen": "https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f?w=400", "silabas": ["tor", "tu", "ga"], "silaba_oculta": 2, "opciones": ["ga", "go", "gu", "ge"]},
    {"nombre": "pelota", "imagen": "https://images.unsplash.com/photo-1614632537197-38a17061c2bd?w=400", "silabas": ["pe", "lo", "ta"], "silaba_oculta": 1, "opciones": ["lo", "la", "le", "lu"]},
    {"nombre": "zapato", "imagen": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400", "silabas": ["za", "pa", "to"], "silaba_oculta": 0, "opciones": ["za", "ze", "zo", "zu"]},
    {"nombre": "caballo", "imagen": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400", "silabas": ["ca", "ba", "llo"], "silaba_oculta": 1, "opciones": ["ba", "be", "bi", "bo"]},
    {"nombre": "ventana", "imagen": "https://images.unsplash.com/photo-1509644851169-2acc08aa25b5?w=400", "silabas": ["ven", "ta", "na"], "silaba_oculta": 2, "opciones": ["na", "ne", "no", "nu"]},
]

# Mapeo de palabras a MÚLTIPLES URLs de Unsplash para variación aleatoria
# Cada palabra tiene una lista de 3-5 imágenes diferentes
IMAGENES_UNSPLASH = {
    # Animales
    "gato": [
        "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1529778873920-4da4926a72c2?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1495360010541-f48722b34f7d?w=400&h=400&fit=crop",
    ],
    "perro": [
        "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1561037404-61cd46aa615b?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?w=400&h=400&fit=crop",
    ],
    "pato": [
        "https://images.unsplash.com/photo-1459682687441-7761439a709d?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1551969014-7d2c4cddf0b6?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1598928506311-c55ded91a20c?w=400&h=400&fit=crop",
    ],
    "conejo": [
        "https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1535241749838-299277b6305f?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1547844312-cbe0b3cb3110?w=400&h=400&fit=crop",
    ],
    "elefante": [
        "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1564760055775-d63b17a55c44?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1591825729269-caeb344f6df2?w=400&h=400&fit=crop",
    ],
    "caballo": [
        "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1534773252187-74b5e7c90b0f?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1551563386-d1bc8b1e5f0e?w=400&h=400&fit=crop",
    ],
    "pájaro": [
        "https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1605460375648-278bcbd579a6?w=400&h=400&fit=crop",
    ],
    "pajaro": [
        "https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1605460375648-278bcbd579a6?w=400&h=400&fit=crop",
    ],
    "pez": [
        "https://images.unsplash.com/photo-1524704654690-b56c05c78a00?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1520990659643-2168a55647d4?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1535591273668-578e31182c4f?w=400&h=400&fit=crop",
    ],
    "león": [
        "https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1614027164847-1b28cfe1df60?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1534188753412-5e94d27b5f2c?w=400&h=400&fit=crop",
    ],
    "leon": [
        "https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1614027164847-1b28cfe1df60?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1534188753412-5e94d27b5f2c?w=400&h=400&fit=crop",
    ],
    "tigre": [
        "https://images.unsplash.com/photo-1551492910-2f0acb2e8115?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1564349683136-77e08dba1ef7?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1615963244664-5b845b2025ee?w=400&h=400&fit=crop",
    ],
    "oso": [
        "https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?w=400&h=400&fit=crop",
    ],
    "mariposa": [
        "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1534625279866-1242e4e8f066?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1594735962322-e52f6581f994?w=400&h=400&fit=crop",
    ],
    "tortuga": [
        "https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1591825729269-caeb344f6df2?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1516574187841-cb9cc2ca948b?w=400&h=400&fit=crop",
    ],
    "vaca": [
        "https://images.unsplash.com/photo-1560493676-04071c5f467b?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1544980919-e17526d4ed0a?w=400&h=400&fit=crop",
    ],
    "gallina": [
        "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1596278422672-0610a7447e79?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1563281577-a7be47e20db9?w=400&h=400&fit=crop",
    ],
    "oveja": [
        "https://images.unsplash.com/photo-1551913902-c92207b5dc7c?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1584267385494-9fdd9a71ad75?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1533318087102-b3ad366ed041?w=400&h=400&fit=crop",
    ],
    # Objetos
    "casa": [
        "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400&h=400&fit=crop",
    ],
    "mesa": [
        "https://images.unsplash.com/photo-1530018607912-eff2daa1bac4?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1533090161767-e6ffed986c88?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1551298370-9d3d53740c72?w=400&h=400&fit=crop",
    ],
    "pelota": [
        "https://images.unsplash.com/photo-1614632537197-38a17061c2bd?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1575361204480-aadea25e6e68?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1551958219-acbc608c6377?w=400&h=400&fit=crop",
    ],
    "zapato": [
        "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=400&h=400&fit=crop",
    ],
    "ventana": [
        "https://images.unsplash.com/photo-1509644851169-2acc08aa25b5?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1545146695-36d61a8f7f93?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=400&h=400&fit=crop",
    ],
    "silla": [
        "https://images.unsplash.com/photo-1503602642458-232111445657?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1506439773649-6e0eb8cfb237?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1581539250439-c96689b516dd?w=400&h=400&fit=crop",
    ],
    # Naturaleza
    "sol": [
        "https://images.unsplash.com/photo-1496450681664-3df85efbd29f?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1503803548695-c2a7b4a5b875?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1591123120675-6f7f1aae0e5b?w=400&h=400&fit=crop",
    ],
    "luna": [
        "https://images.unsplash.com/photo-1532693322450-2cb5c511067d?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1509973867816-372f2c7c1c01?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1550596334-7bb40a71b905?w=400&h=400&fit=crop",
    ],
    "flor": [
        "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1597848212624-e530bb8f8db5?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1508610048659-a06b669e3321?w=400&h=400&fit=crop",
    ],
    "estrella": [
        "https://images.unsplash.com/photo-1519810755548-39cd217da494?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1472120435266-53107fd0c44a?w=400&h=400&fit=crop",
    ],
    "nube": [
        "https://images.unsplash.com/photo-1534088568595-a066f410bcda?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1513002749550-c59d786b8e6c?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1527004013197-933c4bb611b3?w=400&h=400&fit=crop",
    ],
    "árbol": [
        "https://images.unsplash.com/photo-1541516160071-4bb0c5af65ba?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=400&h=400&fit=crop",
    ],
    "arbol": [
        "https://images.unsplash.com/photo-1541516160071-4bb0c5af65ba?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=400&h=400&fit=crop",
    ],
    "montaña": [
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=400&h=400&fit=crop",
    ],
    "montana": [
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=400&h=400&fit=crop",
    ],
    "río": [
        "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1520106212299-d99c443e4568?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=400&h=400&fit=crop",
    ],
    "rio": [
        "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1520106212299-d99c443e4568?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=400&h=400&fit=crop",
    ],
    "playa": [
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400&h=400&fit=crop",
    ],
    "mar": [
        "https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1484821582734-6c6c9f99a672?w=400&h=400&fit=crop",
    ],
    # Alimentos
    "manzana": [
        "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1619546813926-a78fa6372cd2?w=400&h=400&fit=crop",
    ],
    "pan": [
        "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1585478259715-876acc5be8eb?w=400&h=400&fit=crop",
    ],
    "agua": [
        "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1603126857599-f6e157fa2fe6?w=400&h=400&fit=crop",
    ],
    "leche": [
        "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1628088062854-d1870b4553da?w=400&h=400&fit=crop",
    ],
    "queso": [
        "https://images.unsplash.com/photo-1452195100486-9cc805987862?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1618164436241-4473940d1f5c?w=400&h=400&fit=crop",
    ],
    "naranja": [
        "https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1557800636-894a64c1696f?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1582979512210-99b6a53386f9?w=400&h=400&fit=crop",
    ],
    "plátano": [
        "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1603833665858-e61d17a86224?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1528825871115-3581a5387919?w=400&h=400&fit=crop",
    ],
    "platano": [
        "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1603833665858-e61d17a86224?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1528825871115-3581a5387919?w=400&h=400&fit=crop",
    ],
    "uva": [
        "https://images.unsplash.com/photo-1596363505729-4190a9506133?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1599819177032-c8c1f49e74be?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1601275177229-7f937c2e2c5b?w=400&h=400&fit=crop",
    ],
    "pera": [
        "https://images.unsplash.com/photo-1568570935644-e9c96a60b7f2?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1587049352846-4a222e784422?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1514995669114-6081e934b693?w=400&h=400&fit=crop",
    ],
    "sandía": [
        "https://images.unsplash.com/photo-1589984662646-e7b2e4962f18?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1563114773-84221bd62daa?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1582281298055-e25b2a3deab6?w=400&h=400&fit=crop",
    ],
    "sandia": [
        "https://images.unsplash.com/photo-1589984662646-e7b2e4962f18?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1563114773-84221bd62daa?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1582281298055-e25b2a3deab6?w=400&h=400&fit=crop",
    ],
    # ========== NUEVAS PALABRAS PARA MAYOR VARIEDAD ==========
    # Más animales
    "lobo": [
        "https://images.unsplash.com/photo-1550355191-aa8a80b41353?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1614027164847-1b28cfe1df60?w=400&h=400&fit=crop",
    ],
    "zorro": [
        "https://images.unsplash.com/photo-1474511320723-9a56873867b5?w=400&h=400&fit=crop",  # Red fox closeup
        "https://images.unsplash.com/photo-1516642067569-e16a752c9f49?w=400&h=400&fit=crop",  # Red fox portrait
        "https://images.unsplash.com/photo-1500993855538-c6a99f437aa7?w=400&h=400&fit=crop",  # Fox in nature
    ],
    "mono": [
        "https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1503066211613-c17ebc9daef0?w=400&h=400&fit=crop",
    ],
    "jirafa": [
        "https://images.unsplash.com/photo-1547721064-da6cfb341d50?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1534567110243-e85d34cb820e?w=400&h=400&fit=crop",
    ],
    "cebra": [
        "https://images.unsplash.com/photo-1523731404588-d4a93b0873cd?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=400&h=400&fit=crop",
    ],
    "delfin": [
        "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1535859619928-2c155b9926d0?w=400&h=400&fit=crop",
    ],
    "foca": [
        "https://images.unsplash.com/photo-1555685812-4b943f1cb0eb?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1581579438747-1dc8d17bbce4?w=400&h=400&fit=crop",
    ],
    "rana": [
        "https://images.unsplash.com/photo-1503844401201-e0086ac5c59e?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1588192968807-f1c08d50296d?w=400&h=400&fit=crop",
    ],
    "abeja": [
        "https://images.unsplash.com/photo-1558642084-fd07fae5282e?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1563299796-17596ed6b017?w=400&h=400&fit=crop",
    ],
    # Más objetos
    "puerta": [
        "https://images.unsplash.com/photo-1545447824-412a622952d0?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1523755231516-e43fd2e8dca5?w=400&h=400&fit=crop",
    ],
    "reloj": [
        "https://images.unsplash.com/photo-1509048191080-d2984bad6ae5?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1495364141860-b0d03eccd065?w=400&h=400&fit=crop",
    ],
    "libro": [
        "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=400&fit=crop",
    ],
    "lapiz": [
        "https://images.unsplash.com/photo-1587107862403-b33867c4f42e?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1587907274552-d63e799a5d40?w=400&h=400&fit=crop",
    ],
    "cama": [
        "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=400&h=400&fit=crop",
    ],
    "sofa": [
        "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=400&fit=crop",
    ],
    "lampara": [
        "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1524484485831-a92ffc0de03f?w=400&h=400&fit=crop",
    ],
    "espejo": [
        "https://images.unsplash.com/photo-1618220179428-22790b461013?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=400&h=400&fit=crop",
    ],
    "llave": [
        "https://images.unsplash.com/photo-1582139329536-e7284fece509?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1580752300992-559f8e0734e0?w=400&h=400&fit=crop",
    ],
    "vaso": [
        "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1541537904654-6da3e7e45465?w=400&h=400&fit=crop",
    ],
    "plato": [
        "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1589236342032-66bac72e0aa6?w=400&h=400&fit=crop",
    ],
    "taza": [
        "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?w=400&h=400&fit=crop",
    ],
    "bolsa": [
        "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=400&fit=crop",
    ],
    # Más naturaleza
    "lago": [
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=400&h=400&fit=crop",
    ],
    "bosque": [
        "https://images.unsplash.com/photo-1511497584788-876760111969?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?w=400&h=400&fit=crop",
    ],
    "roca": [
        "https://images.unsplash.com/photo-1494891848038-7bd202a2afeb?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=400&h=400&fit=crop",
    ],
    "arena": [
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=400&h=400&fit=crop",
    ],
    "tierra": [
        "https://images.unsplash.com/photo-1470115636492-6d2b56f9146d?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1425913397330-cf8af2ff40a1?w=400&h=400&fit=crop",
    ],
    "cielo": [
        "https://images.unsplash.com/photo-1534088568595-a066f410bcda?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1517483000871-1dbf64a6e1c6?w=400&h=400&fit=crop",
    ],
    "viento": [
        "https://images.unsplash.com/photo-1500497138177-5406823a2a57?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1527004013197-933c4bb611b3?w=400&h=400&fit=crop",
    ],
    "lluvia": [
        "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1513002749550-c59d786b8e6c?w=400&h=400&fit=crop",
    ],
    "nieve": [
        "https://images.unsplash.com/photo-1491002052546-bf38f186af56?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1478030213993-8e440a1e5858?w=400&h=400&fit=crop",
    ],
    # Más alimentos
    "fresa": [
        "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1518635017498-87f514b751ba?w=400&h=400&fit=crop",
    ],
    "limon": [
        "https://images.unsplash.com/photo-1590502593747-42a996133562?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1587486937476-8c7b19ebe252?w=400&h=400&fit=crop",
    ],
    "mango": [
        "https://images.unsplash.com/photo-1553279768-865429fa0078?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1601493700631-2b16ec4b4716?w=400&h=400&fit=crop",
    ],
    "carne": [
        "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1603048297172-c92544798d5a?w=400&h=400&fit=crop",
    ],
    "pollo": [
        "https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=400&h=400&fit=crop",
    ],
    "huevo": [
        "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1506976785307-8732e854ad03?w=400&h=400&fit=crop",
    ],
    "arroz": [
        "https://images.unsplash.com/photo-1516684732162-798a0062be99?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?w=400&h=400&fit=crop",
    ],
    "sopa": [
        "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=400&h=400&fit=crop",
    ],
    "jugo": [
        "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1622597467836-f3c423641b5c?w=400&h=400&fit=crop",
    ],
    "miel": [
        "https://images.unsplash.com/photo-1587049352846-4a222e784422?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1558642084-fd07fae5282e?w=400&h=400&fit=crop",
    ],
}


@api_view(['GET'])
def juego_anagrama(request):
    """Genera palabras aleatorias para el juego de anagramas usando palabras garantizadas"""
    # Obtener cantidad desde query params, por defecto 3
    cantidad = int(request.GET.get('cantidad', 3))
    # Limitar entre 2 y 8 palabras
    cantidad = max(2, min(8, cantidad))

    try:
        # USAR PALABRAS GARANTIZADAS DIRECTAMENTE (sin validación IA)
        print("🔥 Usando PALABRAS GARANTIZADAS (sin validación IA)...")

        # Seleccionar palabras aleatorias del pool garantizado
        palabras_disponibles = list(PALABRAS_GARANTIZADAS.keys())
        palabras_seleccionadas = random.sample(palabras_disponibles, min(cantidad, len(palabras_disponibles)))

        palabras_procesadas = []
        for nombre in palabras_seleccionadas:
            palabra_data = PALABRAS_GARANTIZADAS[nombre]
            palabras_procesadas.append({
                "nombre": nombre,
                "imagen": palabra_data["imagen"],
                "palabra_dividida_letras": "-".join(list(nombre))
            })
            print(f"✅ Palabra '{nombre}' agregada (GARANTIZADA)")

        return Response(palabras_procesadas)

    except Exception as e:
        print(f"❌ Error en juego_anagrama: {e}")
        # Fallback adicional usando palabras de respaldo
        palabras_respaldo = random.sample(PALABRAS_RESPALDO_ANAGRAMA, min(cantidad, len(PALABRAS_RESPALDO_ANAGRAMA)))
        for palabra in palabras_respaldo:
            nombre = palabra['nombre']
            if nombre in IMAGENES_UNSPLASH:
                urls_disponibles = IMAGENES_UNSPLASH[nombre]
                if isinstance(urls_disponibles, list):
                    palabra['imagen'] = random.choice(urls_disponibles)
                else:
                    palabra['imagen'] = urls_disponibles
        return Response(palabras_respaldo)


@api_view(['GET'])
def juego_silabas(request):
    """Genera palabras aleatorias para el juego de sílabas usando palabras garantizadas"""
    # Obtener cantidad desde query params, por defecto 3
    cantidad = int(request.GET.get('cantidad', 3))
    # Limitar entre 2 y 8 palabras
    cantidad = max(2, min(8, cantidad))

    try:
        # USAR PALABRAS GARANTIZADAS DIRECTAMENTE (sin validación IA)
        print("🔥 Usando PALABRAS GARANTIZADAS para sílabas (sin validación IA)...")

        # Seleccionar palabras aleatorias del pool garantizado
        palabras_disponibles = list(PALABRAS_GARANTIZADAS.keys())
        palabras_seleccionadas = random.sample(palabras_disponibles, min(cantidad, len(palabras_disponibles)))

        palabras_procesadas = []
        for nombre in palabras_seleccionadas:
            palabra_data = PALABRAS_GARANTIZADAS[nombre]
            silabas = palabra_data["silabas"]

            # Seleccionar una sílaba aleatoria para ocultar
            silaba_oculta_idx = random.randint(0, len(silabas) - 1)
            silaba_correcta = silabas[silaba_oculta_idx]

            # Generar opciones incorrectas
            opciones_pool = ["ba", "ca", "da", "fa", "ga", "ja", "la", "ma", "na", "pa", "ra", "sa", "ta", "va", "za",
                           "be", "ce", "de", "fe", "ge", "je", "le", "me", "ne", "pe", "re", "se", "te", "ve", "ze",
                           "bi", "ci", "di", "fi", "gi", "ji", "li", "mi", "ni", "pi", "ri", "si", "ti", "vi", "zi",
                           "bo", "co", "do", "fo", "go", "jo", "lo", "mo", "no", "po", "ro", "so", "to", "vo", "zo",
                           "bu", "cu", "du", "fu", "gu", "ju", "lu", "mu", "nu", "pu", "ru", "su", "tu", "vu", "zu"]

            # Filtrar opciones que no estén en las sílabas de la palabra
            opciones_incorrectas = [op for op in opciones_pool if op not in silabas and op != silaba_correcta]
            opciones = [silaba_correcta] + random.sample(opciones_incorrectas, min(3, len(opciones_incorrectas)))
            random.shuffle(opciones)

            palabras_procesadas.append({
                "nombre": nombre,
                "imagen": palabra_data["imagen"],
                "silabas": silabas,
                "silaba_oculta": silaba_oculta_idx,
                "opciones": opciones
            })
            print(f"✅ Palabra '{nombre}' agregada (GARANTIZADA) - sílabas: {silabas}")

        return Response(palabras_procesadas)

    except Exception as e:
        print(f"❌ Error en juego_silabas: {e}")
        # Fallback adicional usando palabras de respaldo
        palabras_respaldo = random.sample(PALABRAS_RESPALDO_SILABAS, min(cantidad, len(PALABRAS_RESPALDO_SILABAS)))
        for palabra in palabras_respaldo:
            nombre = palabra['nombre']
            if nombre in IMAGENES_UNSPLASH:
                urls_disponibles = IMAGENES_UNSPLASH[nombre]
                if isinstance(urls_disponibles, list):
                    palabra['imagen'] = random.choice(urls_disponibles)
                else:
                    palabra['imagen'] = urls_disponibles
        return Response(palabras_respaldo)


@api_view(['POST'])
def generar_oracion(request):
    """Genera una oración usando la palabra proporcionada"""
    palabra = request.data.get('palabra')

    if not palabra:
        return Response({'error': 'No se proporcionó una palabra'}, status=400)

    try:
        client = get_gemini_client()
        if not client:
            raise ValueError("Gemini API key not configured")

        prompt = f"""Genera UNA SOLA oración simple, natural, LÓGICA y CREATIVA para un niño de 7 años que incluya la palabra: {palabra}

REGLAS IMPORTANTES:
- La oración debe tener entre 5 y 10 palabras
- Usa un lenguaje claro y sencillo apropiado para niños
- Utiliza correctamente los artículos (el/la/un/una) según el género de la palabra
- La oración debe describir características REALES y VERDADERAS de la palabra
- USA SENTIDO COMÚN: describe la palabra con atributos que realmente tenga
- NO uses signos de exclamación, comas ni puntos al final
- Asegúrate de que la gramática sea perfecta
- La oración debe sonar natural cuando un niño la lea en voz alta
- SÉ CREATIVO: intenta crear una oración DIFERENTE cada vez, usando distintos contextos, acciones y descripciones
- VARÍA el tipo de oración: a veces descriptiva, a veces de acción, a veces de ubicación

IMPORTANTE - COHERENCIA LÓGICA:
- Si es un animal lento (tortuga, caracol), NO digas que es rápido
- Si es un animal rápido (conejo, león), NO digas que es lento
- Si vuela (pájaro, mariposa), menciona que vuela
- Si nada (pez, ballena), menciona que nada
- Usa las características VERDADERAS de cada cosa

IMPORTANTE - CREATIVIDAD Y VARIEDAD:
- NO repitas siempre las mismas frases genéricas
- Intenta usar verbos diferentes (corre, salta, brilla, vuela, nada, duerme, juega, come, etc.)
- Varía los adjetivos (bonito, grande, rápido, lento, hermoso, dulce, etc.)
- Cambia el contexto (en casa, en el parque, en el jardín, en el cielo, etc.)

Ejemplos de oraciones CORRECTAS con sentido común y variedad:
- "El gato duerme tranquilo en su cama" ✓
- "La mariposa vuela entre las flores del jardín" ✓
- "La tortuga camina despacio por el jardín" ✓ (tortugas son lentas)
- "El conejo salta muy rápido" ✓ (conejos son rápidos)
- "El sol brilla en el cielo azul" ✓
- "Mi perro mueve la cola feliz" ✓
- "La luna ilumina la noche oscura" ✓

Ejemplos de oraciones INCORRECTAS (NO hacer):
- "La tortuga corre muy rápido" ✗ (las tortugas son lentas)
- "El caracol es muy veloz" ✗ (los caracoles son lentos)
- "El pez camina en el parque" ✗ (los peces nadan)

Responde SOLO con la oración, sin texto adicional."""

        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt
        )

        # Limpiar la respuesta
        oracion = response.text.strip()
        # Remover puntos finales si los hay
        oracion = oracion.rstrip('.,!?')

        return Response({'oracion': oracion})

    except Exception as e:
        # Sistema inteligente de oraciones de respaldo
        print(f"Error generando oración: {e}")

        # Diccionario de oraciones específicas con sentido común para cada palabra
        oraciones_especificas = {
            # Animales rápidos
            'gato': [
                "El gato duerme tranquilo en su cama",
                "Mi gato juega con una pelota",
                "El gato salta sobre la mesa",
                "Veo un gato que camina en el jardín",
                "El gato ronronea cuando está feliz",
                "Mi gato negro descansa en el sofá",
                "El gato lame sus patas con cuidado",
                "Un gato pequeño sube al árbol",
                "El gato persigue a una mariposa"
            ],
            'perro': [
                "El perro corre rápido en el parque",
                "Mi perro mueve la cola cuando me ve",
                "El perro ladra cuando alguien llega",
                "Veo un perro que juega con su pelota",
                "El perro es el mejor amigo del hombre",
                "Mi perro café corre en el jardín",
                "El perro salta de alegría al verme",
                "Un perro grande cuida la casa",
                "El perro juega con los niños"
            ],
            'conejo': [
                "El conejo salta muy rápido",
                "Mi conejo come zanahorias",
                "El conejo tiene orejas largas",
                "Veo un conejo blanco en el jardín",
                "El conejo se esconde en su madriguera",
                "Mi conejo mueve su nariz sin parar",
                "El conejo salta entre las flores",
                "Un conejo pequeño busca comida"
            ],
            'caballo': [
                "El caballo corre muy rápido",
                "Mi caballo galopa en el campo",
                "El caballo es grande y fuerte",
                "Veo un caballo café en la granja",
                "El caballo come pasto fresco",
                "Mi caballo relincha por la mañana",
                "El caballo trota por el camino",
                "Un caballo hermoso corre libre"
            ],
            # Animales lentos
            'tortuga': [
                "La tortuga camina despacio por el jardín",
                "Mi tortuga nada en el agua",
                "La tortuga tiene un caparazón duro",
                "Veo una tortuga que descansa al sol",
                "La tortuga se mueve lentamente",
                "Mi tortuga verde come lechuga",
                "La tortuga se esconde en su caparazón",
                "Una tortuga vieja vive en el estanque"
            ],
            # Animales que vuelan
            'pájaro': [
                "El pájaro vuela alto en el cielo",
                "Mi pájaro canta en su jaula",
                "El pájaro tiene plumas de colores",
                "Veo un pájaro en el árbol",
                "El pájaro construye su nido",
                "Mi pájaro amarillo canta feliz",
                "El pájaro vuela de rama en rama",
                "Un pájaro pequeño busca comida"
            ],
            'pajaro': [
                "El pájaro vuela alto en el cielo",
                "Mi pájaro canta en su jaula",
                "El pájaro tiene plumas de colores",
                "Veo un pájaro en el árbol",
                "El pájaro construye su nido",
                "Mi pájaro amarillo canta feliz",
                "El pájaro vuela de rama en rama",
                "Un pájaro pequeño busca comida"
            ],
            'mariposa': [
                "La mariposa vuela entre las flores",
                "Mi mariposa tiene alas de colores",
                "La mariposa se posa en una flor",
                "Veo una mariposa bonita en el jardín",
                "La mariposa vuela libremente",
                "Mi mariposa naranja es hermosa",
                "La mariposa busca flores dulces",
                "Una mariposa colorida pasa volando"
            ],
            # Animales que nadan
            'pez': [
                "El pez nada en el agua",
                "Mi pez vive en la pecera",
                "El pez tiene escamas brillantes",
                "Veo un pez de colores nadando",
                "El pez nada rápido en el río",
                "Mi pez dorado es muy bonito",
                "El pez busca comida en el agua",
                "Un pez pequeño nada feliz"
            ],
            # Otros animales
            'pato': [
                "El pato nada en el lago",
                "Mi pato hace cuac cuac",
                "El pato tiene plumas amarillas",
                "Veo un pato nadando en el agua",
                "El pato busca comida en el estanque",
                "Mi pato blanco es muy gracioso",
                "El pato camina junto al lago",
                "Un pato grande nada con sus patitos"
            ],
            'elefante': [
                "El elefante es grande y fuerte",
                "Mi elefante tiene trompa larga",
                "El elefante vive en la selva",
                "Veo un elefante en el zoológico",
                "El elefante usa su trompa para beber",
                "Mi elefante gris es enorme",
                "El elefante camina con pasos grandes",
                "Un elefante viejo descansa bajo un árbol"
            ],
            'león': [
                "El león es el rey de la selva",
                "Mi león ruge muy fuerte",
                "El león corre rápido cuando caza",
                "Veo un león descansando",
                "El león tiene una melena hermosa",
                "Mi león dorado es poderoso",
                "El león protege a su familia",
                "Un león grande camina con orgullo"
            ],
            'leon': [
                "El león es el rey de la selva",
                "Mi león ruge muy fuerte",
                "El león corre rápido cuando caza",
                "Veo un león descansando",
                "El león tiene una melena hermosa",
                "Mi león dorado es poderoso",
                "El león protege a su familia",
                "Un león grande camina con orgullo"
            ],
            'tigre': [
                "El tigre tiene rayas negras",
                "Mi tigre corre muy rápido",
                "El tigre es un cazador poderoso",
                "Veo un tigre en la selva",
                "El tigre ruge en la noche",
                "Mi tigre naranja es hermoso",
                "El tigre camina sigilosamente",
                "Un tigre grande descansa en las rocas"
            ],
            'oso': [
                "El oso es grande y peludo",
                "Mi oso duerme en el invierno",
                "El oso come miel del panal",
                "Veo un oso en el bosque",
                "El oso camina con paso pesado",
                "Mi oso café es muy fuerte",
                "El oso busca peces en el río",
                "Un oso grande protege a sus crías"
            ],
            'vaca': [
                "La vaca nos da leche",
                "Mi vaca come pasto en el campo",
                "La vaca hace muuu",
                "Veo una vaca en la granja",
                "La vaca descansa bajo la sombra",
                "Mi vaca blanca y negra es linda",
                "La vaca pasea por el prado",
                "Una vaca grande mastica el pasto"
            ],
            'gallina': [
                "La gallina pone huevos",
                "Mi gallina cacarea en el corral",
                "La gallina tiene plumas suaves",
                "Veo una gallina con sus pollitos",
                "La gallina busca comida en el suelo",
                "Mi gallina roja es muy bonita",
                "La gallina cuida a sus pollitos",
                "Una gallina grande pasea en la granja"
            ],
            'oveja': [
                "La oveja tiene lana suave",
                "Mi oveja bala en el campo",
                "La oveja come pasto verde",
                "Veo una oveja blanca en el prado",
                "La oveja nos da lana para abrigos",
                "Mi oveja esponjosa es tierna",
                "La oveja camina con el rebaño",
                "Una oveja pequeña juega en el campo"
            ],
            # Naturaleza
            'sol': [
                "El sol brilla en el cielo",
                "El sol nos da luz y calor",
                "El sol sale todas las mañanas",
                "Veo el sol muy brillante hoy",
                "El sol calienta la tierra",
                "Mi sol favorito sale temprano",
                "El sol ilumina todo el día",
                "Un sol dorado aparece al amanecer"
            ],
            'luna': [
                "La luna brilla en la noche",
                "La luna sale cuando oscurece",
                "La luna es redonda y blanca",
                "Veo la luna en el cielo nocturno",
                "La luna ilumina la noche oscura",
                "Mi luna favorita está llena",
                "La luna se refleja en el agua",
                "Una luna plateada brilla suavemente"
            ],
            'flor': [
                "La flor huele muy rico",
                "Mi flor tiene pétalos de colores",
                "La flor crece en el jardín",
                "Veo una flor roja muy bonita",
                "La flor atrae a las abejas",
                "Mi flor favorita es la rosa",
                "La flor se abre con el sol",
                "Una flor hermosa perfuma el aire"
            ],
            'estrella': [
                "La estrella brilla en la noche",
                "Mi estrella favorita está en el cielo",
                "La estrella titila muy bonito",
                "Veo muchas estrellas en la noche",
                "La estrella ilumina el cielo oscuro",
                "Mi estrella brillante es hermosa",
                "La estrella parpadea en el firmamento",
                "Una estrella fugaz cruza el cielo"
            ],
            'arbol': [
                "El árbol da sombra en verano",
                "Mi árbol tiene hojas verdes",
                "El árbol crece muy alto",
                "Veo un árbol grande en el parque",
                "El árbol da frutos en otoño",
                "Mi árbol favorito tiene flores",
                "El árbol se mueve con el viento",
                "Un árbol viejo da mucha sombra"
            ],
            'nube': [
                "La nube flota en el cielo",
                "Mi nube es blanca y esponjosa",
                "La nube trae lluvia",
                "Veo una nube con forma de animal",
                "La nube se mueve con el viento",
                "Mi nube favorita parece algodón",
                "La nube cubre el sol",
                "Una nube grande pasa volando"
            ],
            # Alimentos
            'manzana': [
                "La manzana es roja y dulce",
                "Mi manzana está muy rica",
                "La manzana es mi fruta favorita",
                "Como una manzana en el recreo",
                "La manzana es jugosa y fresca",
                "Mi manzana verde es deliciosa",
                "La manzana crece en el árbol",
                "Una manzana roja brilla en el plato"
            ],
            'pan': [
                "El pan está caliente y suave",
                "Mi pan huele muy rico",
                "El pan es mi alimento favorito",
                "Como pan con mantequilla",
                "El pan recién horneado es delicioso",
                "Mi pan dorado está crujiente",
                "El pan me da mucha energía",
                "Un pan fresco sale del horno"
            ],
            'naranja': [
                "La naranja es dulce y jugosa",
                "Mi naranja tiene mucha vitamina",
                "La naranja es de color anaranjado",
                "Como una naranja cada mañana",
                "La naranja me refresca mucho",
                "Mi naranja favorita es muy dulce",
                "La naranja tiene un olor rico",
                "Una naranja madura está deliciosa"
            ],
            'platano': [
                "El plátano es amarillo y suave",
                "Mi plátano está muy maduro",
                "El plátano me da energía",
                "Como un plátano en el desayuno",
                "El plátano es fácil de pelar",
                "Mi plátano favorito está dulce",
                "El plátano crece en racimos",
                "Un plátano maduro es delicioso"
            ],
            # Objetos
            'casa': [
                "La casa es donde vivo",
                "Mi casa tiene ventanas grandes",
                "La casa me protege del frío",
                "Veo una casa bonita en la calle",
                "La casa tiene un jardín hermoso",
                "Mi casa es cómoda y caliente",
                "La casa tiene techo rojo",
                "Una casa nueva se ve muy linda"
            ],
            'mesa': [
                "La mesa está en el comedor",
                "Mi mesa es de madera",
                "La mesa tiene cuatro patas",
                "Veo una mesa con comida",
                "La mesa es donde comemos",
                "Mi mesa redonda es muy bonita",
                "La mesa está limpia y ordenada",
                "Una mesa grande cabe en la sala"
            ],
            'pelota': [
                "La pelota rebota muy alto",
                "Mi pelota es de color azul",
                "La pelota rueda por el piso",
                "Juego con una pelota en el parque",
                "La pelota es redonda y suave",
                "Mi pelota favorita es la de fútbol",
                "La pelota vuela cuando la pateo",
                "Una pelota nueva brilla mucho"
            ],
            'silla': [
                "La silla es para sentarse",
                "Mi silla es cómoda",
                "La silla está junto a la mesa",
                "Veo una silla de madera",
                "La silla tiene cuatro patas",
                "Mi silla favorita es la roja",
                "La silla me ayuda a descansar",
                "Una silla nueva llegó a casa"
            ],
            'ventana': [
                "La ventana deja entrar la luz",
                "Mi ventana da al jardín",
                "La ventana tiene vidrio transparente",
                "Veo las nubes por la ventana",
                "La ventana se abre para ventilar",
                "Mi ventana favorita es la grande",
                "La ventana me permite ver afuera",
                "Una ventana limpia brilla mucho"
            ],
            'zapato': [
                "El zapato protege mis pies",
                "Mi zapato es muy cómodo",
                "El zapato tiene cordones largos",
                "Veo un zapato nuevo en la tienda",
                "El zapato me queda perfecto",
                "Mi zapato favorito es el deportivo",
                "El zapato está limpio y brillante",
                "Un zapato rojo me gusta mucho"
            ],
        }

        # Si existe oración específica, usarla
        palabra_lower = palabra.lower()
        if palabra_lower in oraciones_especificas:
            return Response({
                'oracion': random.choice(oraciones_especificas[palabra_lower])
            })

        # Diccionario de palabras comunes con su género
        palabras_femeninas = {
            'casa', 'mesa', 'flor', 'luna', 'pelota', 'mariposa',
            'tortuga', 'ventana', 'silla', 'manzana', 'pera', 'uva',
            'estrella', 'nube', 'montaña', 'playa', 'vaca', 'gallina',
            'oveja', 'abeja', 'hormiga', 'araña', 'rana', 'ballena'
        }

        # Determinar género
        es_femenina = palabra.lower().endswith('a') or palabra.lower() in palabras_femeninas
        articulo_def = 'la' if es_femenina else 'el'
        articulo_indef = 'una' if es_femenina else 'un'
        adjetivo_bonito = 'bonita' if es_femenina else 'bonito'
        adjetivo_favorito = 'favorita' if es_femenina else 'favorito'
        adjetivo_nuevo = 'nueva' if es_femenina else 'nuevo'
        adjetivo_hermoso = 'hermosa' if es_femenina else 'hermoso'
        adjetivo_delicioso = 'deliciosa' if es_femenina else 'delicioso'
        adjetivo_rico = 'rica' if es_femenina else 'rico'

        # Plantillas genéricas (solo para palabras sin oraciones específicas)
        oraciones_animales = [
            f"Veo {articulo_indef} {palabra} en el jardín",
            f"Mi {palabra} {adjetivo_favorito} vive cerca de mi casa",
            f"Me gusta observar a {articulo_def} {palabra}",
            f"{articulo_def.capitalize()} {palabra} es muy {adjetivo_bonito}",
            f"Tengo {articulo_indef} {palabra} en casa",
            f"{articulo_def.capitalize()} {palabra} come todos los días",
            f"Vi {articulo_indef} {palabra} en el parque",
            f"Mi amigo tiene {articulo_indef} {palabra}",
            f"{articulo_def.capitalize()} {palabra} descansa en la sombra",
            f"Me encanta {articulo_def} {palabra} que vi ayer"
        ]

        oraciones_objetos = [
            f"Tengo {articulo_indef} {palabra} {adjetivo_bonito} en mi cuarto",
            f"Mi mamá me compró {articulo_indef} {palabra} {adjetivo_nuevo}",
            f"{articulo_def.capitalize()} {palabra} está sobre la mesa",
            f"Me gusta jugar con mi {palabra}",
            f"Veo {articulo_indef} {palabra} de color azul",
            f"Mi {palabra} {adjetivo_favorito} está aquí",
            f"Encontré {articulo_indef} {palabra} en la tienda",
            f"{articulo_def.capitalize()} {palabra} es muy útil",
            f"Uso mi {palabra} todos los días",
            f"Quiero {articulo_indef} {palabra} {adjetivo_nuevo}"
        ]

        oraciones_naturaleza = [
            f"{articulo_def.capitalize()} {palabra} brilla en el cielo",
            f"Miro {articulo_def} {palabra} desde mi ventana",
            f"Me encanta {articulo_def} {palabra} de la mañana",
            f"{articulo_def.capitalize()} {palabra} es {adjetivo_hermoso} hoy",
            f"Dibujé {articulo_indef} {palabra} en mi cuaderno",
            f"Veo {articulo_def} {palabra} cada día",
            f"{articulo_def.capitalize()} {palabra} me gusta mucho",
            f"Observo {articulo_def} {palabra} con atención",
            f"{articulo_def.capitalize()} {palabra} aparece en el cielo",
            f"Me fascina {articulo_def} {palabra} {adjetivo_hermoso}"
        ]

        oraciones_alimentos = [
            f"Me gusta comer {palabra} en el desayuno",
            f"{articulo_def.capitalize()} {palabra} está muy {adjetivo_rico}",
            f"Mi mamá prepara {palabra} {adjetivo_delicioso}",
            f"Compré {articulo_indef} {palabra} en el mercado",
            f"{articulo_def.capitalize()} {palabra} es mi {adjetivo_favorito}",
            f"Como {palabra} todos los días",
            f"{articulo_def.capitalize()} {palabra} me da energía",
            f"Me encanta {articulo_def} {palabra} fresco",
            f"Probé {articulo_indef} {palabra} {adjetivo_delicioso}",
            f"{articulo_def.capitalize()} {palabra} sabe muy bien"
        ]

        # Intentar categorizar la palabra
        palabra_lower = palabra.lower()

        if palabra_lower in ['gato', 'perro', 'pato', 'conejo', 'elefante', 'caballo',
                             'pájaro', 'pez', 'león', 'tigre', 'oso', 'mariposa',
                             'tortuga', 'vaca', 'gallina', 'oveja']:
            oraciones_pool = oraciones_animales
        elif palabra_lower in ['sol', 'luna', 'estrella', 'nube', 'flor', 'árbol',
                               'montaña', 'río', 'playa', 'mar']:
            oraciones_pool = oraciones_naturaleza
        elif palabra_lower in ['manzana', 'pan', 'agua', 'leche', 'queso', 'naranja',
                               'plátano', 'uva', 'pera', 'sandía']:
            oraciones_pool = oraciones_alimentos
        else:
            oraciones_pool = oraciones_objetos

        return Response({
            'oracion': random.choice(oraciones_pool),
            'info': 'Oración generada automáticamente'
        })
