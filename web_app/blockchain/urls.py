from django.urls import path
from . import views

urlpatterns = [
    path('add_block/', views.add_block, name='add_block'),
    path('get_chain/', views.get_chain, name='get_chain'),
    path('dashboard/', views.blockchain_dashboard, name='blockchain-dashboard'),  # Ruta para el dashboard
    path('consulta/', views.consulta, name='blockchain-consulta'),
    path("ordenes", views.orden, name="blockchain-orden"), 
]


