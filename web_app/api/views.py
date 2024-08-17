from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Order
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='user-login')
def index(request):
    # funcion para crear un "web" de entrada index
    return render(request, "dashboard/index.html")

@login_required(login_url='user-login')
def staff(request):
    # crear un "web" de entrada para staff
    workers = User.objects.all()
    context={
        'workers':workers
    }
    return render(request, "dashboard/staff.html", context)

@login_required(login_url='user-login')
def staff_detail(request, pk):
    workers = User.objects.get(id=pk)
    context={
        'workers':workers,
    }
    return render(request, "dashboard/staff_detail.html", context)

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

@login_required(login_url='user-login')
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect("api-productos")
    return render(request, "dashboard/productos_delete.html")

@login_required(login_url='user-login')
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
    orders = Order.objects.all()

    context={
        'orders':orders,
    }
    return render(request, "dashboard/ordenes.html", context)