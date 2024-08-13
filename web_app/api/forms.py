from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'quantity']
        labels = {
            'name': 'Nombre del Producto',     # Cambia "name" a "Nombre del Producto"
            'category': 'Categoría',           # Cambia "category" a "Categoría"
            'quantity': 'Cantidad Disponible', # Cambia "quantity" a "Cantidad Disponible"
        }
         