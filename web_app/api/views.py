from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Order
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, OrderForm
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
@login_required(login_url='user-login')
def index(request):
    # funcion para crear un "web" de entrada index
    orders = Order.objects.all()
    products = Product.objects.all()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
            return redirect("api-index")
    else:
        form = OrderForm()

    context={
        'orders':orders,
        'form':form,
        'products':products,
    }
    return render(request, "dashboard/index.html", context)

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

    CATEGORY_TRANSLATIONS = {
    'Food': 'Alimentos',
    'Electronics': 'Electrónica',
    'Stationary': 'Papelería',
    }

    # Traducir las categorías
    for item in items:
        item.category = CATEGORY_TRANSLATIONS.get(item.category, item.category)

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} ha sido añadido con exito')
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


    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            order_name = form.cleaned_data.get('product').name
            messages.success(request, f'La orden {order_name} ha sido añadida con éxito')
            return redirect("api-ordenes")
                         
    else:
        form = OrderForm()

    context={
        'orders':orders,
        'form':form,
    }
    return render(request, "dashboard/ordenes.html", context)