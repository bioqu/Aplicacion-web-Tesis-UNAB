from django import forms
from .models import Product, Order, PDF

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
    
    quantity_available = forms.IntegerField(
        label='Cantidad Disponible',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    class Meta:
        model = Order
        fields = ['product', 'order_quantity', 'quantity_available']
        labels = {
            'product': 'Nombre del Producto',
            'order_quantity': 'Cantidad',
            'quantity_available': 'Cantidad Disponible'
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        if 'product' in self.data:
            try:
                product_id = int(self.data.get('product'))
                product = Product.objects.get(id=product_id)
                self.fields['quantity_available'].initial = product.quantity  # Aquí se asigna quantity a quantity_available
            except (ValueError, TypeError, Product.DoesNotExist):
                pass  # Si no existe el producto, dejar el campo vacío
        elif self.instance.pk:
            self.fields['quantity_available'].initial = self.instance.product.quantity  # Aquí también se asigna quantity a quantity_available

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'staff', 'order_quantity', 'completado']  # Incluye 'completado' para la edición

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ['file']  # Suponiendo que el modelo PDF tiene un campo 'file' para almacenar el PDF