from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Order
from django.contrib.auth.decorators import login_required
from .forms import ProductForm

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
    items = Product.objects.all() #usando ORM 
    #items = Product.objects.raw('SELECT * FROM api_product')

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("api-productos") 
                         
    else:
        form = ProductForm()

    context = {
        'items': items,
        'form': form,
    }
    return render(request, "dashboard/productos.html", context)

def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect("api-productos")
    return render(request, "dashboard/productos_delete.html")

def product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('api-productos')

    else:
        form = ProductForm(instance=item)

    context={
        'form':form,
    }
    return render(request, "dashboard/productos_update.html", context)

@login_required(login_url='user-login')
def ordenes(request):
    # crear un "web" de entrada para ordenes
    return render(request, "dashboard/ordenes.html")