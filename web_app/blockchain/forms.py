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

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        if 'nombre' in self.data:
            try:
                product_id = int(self.data.get('nombre'))
                product = Product.objects.get(id=product_id)
                self.fields['stock'].initial = product.quantity  # Muestra el stock actual
            except (ValueError, TypeError, Product.DoesNotExist):
                pass  # Si no existe el producto, dejar el campo vacío
        elif self.instance.pk:
            self.fields['stock'].initial = self.instance.nombre.quantity  # Prellenado en caso de edición

class OrderForm2(forms.ModelForm):
    class Meta:
        model = Block
        fields = ['orden_id', 'nombre', 'cantidad', 'stock', 'cliente']

    def __init__(self, *args, **kwargs):
        super(OrderForm2, self).__init__(*args, **kwargs)
        # Hacer que los campos 'orden_id' y 'nombre' sean de solo lectura
        self.fields['orden_id'].widget.attrs['readonly'] = True
        self.fields['nombre'].widget.attrs['readonly'] = True, 