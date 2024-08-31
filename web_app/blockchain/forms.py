from django import forms
from api.models import Product
from .models import Block

class OrderForm(forms.ModelForm):
    class Meta:
        model = Block
        fields = ['orden_id', 'nombre', 'cantidad', 'stock', 'cliente']
        labels = {
            'orden_id': 'ID de la Orden',
            'nombre': 'Nombre del Producto',
            'cantidad': 'Cantidad',
            'stock': 'Stock',
            'cliente': 'Cliente',
            
        }
