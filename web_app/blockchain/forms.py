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

class OrderForm2(forms.ModelForm):
    class Meta:
        model = Block
        fields = ['orden_id', 'nombre', 'cantidad', 'stock', 'cliente']

    def __init__(self, *args, **kwargs):
        super(OrderForm2, self).__init__(*args, **kwargs)
        # Hacer que los campos 'orden_id' y 'nombre' sean de solo lectura
        self.fields['orden_id'].widget.attrs['readonly'] = True
        self.fields['nombre'].widget.attrs['readonly'] = True