from django.urls import path
from . import views

urlpatterns = [
    path('get_chain/', views.get_chain, name='get_chain'),
    path('dashboard/', views.blockchain_dashboard, name='blockchain-dashboard'),  # Ruta para el dashboard
    path('consulta/', views.consulta, name='blockchain-consulta'),
    path("ordenes/", views.orden, name="blockchain-orden"),
    path('bloques/', views.lista_bloques, name='blockchain-bloques'),
    path("crear_cadena/<str:nombre>/", views.crear_cadena, name='crear-cadena'), 
]