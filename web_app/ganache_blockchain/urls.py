from django.urls import path
from . import views

urlpatterns = [
    path('contract/', views.my_contract_view, name='my_contract_view'),
]