from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def main(request):
    # funcion para crear un "web" de entrada main
    return HttpResponse("<h1>Hello mutherfuckers</h1>")
