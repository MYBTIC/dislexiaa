from django.shortcuts import render
from google import genai
from google.genai import types
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .models import PalabraModo1, PalabraModo2
from .serializers import PalabraModo1Serializer, PalabraModo2Serializer
import json
import random

# Configuramos el cliente de Gemini de forma lazy (solo cuando se necesite)
def get_gemini_client():
    """Obtiene el cliente de Gemini, solo si la API key está configurada"""
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if api_key and api_key.strip():
        return genai.Client(api_key=api_key)
    return None

def obtener_imagen_palabra(palabra):
    """
    Obtiene la URL de imagen para una palabra
    Usa el mapeo directo de URLs específicas de Unsplash
    """
    # Normalizar la palabra (quitar tildes y convertir a minúsculas)
    palabra_normalizada = palabra.lower().strip()

    # Buscar en el mapeo directo
    if palabra_normalizada in IMAGENES_UNSPLASH:
        return IMAGENES_UNSPLASH[palabra_normalizada]

    # Imagen de respaldo genérica
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
    {"nombre": "mariposa", "imagen": "https://images.unsplash.com/photo-1452570053594-1b985d6ea890?w=400", "silabas": ["ma", "ri", "po", "sa"], "silaba_oculta": 2, "opciones": ["po", "pe", "pa", "pi"]},
    {"nombre": "elefante", "imagen": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=400", "silabas": ["e", "le", "fan", "te"], "silaba_oculta": 1, "opciones": ["le", "la", "lo", "li"]},
    {"nombre": "conejo", "imagen": "https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400", "silabas": ["co", "ne", "jo"], "silaba_oculta": 1, "opciones": ["ne", "na", "no", "ni"]},
    {"nombre": "tortuga", "imagen": "https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f?w=400", "silabas": ["tor", "tu", "ga"], "silaba_oculta": 2, "opciones": ["ga", "go", "gu", "ge"]},
    {"nombre": "pelota", "imagen": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400", "silabas": ["pe", "lo", "ta"], "silaba_oculta": 1, "opciones": ["lo", "la", "le", "lu"]},
    {"nombre": "zapato", "imagen": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400", "silabas": ["za", "pa", "to"], "silaba_oculta": 0, "opciones": ["za", "ze", "zo", "zu"]},
    {"nombre": "caballo", "imagen": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400", "silabas": ["ca", "ba", "llo"], "silaba_oculta": 1, "opciones": ["ba", "be", "bi", "bo"]},
    {"nombre": "ventana", "imagen": "https://images.unsplash.com/photo-1509644851169-2acc08aa25b5?w=400", "silabas": ["ven", "ta", "na"], "silaba_oculta": 2, "opciones": ["na", "ne", "no", "nu"]},
]

# Mapeo de palabras a URLs específicas de Unsplash (IDs confiables)
IMAGENES_UNSPLASH = {
    # Animales
    "gato": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=400&fit=crop",
    "perro": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=400&fit=crop",
    "pato": "https://images.unsplash.com/photo-1459682687441-7761439a709d?w=400&h=400&fit=crop",
    "conejo": "https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=400&h=400&fit=crop",
    "elefante": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=400&h=400&fit=crop",
    "caballo": "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400&h=400&fit=crop",
    "pájaro": "https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=400&h=400&fit=crop",
    "pajaro": "https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=400&h=400&fit=crop",
    "pez": "https://images.unsplash.com/photo-1524704654690-b56c05c78a00?w=400&h=400&fit=crop",
    "león": "https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=400&h=400&fit=crop",
    "leon": "https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=400&h=400&fit=crop",
    "tigre": "https://images.unsplash.com/photo-1551492910-2f0acb2e8115?w=400&h=400&fit=crop",
    "oso": "https://images.unsplash.com/photo-1589656966895-2f33e7653819?w=400&h=400&fit=crop",
    "mariposa": "https://images.unsplash.com/photo-1452570053594-1b985d6ea890?w=400&h=400&fit=crop",
    "tortuga": "https://images.unsplash.com/photo-1437622368342-7a3d73a34c8f?w=400&h=400&fit=crop",
    "vaca": "https://images.unsplash.com/photo-1560493676-04071c5f467b?w=400&h=400&fit=crop",
    "gallina": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=400&h=400&fit=crop",
    "oveja": "https://images.unsplash.com/photo-1551913902-c92207b5dc7c?w=400&h=400&fit=crop",
    # Objetos
    "casa": "https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=400&h=400&fit=crop",
    "mesa": "https://images.unsplash.com/photo-1530018607912-eff2daa1bac4?w=400&h=400&fit=crop",
    "pelota": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop",
    "zapato": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop",
    "ventana": "https://images.unsplash.com/photo-1509644851169-2acc08aa25b5?w=400&h=400&fit=crop",
    "silla": "https://images.unsplash.com/photo-1503602642458-232111445657?w=400&h=400&fit=crop",
    # Naturaleza
    "sol": "https://images.unsplash.com/photo-1496450681664-3df85efbd29f?w=400&h=400&fit=crop",
    "luna": "https://images.unsplash.com/photo-1532693322450-2cb5c511067d?w=400&h=400&fit=crop",
    "flor": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400&h=400&fit=crop",
    "estrella": "https://images.unsplash.com/photo-1519810755548-39cd217da494?w=400&h=400&fit=crop",
    "nube": "https://images.unsplash.com/photo-1534088568595-a066f410bcda?w=400&h=400&fit=crop",
    "árbol": "https://images.unsplash.com/photo-1541516160071-4bb0c5af65ba?w=400&h=400&fit=crop",
    "arbol": "https://images.unsplash.com/photo-1541516160071-4bb0c5af65ba?w=400&h=400&fit=crop",
    "montaña": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=400&fit=crop",
    "montana": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=400&fit=crop",
    "río": "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=400&h=400&fit=crop",
    "rio": "https://images.unsplash.com/photo-1439066615861-d1af74d74000?w=400&h=400&fit=crop",
    "playa": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&h=400&fit=crop",
    "mar": "https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=400&h=400&fit=crop",
    # Alimentos
    "manzana": "https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=400&h=400&fit=crop",
    "pan": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=400&fit=crop",
    "agua": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=400&h=400&fit=crop",
    "leche": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400&h=400&fit=crop",
    "queso": "https://images.unsplash.com/photo-1452195100486-9cc805987862?w=400&h=400&fit=crop",
    "naranja": "https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?w=400&h=400&fit=crop",
    "plátano": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400&h=400&fit=crop",
    "platano": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400&h=400&fit=crop",
    "uva": "https://images.unsplash.com/photo-1596363505729-4190a9506133?w=400&h=400&fit=crop",
    "pera": "https://images.unsplash.com/photo-1568570935644-e9c96a60b7f2?w=400&h=400&fit=crop",
    "sandía": "https://images.unsplash.com/photo-1589984662646-e7b2e4962f18?w=400&h=400&fit=crop",
    "sandia": "https://images.unsplash.com/photo-1589984662646-e7b2e4962f18?w=400&h=400&fit=crop",
}


@api_view(['GET'])
def juego_anagrama(request):
    """Genera palabras aleatorias para el juego de anagramas usando Gemini"""
    # Obtener cantidad desde query params, por defecto 3
    cantidad = int(request.GET.get('cantidad', 3))
    # Limitar entre 2 y 8 palabras
    cantidad = max(2, min(8, cantidad))

    try:
        client = get_gemini_client()
        if not client:
            raise ValueError("Gemini API key not configured")

        categoria = random.choice(CATEGORIAS_PALABRAS)

        prompt = f"""Genera exactamente {cantidad} palabras en español para un juego educativo de niños de 7 años.
        Categoría: {categoria}

        REGLAS IMPORTANTES:
        - Palabras de 3 a 6 letras solamente
        - Sin tildes ni caracteres especiales
        - Palabras comunes que un niño conoce
        - Todas las letras en minúscula
        - Para cada palabra, proporciona un término de búsqueda en INGLÉS específico y preciso para encontrar la imagen correcta

        Responde SOLO con un JSON válido con este formato exacto, sin texto adicional:
        [
            {{"nombre": "gato", "imagen_busqueda": "cute kitten cat"}},
            {{"nombre": "perro", "imagen_busqueda": "cute puppy dog"}},
            {{"nombre": "manzana", "imagen_busqueda": "red apple fruit"}}
        ]
        
        IMPORTANTE: El término de búsqueda debe ser EN INGLÉS y muy específico para que la imagen coincida exactamente con la palabra.
        """

        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt
        )

        # Limpiar la respuesta
        texto = response.text.strip()
        if texto.startswith("```json"):
            texto = texto[7:]
        if texto.startswith("```"):
            texto = texto[3:]
        if texto.endswith("```"):
            texto = texto[:-3]
        texto = texto.strip()

        palabras_raw = json.loads(texto)

        # Procesar palabras y obtener imágenes
        palabras_procesadas = []
        for p in palabras_raw[:cantidad]:
            nombre = p['nombre'].lower().strip()

            # Obtener imagen del mapeo directo
            imagen_url = obtener_imagen_palabra(nombre)

            palabras_procesadas.append({
                "nombre": nombre,
                "imagen": imagen_url,
                "palabra_dividida_letras": "-".join(list(nombre))
            })

        return Response(palabras_procesadas)

    except Exception as e:
        print(f"Error en juego_anagrama: {e}")
        # Usar palabras de respaldo
        palabras = random.sample(PALABRAS_RESPALDO_ANAGRAMA, min(cantidad, len(PALABRAS_RESPALDO_ANAGRAMA)))
        return Response(palabras)


@api_view(['GET'])
def juego_silabas(request):
    """Genera palabras aleatorias para el juego de sílabas usando Gemini"""
    # Obtener cantidad desde query params, por defecto 3
    cantidad = int(request.GET.get('cantidad', 3))
    # Limitar entre 2 y 8 palabras
    cantidad = max(2, min(8, cantidad))

    try:
        client = get_gemini_client()
        if not client:
            raise ValueError("Gemini API key not configured")

        categoria = random.choice(CATEGORIAS_PALABRAS)

        prompt = f"""Genera exactamente {cantidad} palabras en español para un juego educativo de sílabas para niños de 7 años.
        Categoría: {categoria}

        REGLAS IMPORTANTES:
        - Palabras de 2 a 4 sílabas
        - Sin tildes ni caracteres especiales
        - Palabras comunes que un niño conoce
        - Todas las letras en minúscula
        - Para cada palabra, proporciona un término de búsqueda en INGLÉS específico y preciso para encontrar la imagen correcta

        Para cada palabra incluye:
        - Las sílabas separadas
        - El índice de una sílaba para ocultar (0, 1, 2...)
        - 4 opciones de sílabas (la correcta + 3 incorrectas similares)

        Responde SOLO con un JSON válido con este formato exacto, sin texto adicional:
        [
            {{
                "nombre": "mariposa",
                "imagen_busqueda": "colorful butterfly insect",
                "silabas": ["ma", "ri", "po", "sa"],
                "silaba_oculta": 2,
                "opciones": ["po", "pe", "pa", "pi"]
            }}
        ]
        
        IMPORTANTE: El término de búsqueda debe ser EN INGLÉS y muy específico para que la imagen coincida exactamente con la palabra.
        """

        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt
        )

        # Limpiar la respuesta
        texto = response.text.strip()
        if texto.startswith("```json"):
            texto = texto[7:]
        if texto.startswith("```"):
            texto = texto[3:]
        if texto.endswith("```"):
            texto = texto[:-3]
        texto = texto.strip()

        palabras_raw = json.loads(texto)

        # Procesar palabras y obtener imágenes
        palabras_procesadas = []
        for p in palabras_raw[:cantidad]:
            nombre = p['nombre'].lower().strip()

            # Obtener imagen del mapeo directo
            imagen_url = obtener_imagen_palabra(nombre)

            # Asegurar que las opciones incluyan la sílaba correcta
            silaba_correcta = p['silabas'][p['silaba_oculta']]
            opciones = p['opciones']
            if silaba_correcta not in opciones:
                opciones[0] = silaba_correcta
            random.shuffle(opciones)

            palabras_procesadas.append({
                "nombre": nombre,
                "imagen": imagen_url,
                "silabas": p['silabas'],
                "silaba_oculta": p['silaba_oculta'],
                "opciones": opciones
            })

        return Response(palabras_procesadas)

    except Exception as e:
        print(f"Error en juego_silabas: {e}")
        # Usar palabras de respaldo
        palabras = random.sample(PALABRAS_RESPALDO_SILABAS, min(cantidad, len(PALABRAS_RESPALDO_SILABAS)))
        return Response(palabras)


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

        prompt = f"""Genera UNA SOLA oración simple, natural y LÓGICA para un niño de 7 años que incluya la palabra: {palabra}

REGLAS IMPORTANTES:
- La oración debe tener entre 5 y 10 palabras
- Usa un lenguaje claro y sencillo apropiado para niños
- Utiliza correctamente los artículos (el/la/un/una) según el género de la palabra
- La oración debe describir características REALES y VERDADERAS de la palabra
- USA SENTIDO COMÚN: describe la palabra con atributos que realmente tenga
- NO uses signos de exclamación, comas ni puntos al final
- Asegúrate de que la gramática sea perfecta
- La oración debe sonar natural cuando un niño la lea en voz alta

IMPORTANTE - COHERENCIA LÓGICA:
- Si es un animal lento (tortuga, caracol), NO digas que es rápido
- Si es un animal rápido (conejo, león), NO digas que es lento
- Si vuela (pájaro, mariposa), menciona que vuela
- Si nada (pez, ballena), menciona que nada
- Usa las características VERDADERAS de cada cosa

Ejemplos de oraciones CORRECTAS con sentido común:
- "El gato duerme tranquilo en su cama" ✓
- "La mariposa vuela entre las flores del jardín" ✓
- "La tortuga camina despacio por el jardín" ✓ (tortugas son lentas)
- "El conejo salta muy rápido" ✓ (conejos son rápidos)
- "El sol brilla en el cielo azul" ✓

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
                "Veo un gato que camina en el jardín"
            ],
            'perro': [
                "El perro corre rápido en el parque",
                "Mi perro mueve la cola cuando me ve",
                "El perro ladra cuando alguien llega",
                "Veo un perro que juega con su pelota"
            ],
            'conejo': [
                "El conejo salta muy rápido",
                "Mi conejo come zanahorias",
                "El conejo tiene orejas largas",
                "Veo un conejo blanco en el jardín"
            ],
            'caballo': [
                "El caballo corre muy rápido",
                "Mi caballo galopa en el campo",
                "El caballo es grande y fuerte",
                "Veo un caballo café en la granja"
            ],
            # Animales lentos
            'tortuga': [
                "La tortuga camina despacio por el jardín",
                "Mi tortuga nada en el agua",
                "La tortuga tiene un caparazón duro",
                "Veo una tortuga que descansa al sol"
            ],
            # Animales que vuelan
            'pájaro': [
                "El pájaro vuela alto en el cielo",
                "Mi pájaro canta en su jaula",
                "El pájaro tiene plumas de colores",
                "Veo un pájaro en el árbol"
            ],
            'pajaro': [
                "El pájaro vuela alto en el cielo",
                "Mi pájaro canta en su jaula",
                "El pájaro tiene plumas de colores",
                "Veo un pájaro en el árbol"
            ],
            'mariposa': [
                "La mariposa vuela entre las flores",
                "Mi mariposa tiene alas de colores",
                "La mariposa se posa en una flor",
                "Veo una mariposa bonita en el jardín"
            ],
            # Animales que nadan
            'pez': [
                "El pez nada en el agua",
                "Mi pez vive en la pecera",
                "El pez tiene escamas brillantes",
                "Veo un pez de colores nadando"
            ],
            # Otros animales
            'pato': [
                "El pato nada en el lago",
                "Mi pato hace cuac cuac",
                "El pato tiene plumas amarillas",
                "Veo un pato nadando en el agua"
            ],
            'elefante': [
                "El elefante es grande y fuerte",
                "Mi elefante tiene trompa larga",
                "El elefante vive en la selva",
                "Veo un elefante en el zoológico"
            ],
            'león': [
                "El león es el rey de la selva",
                "Mi león ruge muy fuerte",
                "El león corre rápido cuando caza",
                "Veo un león descansando"
            ],
            'leon': [
                "El león es el rey de la selva",
                "Mi león ruge muy fuerte",
                "El león corre rápido cuando caza",
                "Veo un león descansando"
            ],
            'vaca': [
                "La vaca nos da leche",
                "Mi vaca come pasto en el campo",
                "La vaca hace muuu",
                "Veo una vaca en la granja"
            ],
            'gallina': [
                "La gallina pone huevos",
                "Mi gallina cacarea en el corral",
                "La gallina tiene plumas suaves",
                "Veo una gallina con sus pollitos"
            ],
            # Naturaleza
            'sol': [
                "El sol brilla en el cielo",
                "El sol nos da luz y calor",
                "El sol sale todas las mañanas",
                "Veo el sol muy brillante hoy"
            ],
            'luna': [
                "La luna brilla en la noche",
                "La luna sale cuando oscurece",
                "La luna es redonda y blanca",
                "Veo la luna en el cielo nocturno"
            ],
            'flor': [
                "La flor huele muy rico",
                "Mi flor tiene pétalos de colores",
                "La flor crece en el jardín",
                "Veo una flor roja muy bonita"
            ],
            'estrella': [
                "La estrella brilla en la noche",
                "Mi estrella favorita está en el cielo",
                "La estrella titila muy bonito",
                "Veo muchas estrellas en la noche"
            ],
            # Alimentos
            'manzana': [
                "La manzana es roja y dulce",
                "Mi manzana está muy rica",
                "La manzana es mi fruta favorita",
                "Como una manzana en el recreo"
            ],
            'pan': [
                "El pan está caliente y suave",
                "Mi pan huele muy rico",
                "El pan es mi alimento favorito",
                "Como pan con mantequilla"
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
            f"{articulo_def.capitalize()} {palabra} es muy {adjetivo_bonito}"
        ]

        oraciones_objetos = [
            f"Tengo {articulo_indef} {palabra} {adjetivo_bonito} en mi cuarto",
            f"Mi mamá me compró {articulo_indef} {palabra} {adjetivo_nuevo}",
            f"{articulo_def.capitalize()} {palabra} está sobre la mesa",
            f"Me gusta jugar con mi {palabra}",
            f"Veo {articulo_indef} {palabra} de color azul"
        ]

        oraciones_naturaleza = [
            f"{articulo_def.capitalize()} {palabra} brilla en el cielo",
            f"Miro {articulo_def} {palabra} desde mi ventana",
            f"Me encanta {articulo_def} {palabra} de la mañana",
            f"{articulo_def.capitalize()} {palabra} es {adjetivo_hermoso} hoy",
            f"Dibujé {articulo_indef} {palabra} en mi cuaderno"
        ]

        oraciones_alimentos = [
            f"Me gusta comer {palabra} en el desayuno",
            f"{articulo_def.capitalize()} {palabra} está muy {adjetivo_rico}",
            f"Mi mamá prepara {palabra} {adjetivo_delicioso}",
            f"Compré {articulo_indef} {palabra} en el mercado",
            f"{articulo_def.capitalize()} {palabra} es mi {adjetivo_favorito}"
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
