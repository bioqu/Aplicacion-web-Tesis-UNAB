from django import forms
from .models import Product, Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity']
        labels = {
            'name': 'Nombre del Producto',     # Cambia "name" a "Nombre del Producto"
            'category': 'Categoría',           # Cambia "category" a "Categoría"
            'quantity': 'Cantidad Disponible', # Cambia "quantity" a "Cantidad Disponible"
        }

class OrderForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label='Nombre del Producto',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Order
        fields = ['product', 'order_quantity']
        labels = {
            'product': 'Nombre del Producto',     
            'order_quantity': 'Cantidad',           
        }