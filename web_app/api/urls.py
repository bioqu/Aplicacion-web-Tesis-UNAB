from django.urls import path # type: ignore
from . import views

urlpatterns = [
    #cada vez que llegue un request para una pagina vacia ("") va a redirigir a pagina main
    path("dashboard", views.index, name = "api-index"),
    path("staff/", views.staff, name = "api-staff"),
    path("productos/", views.productos, name = "api-productos"),
    path("ordenes/", views.ordenes, name = "api-ordenes"),
    path("productos/delete/<int:pk>/", views.product_delete, name = "api-productos-delete"),
    
]
 