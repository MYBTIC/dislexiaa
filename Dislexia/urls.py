"""
URL configuration for Dislexia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_home(request):
    """Vista de bienvenida para la raíz del API"""
    return JsonResponse({
        'message': 'Bienvenido al API del Juego de Palabras',
        'version': '1.0',
        'endpoints': {
            'anagramas': '/api/juego1/',
            'silabas': '/api/juego2/',
            'generar_oracion': '/api/oracion/ (POST)',
            'admin': '/admin/'
        },
        'docs': 'Ver README.md para mas informacion'
    })

urlpatterns = [
    path('', api_home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Esto conecta las rutas de tu app api
]


