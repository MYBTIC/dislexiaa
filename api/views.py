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

# Configuramos el cliente de Gemini con la API key
client = genai.Client(api_key=settings.GEMINI_API_KEY)

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


@api_view(['GET'])
def juego_anagrama(request):
    """Genera palabras aleatorias para el juego de anagramas usando Gemini"""
    try:
        categoria = random.choice(CATEGORIAS_PALABRAS)

        prompt = f"""Genera exactamente 5 palabras en español para un juego educativo de niños de 7 años.
        Categoría: {categoria}

        REGLAS IMPORTANTES:
        - Palabras de 3 a 6 letras solamente
        - Sin tildes ni caracteres especiales
        - Palabras comunes que un niño conoce
        - Todas las letras en minúscula

        Responde SOLO con un JSON válido con este formato exacto, sin texto adicional:
        [
            {{"nombre": "gato", "imagen_busqueda": "cute cat cartoon"}},
            {{"nombre": "perro", "imagen_busqueda": "cute dog cartoon"}}
        ]
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

        # Procesar palabras y agregar URLs de imágenes
        palabras_procesadas = []
        for p in palabras_raw[:5]:
            nombre = p['nombre'].lower().strip()
            # Usar Unsplash para imágenes
            imagen_url = f"https://source.unsplash.com/400x400/?{p.get('imagen_busqueda', nombre)}"

            palabras_procesadas.append({
                "nombre": nombre,
                "imagen": imagen_url,
                "palabra_dividida_letras": "-".join(list(nombre))
            })

        return Response(palabras_procesadas)

    except Exception as e:
        print(f"Error en juego_anagrama: {e}")
        # Usar palabras de respaldo
        palabras = random.sample(PALABRAS_RESPALDO_ANAGRAMA, min(5, len(PALABRAS_RESPALDO_ANAGRAMA)))
        return Response(palabras)


@api_view(['GET'])
def juego_silabas(request):
    """Genera palabras aleatorias para el juego de sílabas usando Gemini"""
    try:
        categoria = random.choice(CATEGORIAS_PALABRAS)

        prompt = f"""Genera exactamente 5 palabras en español para un juego educativo de sílabas para niños de 7 años.
        Categoría: {categoria}

        REGLAS IMPORTANTES:
        - Palabras de 2 a 4 sílabas
        - Sin tildes ni caracteres especiales
        - Palabras comunes que un niño conoce
        - Todas las letras en minúscula

        Para cada palabra incluye:
        - Las sílabas separadas
        - El índice de una sílaba para ocultar (0, 1, 2...)
        - 4 opciones de sílabas (la correcta + 3 incorrectas similares)

        Responde SOLO con un JSON válido con este formato exacto, sin texto adicional:
        [
            {{
                "nombre": "mariposa",
                "imagen_busqueda": "butterfly cartoon cute",
                "silabas": ["ma", "ri", "po", "sa"],
                "silaba_oculta": 2,
                "opciones": ["po", "pe", "pa", "pi"]
            }}
        ]
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

        # Procesar palabras
        palabras_procesadas = []
        for p in palabras_raw[:5]:
            nombre = p['nombre'].lower().strip()
            imagen_url = f"https://source.unsplash.com/400x400/?{p.get('imagen_busqueda', nombre)}"

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
        palabras = random.sample(PALABRAS_RESPALDO_SILABAS, min(5, len(PALABRAS_RESPALDO_SILABAS)))
        return Response(palabras)


@api_view(['POST'])
def generar_oracion(request):
    """Genera una oración usando la palabra proporcionada"""
    palabra = request.data.get('palabra')

    if not palabra:
        return Response({'error': 'No se proporcionó una palabra'}, status=400)

    try:
        prompt = (f"Genera una oración con máximo de 10 palabras para un niño de 7 años, "
                  f"evita poner signos de exclamación, comas y puntos. "
                  f"Dentro de la oración pon esta palabra: {palabra}")

        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt
        )

        return Response({'oracion': response.text.strip()})
    except Exception as e:
        # Si superas las peticiones diarias, este bloque evitará que el juego se rompa
        oraciones_respaldo = [
            f"El {palabra} juega en el parque",
            f"Mira el {palabra} que está allí",
            f"Me gusta mucho el {palabra}",
            f"El {palabra} es muy bonito",
            f"Veo un {palabra} grande"
        ]
        return Response({
            'oracion': random.choice(oraciones_respaldo),
            'error': 'Usando oración de respaldo'
        })
