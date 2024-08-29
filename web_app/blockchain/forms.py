from django import forms
from api.models import Product
from .models import Block

class OrderForm(forms.ModelForm):
    nombre = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        to_field_name="name",
        empty_label="Selecciona un producto",
        label="Nombre del Producto"
    )

    class Meta:
        model = Block
        fields = ['orden_id', 'nombre', 'cantidad', 'cliente', 'stock']
        labels = {
            'orden_id': 'ID de la Orden',
            'nombre': 'Nombre del Producto',
            'cantidad': 'Cantidad',
            'cliente': 'Cliente',
            'stock': 'Stock',
        }
