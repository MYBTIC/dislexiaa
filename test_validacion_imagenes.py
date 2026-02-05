"""
Script de prueba para el sistema de validación ultra rigurosa de imágenes.

Este script demuestra cómo el sistema valida cada imagen antes de aceptarla.
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dislexia.settings')
django.setup()

from api.views import get_gemini_client, obtener_imagen_validada_del_diccionario, IMAGENES_UNSPLASH

def probar_validacion():
    """Prueba el sistema de validación con algunas palabras."""

    print("=" * 70)
    print("🔒 SISTEMA DE VALIDACIÓN ULTRA RIGUROSA DE IMÁGENES")
    print("=" * 70)
    print()

    # Obtener cliente de Gemini
    client = get_gemini_client()
    if not client:
        print("❌ Error: No se pudo obtener el cliente de Gemini")
        print("💡 Asegúrate de tener configurada la API key en settings.py")
        return

    print("✅ Cliente de Gemini inicializado correctamente")
    print()

    # Palabras de prueba
    palabras_prueba = ["zorro", "pelota", "gato", "caballo", "elefante"]

    print(f"🧪 Probando validación para {len(palabras_prueba)} palabras...")
    print()

    resultados = []

    for palabra in palabras_prueba:
        print("-" * 70)
        print(f"📝 Palabra: '{palabra}'")

        # Verificar si está en el diccionario
        if palabra not in IMAGENES_UNSPLASH:
            print(f"   ⚠️ '{palabra}' no está en el diccionario de imágenes")
            resultados.append((palabra, None, "No en diccionario"))
            continue

        # Contar imágenes disponibles
        urls = IMAGENES_UNSPLASH[palabra]
        if isinstance(urls, str):
            urls = [urls]
        num_imagenes = len(urls)

        print(f"   📊 {num_imagenes} imagen(es) disponible(s) en el diccionario")
        print()

        # Validar imagen
        imagen_valida = obtener_imagen_validada_del_diccionario(client, palabra)

        if imagen_valida:
            print()
            print(f"   ✅ RESULTADO: Imagen VÁLIDA encontrada para '{palabra}'")
            print(f"   🔗 URL: {imagen_valida[:60]}...")
            resultados.append((palabra, imagen_valida, "Válida"))
        else:
            print()
            print(f"   ❌ RESULTADO: NO se encontró imagen válida para '{palabra}'")
            print(f"   💡 Se buscará alternativa en Unsplash")
            resultados.append((palabra, None, "Inválida"))

        print()

    # Resumen
    print("=" * 70)
    print("📊 RESUMEN DE VALIDACIÓN")
    print("=" * 70)
    print()

    validas = sum(1 for _, img, _ in resultados if img is not None)
    invalidas = len(resultados) - validas

    print(f"Total palabras probadas: {len(resultados)}")
    print(f"✅ Imágenes válidas:     {validas}")
    print(f"❌ Imágenes inválidas:   {invalidas}")
    print(f"📈 Tasa de éxito:        {(validas/len(resultados)*100):.1f}%")
    print()

    print("Detalle por palabra:")
    for palabra, imagen, estado in resultados:
        emoji = "✅" if imagen else "❌"
        print(f"  {emoji} {palabra:15} → {estado}")

    print()
    print("=" * 70)
    print("🎉 Prueba completada!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        probar_validacion()
    except KeyboardInterrupt:
        print("\n\n⚠️ Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
