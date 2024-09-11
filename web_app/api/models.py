from django.db import models
from django.contrib.auth.models import User # type: ignore

# Create your models here.
class Product(models.Model):
    CATEGORY = (
    ('Stationary', 'Papelería'),
    ('Electronics', 'Electrónica'),
    ('Food', 'Alimentos'),
)
    name = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField(null=True)
    category = models.CharField(max_length=50, choices=CATEGORY, null=True)
    
    @property
    def category_display(self):
        return dict(self.CATEGORY).get(self.category, self.category)
    
    def __str__(self):
        return f'{self.name}-{self.quantity}'

#crear queryset para filtraar ordenes completadas
class OrderQuerySet(models.QuerySet):
    def completadas(self):
        return self.filter(completado=True)

    def no_completadas(self):
        return self.filter(completado=False)

#manager para sobreescribir queryset
class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

    def completadas(self):
        return self.get_queryset().completadas()

    def no_completadas(self):
        return self.get_queryset().no_completadas()

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add= True)
    completado = models.BooleanField(default=False)

    objects = OrderManager()  #se asigna el manager personalizado

    def __str__(self):
        return f'{self.product}-{self.order_quantity} ordered by {self.staff}'
    
class PDF(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='pdfs')
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)