from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import hashlib
from api.models import Product
from .models import Block, Cadena
from .forms import OrderForm, OrderForm2
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import HttpResponse

class Bloque:
    def __init__(self, order_id, nombre, cantidad, stock, fecha, cliente, hash , prev_hash='', cadena=None):
        self.orden_id = order_id
        self.nombre = nombre
        self.cantidad = cantidad
        self.stock = stock
        self.fecha = fecha
        self.cliente = cliente
        self.hash = hash
        self.prev_hash = prev_hash
        self.cadena = cadena 

class MiBlock:
    def __init__(self):
        hashLast = self.hashGenerator("las_gen")
        hashFirst = self.hashGenerator("first_gen")

        genesis = Bloque("0", "genesis", 0, 0, 0, 0, hashFirst, hashLast)
        self.chain = [genesis]
    
    def hashGenerator(self, data):
        resultado = hashlib.sha256(data.encode())
        return resultado.hexdigest()

    def add_block(self, orden_id, nombre, cantidad, stock, fecha, cliente, cadena):
        prev_hash = self.chain[-1].hash
        data = f"{orden_id}{nombre}{cantidad}{stock}{fecha},{cliente}"
        hash = self.hashGenerator(data + prev_hash)
        block = Bloque(orden_id, nombre, cantidad, stock, fecha, cliente, hash, prev_hash, cadena)
        self.chain.append(block)
        
        # Guardar en la base de datos
        Block.objects.create(
            orden_id=orden_id,
            nombre=nombre,
            cantidad=cantidad,
            stock=stock,
            fecha = fecha,
            cliente = cliente,
            hash=hash,
            prev_hash=prev_hash,
            cadena=cadena
        )

blch = MiBlock()

@csrf_exempt
def get_chain(request):
    chain_data = [block.__dict__ for block in blch.chain[1:]]
    return JsonResponse(chain_data, safe=False, status=200)

def consulta(request):
    #Contador de objetos (bloques y cadenas)
    block_count = Block.objects.all().count()
    cadena_count = Cadena.objects.all().count()

    # Obtener solo los IDs únicos de los bloques
    all_ids = Block.objects.values_list('orden_id', flat=True).distinct()
    print(f"Todos los IDs: {all_ids}")  # Agrega esta línea para depurar

    # Filtrar los bloques por ID si se ha seleccionado uno
    orden_id = request.GET.get('orden_id')
    if orden_id:
        blocks = Block.objects.filter(orden_id=orden_id)
    else:
        blocks = Block.objects.all()

    print(f"Blocks: {blocks}")  # Agrega esta línea para depurar

    context = {
        'all_ids': all_ids,
        'blocks': blocks,
        'block_count':block_count,
        'cadena_count':cadena_count,
    }

    return render(request, 'blockchain/consulta.html', context)

def orden(request):
    # Contador de objetos (bloques y cadenas)
    block_count = Block.objects.all().count()
    cadena_count = Cadena.objects.all().count()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Obtén los datos del formulario
            orden_id = form.cleaned_data['orden_id']
            nombre = form.cleaned_data['nombre']
            cantidad = form.cleaned_data['cantidad']
            stock = form.cleaned_data['stock']
            fecha = form.cleaned_data.get('fecha', timezone.now())
            cliente = form.cleaned_data['cliente']
            
            # Aquí decides cómo seleccionar o crear una cadena
            cadena_nombre = f"Cadena de {nombre}"  # Usa el nombre del producto o cualquier lógica que prefieras
            cadena, created = Cadena.objects.get_or_create(
                nombre=cadena_nombre,
                defaults={'descripcion': 'Descripción por defecto'}
            )
            
            # Crea un nuevo bloque en la blockchain
            mi_block = MiBlock()
            mi_block.add_block(orden_id, nombre, cantidad, stock, fecha, cliente, cadena)
            
            messages.success(request, f'Orden Blockchain {orden_id} ha sido añadida con éxito a la cadena {cadena.nombre}')
            return redirect('blockchain-orden')
    else:
        form = OrderForm()

    context = {
        'form': form,
        'cadenas': Cadena.objects.all(),
        'block_count':block_count,
        'cadena_count':cadena_count,
    }
    return render(request, "blockchain/orden.html", context)


# blockchain/views.py
def blockchain_dashboard(request):
    block = Block.objects.all()
    cadena = Cadena.objects.all()

    #Contador de objetos (bloques y cadenas)
    block_count = Block.objects.all().count()
    cadena_count = Cadena.objects.all().count()

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
            return redirect("Blockchain-dashboard")
    else:
        form = OrderForm()

    context = {
        'form':form,
        'blocks':block,
        'cadenas':cadena,
        'block_count':block_count,
        'cadena_count':cadena_count,

    }
    return render(request, 'blockchain/dashboard.html', context)

def lista_bloques(request):
    #Contador de objetos (bloques y cadenas)
    block_count = Block.objects.all().count()
    cadena_count = Cadena.objects.all().count()

    blocks = Block.objects.filter(completado=False) #muestra bloques que no están completados

    cadenas = Cadena.objects.all()  # Obtén todas las cadenas

    if request.method == 'POST':
        cadena_nombre = request.POST.get('nombre')
        cadena_descripcion = request.POST.get('descripcion')

        # Crea una nueva cadena si el nombre y descripción son proporcionados
        if cadena_nombre:
            nueva_cadena = Cadena.objects.create(nombre=cadena_nombre, descripcion=cadena_descripcion)
            # Lógica adicional si deseas asociar bloques existentes a esta nueva cadena
            # Ejemplo: asociar todos los bloques actuales a la nueva cadena
            for block in blocks:
                block.cadena = nueva_cadena
                block.save()

        return redirect('blockchain-bloques')  # Redirigir a la misma vista después de crear la cadena

    context = {
        'blocks': blocks,
        'cadenas': cadenas,
        'block_count':block_count,
        'cadena_count':cadena_count,
    }

    return render(request, 'blockchain/bloques.html', context)

def crear_cadena(request, nombre):
    print(f"Recibiendo ID de bloque: {nombre}")
    block = get_object_or_404(Block, nombre=nombre)

    if request.method == "POST":
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']

        # Crear la nueva cadena
        nueva_cadena = Cadena.objects.create(
            nombre=nombre,
            descripcion=descripcion
        )

        # Aquí podrías asociar el block a la cadena si es necesario
        # Por ejemplo:
        block.cadena = nueva_cadena
        block.save()

        return redirect('blockchain-bloques')  # Redirige a la lista de bloques después de crear la cadena

    return render(request, 'blockchain/bloques_crear.html', {'block': block})

def segundo_bloque(request, pk):
    # Contador de objetos (bloques y cadenas)
    block_count = Block.objects.all().count()
    cadena_count = Cadena.objects.all().count()

    # Recuperar los bloques relacionados con esta orden_id
    bloques_relacionados = Block.objects.filter(orden_id=pk).order_by('fecha')
    
    # Si no hay bloques, no deberíamos estar en esta vista
    if not bloques_relacionados.exists():
        return HttpResponse("No se encontró ningún bloque relacionado con esta orden_id", status=404)

    # Identificar el último bloque (el más reciente en la cadena)
    ultimo_bloque = bloques_relacionados.last()
    
    # Filtrar bloques incompletos (opcional, según lo que necesites mostrar)
    bloques_incompletos = Block.objects.filter(cadena=ultimo_bloque.cadena, completado=False)

    if request.method == 'POST':
        form = OrderForm2(request.POST)

        if form.is_valid():
            # Mantén el nombre de la orden del bloque anterior
            nombre = ultimo_bloque.nombre

            # Obtén los datos adicionales del formulario
            cantidad = form.cleaned_data['cantidad']
            stock = form.cleaned_data['stock']
            cliente = form.cleaned_data['cliente']
            cadena = ultimo_bloque.cadena

            # Crear el nuevo bloque
            mi_block = MiBlock()
            
            # Usar el hash del último bloque como prev_hash para el nuevo bloque
            prev_hash = ultimo_bloque.hash
            data = f"{pk}{nombre}{cantidad}{stock}{timezone.now()},{cliente}"
            new_hash = mi_block.hashGenerator(data + prev_hash)
            
            # Guardar el nuevo bloque en la cadena
            Block.objects.create(
                cadena=cadena,
                orden_id=pk,
                nombre=nombre,
                cantidad=cantidad,
                stock=stock,
                fecha=timezone.now(),
                cliente=cliente,
                hash=new_hash,
                prev_hash=prev_hash
            )

            # Marcar el bloque anterior como completado
            ultimo_bloque.completado = True
            ultimo_bloque.save()
            
            return redirect('blockchain-bloques')
    else:
        # Prellenar manualmente los campos en el formulario
        form = OrderForm2(initial={
            'orden_id': ultimo_bloque.orden_id,
            'nombre': ultimo_bloque.nombre,
            'cantidad': ultimo_bloque.cantidad,  # Si deseas prellenar la cantidad del primer bloque
            'stock': ultimo_bloque.stock,        # Si deseas prellenar el stock del primer bloque
            'cliente': ultimo_bloque.cliente
        })
        # Bloquear los campos para que no se puedan editar
        form.fields['orden_id'].widget.attrs['readonly'] = True
        form.fields['nombre'].widget.attrs['readonly'] = True

    return render(request, 'blockchain/segundo_bloque.html', {'form': form, 'bloques_incompletos': bloques_incompletos, 'block_count':block_count, 'cadena_count':cadena_count,})


def ver_cadena(request, cadena_id):
    #Contador de objetos (bloques y cadenas)
    block_count = Block.objects.all().count()
    cadena_count = Cadena.objects.all().count()
    cadena = get_object_or_404(Cadena, id=cadena_id)
    bloques = cadena.bloques.all()  # Obtén todos los bloques de la cadena
    return render(request, 'blockchain/bloques.html', {'cadena': cadena, 'bloques': bloques, 'block_count':block_count, 'cadena_count':cadena_count,})

def get_product_quantity(request, product_name):
    try:
        product = Product.objects.get(name=product_name)
        return JsonResponse({'quantity': product.quantity})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)