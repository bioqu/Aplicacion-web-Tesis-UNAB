from django.db import models
from django.utils import timezone
from api.models import Product

class Block(models.Model):
    orden_id  = models.CharField(max_length=100)
    nombre = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    stock = models.IntegerField()
    fecha = models.DateTimeField(default=timezone.now)  # Se añade automáticamente la fecha y hora actuales
    cliente = models.CharField(max_length=255) #se añade cliente que pide orden
    hash = models.CharField(max_length=64)
    prev_hash = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f'Bloque {self.id} - {self.nombre}'
