from django.urls import path
from . import views

urlpatterns = [
    #cada vez que llegue un request para una pagina vacia ("") va a redirigir a pagina main
    path("", views.index, name = "index"),
    path("staff/", views.staff, name = "staff")
    
]
