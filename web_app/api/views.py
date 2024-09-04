from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Product, Order
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, OrderForm, OrderUpdateForm, PDFUploadForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse



# Create your views here.
@login_required(login_url='user-login')
def index(request):
    # funcion para crear un "web" de entrada index
    orders = Order.objects.all()
    products = Product.objects.all()

    #Contador de objetos ebanda info (productos, ordenes y staff o usuario)
    workers_count = User.objects.all().count()
    orders_count = Order.objects.all().count()
    item_count = Product.objects.all().count()
    productos_con_stock_cero = Product.objects.filter(quantity=0)

    CATEGORY_TRANSLATIONS = {
    'Food': 'Alimentos',
    'Electronics': 'Electrónica',
    'Stationary': 'Papelería',
    }
    
    items = Product.objects.all()
    # Traducir las categorías
    for items in items:
        items.category = CATEGORY_TRANSLATIONS.get(items.category, items.category)


    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            product = instance.product
            order_quantity = instance.order_quantity

            if product.quantity >= order_quantity:
                # Actualizar el stock del producto
                product.quantity -= order_quantity
                product.save()

                # Guardar la orden
                instance.staff = request.user
                instance.save()

                # Mensaje de orden creada con exito
                order_name = form.cleaned_data.get('product').name
                messages.success(request, f'La orden {order_name} ha sido añadida con éxito')
                return redirect("api-index")
            else:
                # Mensaje de error si el stock es insuficiente
                messages.error(request, f'Stock insuficiente para el producto {product.name}. Quedan {product.quantity} unidades.')
    else:
        form = OrderForm()

    context={
        'orders':orders,
        'form':form,
        'products':products,
        'workers_count':workers_count,
        'orders_count':orders_count,
        'item_count':item_count,
        'productos_con_stock_cero': productos_con_stock_cero,
        'items':items,
    }
    return render(request, "dashboard/index.html", context)

@login_required(login_url='user-login')
def staff(request):
    # crear un "web" de entrada para staff   
    workers = User.objects.all()
    workers_count = workers.count()

    #Contador de objetos ebanda info (productos, ordenes y staff o usuario)
    orders_count = Order.objects.all().count()
    item_count = Product.objects.all().count()
    productos_con_stock_cero = Product.objects.filter(quantity=0)


    context={
        'workers':workers,
        'workers_count':workers_count,
        'orders_count':orders_count,
        'item_count':item_count,
        'productos_con_stock_cero': productos_con_stock_cero,
    }
    return render(request, "dashboard/staff.html", context)

@login_required(login_url='user-login')
def staff_detail(request, pk):
    workers = User.objects.get(id=pk)
    #Contador de objetos (productos, ordenes y staff o usuario) &banda info
    orders_count = Order.objects.all().count()
    item_count = Product.objects.all().count()
    workers_count = User.objects.all().count()
    productos_con_stock_cero = Product.objects.filter(quantity=0)

    context={
        'workers':workers,
        'workers_count':workers_count,
        'orders_count':orders_count,
        'item_count':item_count,
        'productos_con_stock_cero': productos_con_stock_cero,
    }
    return render(request, "dashboard/staff_detail.html", context)

@login_required(login_url='user-login')
def productos(request):
    # crear un "web" de entrada para productos
    items = Product.objects.all() #usando ORM 
    #items = Product.objects.raw('SELECT * FROM api_product')

    #Contador de objetos (productos, ordenes y staff o usuario) &banda info
    workers_count = User.objects.all().count()
    orders_count = Order.objects.all().count()
    item_count = items.count()
    productos_con_stock_cero = Product.objects.filter(quantity=0)


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
        'workers_count':workers_count,
        'orders_count':orders_count,
        'item_count':item_count,
        'productos_con_stock_cero': productos_con_stock_cero,
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
    # Inicializar el filtro de ordenes completada
    if 'filter' in request.GET:
        filter_type = request.GET['filter']
        if filter_type == 'completadas':
            orders = Order.objects.completadas()
        elif filter_type == 'no_completadas':
            orders = Order.objects.no_completadas()
        else:
            orders = Order.objects.all()
    else:
        orders = Order.objects.all()
        
    #Contador de objetos (productos, ordenes y staff o usuario) &banda info
    workers_count = User.objects.all().count()
    orders_count = orders.count()
    item_count = Product.objects.all().count()
    productos_con_stock_cero = Product.objects.filter(quantity=0)

    CATEGORY_TRANSLATIONS = {
    'Food': 'Alimentos',
    'Electronics': 'Electrónica',
    'Stationary': 'Papelería',
    }

    items = Product.objects.all()
    # Traducir las categorías
    for items in items:
        items.category = CATEGORY_TRANSLATIONS.get(items.category, items.category)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            product = instance.product
            order_quantity = instance.order_quantity

            if product.quantity >= order_quantity:
                # Actualizar el stock del producto
                product.quantity -= order_quantity
                product.save()

                # Guardar la orden
                instance.staff = request.user
                instance.save()

                # Mensaje de orden creada con exito
                order_name = form.cleaned_data.get('product').name
                messages.success(request, f'La orden {order_name} ha sido añadida con éxito')
                return redirect("api-ordenes")
            else:
                # Mensaje de error si el stock es insuficiente
                messages.error(request, f'Stock insuficiente para el producto {product.name}. Quedan {product.quantity} unidades.')

    else:
        form = OrderForm()

    context = {
        'orders': orders,
        'form': form,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'item_count': item_count,
        'productos_con_stock_cero': productos_con_stock_cero,
        'items':items,
    }
    return render(request, "dashboard/ordenes.html", context)


@login_required(login_url='user-login')
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    #Contador de objetos (productos, ordenes y staff o usuario) & banda inof
    workers_count = User.objects.all().count()
    orders_count = Order.objects.all().count()
    item_count = Product.objects.all().count()
    productos_con_stock_cero = Product.objects.filter(quantity=0)


    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.order = order
            pdf.save()
            return redirect('api-ordenes-detail', pk=order.pk)
    else:
        form = PDFUploadForm()

    context = {
        'order': order,
        'form': form,
        'workers_count':workers_count,
        'orders_count': orders_count,
        'item_count':item_count,
        'productos_con_stock_cero': productos_con_stock_cero,
        
    }
    return render(request, "dashboard/ordenes_detail.html", context)


@login_required(login_url='user-login')
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)

    # Obtener todas las órdenes completadas
    ordenes_completadas = Order.objects.completadas()

    # Obtener todas las órdenes no completadas
    ordenes_no_completadas = Order.objects.no_completadas()

    #Contador de objetos (productos, ordenes y staff o usuario) & banda info
    workers_count = User.objects.all().count()
    orders_count = Order.objects.all().count()
    item_count = Product.objects.all().count()
    productos_con_stock_cero = Product.objects.filter(quantity=0)

    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('api-ordenes')
    else:
        form = OrderUpdateForm(instance=order)

    context = {
        'form': form,
        'order': order,
        'workers_count':workers_count,
        'orders_count': orders_count,
        'item_count':item_count,
        'ordenes_completadas':ordenes_completadas,
        'ordenes_no_completadas':ordenes_no_completadas,
        'productos_con_stock_cero': productos_con_stock_cero,
        
    }
    return render(request, "dashboard/ordenes_edit.html", context)

@login_required(login_url='user-login')
def staff_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.order = order
            pdf.save()
            return redirect('api-index', pk=order.pk)
    else:
        form = PDFUploadForm()

    context = {
        'order': order,
        'form': form,
        'product': order.product, 
        
    }
    return render(request, "dashboard/staff_ordenes_detail.html", context)


@login_required(login_url='user-login')
def staff_order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)


    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('api-index')
    else:
        form = OrderForm(instance=order)

    context = {
        'form': form,
        'order': order,        
    }
    return render(request, "dashboard/staff_ordenes_edit.html", context)

def get_product_quantity(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        return JsonResponse({'quantity': product.quantity})
    except Product.DoesNotExist:
        return JsonResponse({'quantity': 0})