from django.shortcuts import render, redirect
from django.http import JsonResponse
import hashlib
from api.models import Product
from .models import Block
from .forms import OrderForm
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import get_object_or_404

class Bloque:
    def __init__(self, order_id, nombre, cantidad, stock, fecha, cliente, hash , prev_hash=''):
        self.order_id = order_id
        self.nombre = nombre
        self.cantidad = cantidad
        self.stock = stock
        self.fecha = fecha
        self.cliente = cliente
        self.hash = hash
        self.prev_hash = prev_hash

class MiBlock:
    def __init__(self):
        hashLast = self.hashGenerator("las_gen")
        hashFirst = self.hashGenerator("first_gen")

        genesis = Bloque("0", "genesis", 0, 0, 0, 0, hashFirst, hashLast)
        self.chain = [genesis]
    
    def hashGenerator(self, data):
        resultado = hashlib.sha256(data.encode())
        return resultado.hexdigest()

    def add_block(self, order_id, nombre, cantidad, stock, fecha, cliente):
        prev_hash = self.chain[-1].hash
        data = f"{order_id}{nombre}{cantidad}{stock}{fecha},{cliente}"
        hash = self.hashGenerator(data + prev_hash)
        block = Bloque(order_id, nombre, cantidad, stock, fecha, cliente, hash, prev_hash)
        self.chain.append(block)
        
        # Guardar en la base de datos
        Block.objects.create(
            order_id=order_id,
            nombre=nombre,
            cantidad=cantidad,
            stock=stock,
            fecha = fecha,
            cliente = cliente,
            hash=hash,
            prev_hash=prev_hash
        )

blch = MiBlock()

@csrf_exempt
def add_block(request):
    if request.method == 'POST':
        data = request.POST
        order_id = data['ordenes_id']
        nombre = data['nombre']
        cantidad = data['cantidad']
        stock = data['stock']
        fecha = data['fecha']  # Usa la fecha proporcionada o la fecha actual
        cliente = data['cliente']
        blch.add_block(order_id, nombre, cantidad, stock, fecha, cliente)
        return JsonResponse({'message': 'Block added successfully', 'block': blch.chain[-1].__dict__}, status=200)


@csrf_exempt
def get_chain(request):
    chain_data = [block.__dict__ for block in blch.chain[1:]]
    return JsonResponse(chain_data, safe=False, status=200)

def consulta(request):
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
    }

    return render(request, 'blockchain/consulta.html', context)

""" def index(request):
    items = Product.objects.all() #usando ORM 

    context = {
        'items': items,
    }
    return render(request, 'blockchain/index.html', context) """


def orden(request):
    block_order = Block.objects.all()

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("blockchain-orden")
    else:
        form = OrderForm()

    context = {
        'bloc_order': block_order,
        'form': form,
    }
    return render(request, "blockchain/orden.html", context)

# blockchain/views.py
def blockchain_dashboard(request):
    return render(request, 'blockchain/dashboard.html')


