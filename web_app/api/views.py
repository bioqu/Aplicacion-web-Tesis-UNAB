from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Order
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='user-login')
def index(request):
    # funcion para crear un "web" de entrada index
    return render(request, "dashboard/index.html")

@login_required(login_url='user-login')
def staff(request):
    # crear un "web" de entrada para staff
    return render(request, "dashboard/staff.html")

@login_required(login_url='user-login')
def productos(request):
    # crear un "web" de entrada para productos
    return render(request, "dashboard/productos.html")

@login_required(login_url='user-login')
def ordenes(request):
    # crear un "web" de entrada para ordenes
    return render(request, "dashboard/ordenes.html")