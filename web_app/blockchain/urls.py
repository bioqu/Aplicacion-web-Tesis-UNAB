from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='block-index'),
    path('add_block/', views.add_block, name='add_block'),
    path('get_chain/', views.get_chain, name='get_chain'),
    path('dashboard/', views.blockchain_dashboard, name='blockchain_dashboard'),  # Ruta para el dashboard
]
