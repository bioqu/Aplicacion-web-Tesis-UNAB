from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # funcion para crear un "web" de entrada index
    return render(request, "dashboard/index.html")

def staff(request):
    # funcion para crear un "web" de entrada para staff
    return render(request, "dashboard/staff.html")
