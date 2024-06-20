from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # funcion para crear un "web" de entrada index
    return render(request, "dashboard/index.html")

def staff(request):
    # crear un "web" de entrada para staff
    return render(request, "dashboard/staff.html")

def productos(request):
    # crear un "web" de entrada para productos
    return render(request, "dashboard/productos.html")

def ordenes(request):
    # crear un "web" de entrada para ordenes
    return render(request, "dashboard/ordenes.html")