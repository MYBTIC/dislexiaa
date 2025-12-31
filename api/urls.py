from django.urls import path
from . import views

urlpatterns = [
    path('juego1/', views.juego_anagrama),
    path('juego2/', views.juego_silabas),
    # path('oracion/<int:palabra_id>/', views.obtener_oracion),
    path('oracion/', views.generar_oracion),
]