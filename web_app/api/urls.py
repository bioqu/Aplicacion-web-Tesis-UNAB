from django.urls import path
from . import views

urlpatterns = [
    #cada vez que llegue un request para una pagina vacia ("") va a redirigir a pagina main
    path("", views.index, name = "api-index"),
    path("staff/", views.staff, name = "api-staff"),
    path("productos/", views.productos, name = "api-productos"),
    path("ordenes/", views.ordenes, name = "api-ordenes"),
    
]
 