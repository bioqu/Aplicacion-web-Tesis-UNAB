from django.db import models
from django.utils import timezone
from api.models import Product

class Cadena(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Block(models.Model):
    cadena = models.ForeignKey(Cadena, on_delete=models.CASCADE, related_name='bloques', null=True, blank=True)
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
