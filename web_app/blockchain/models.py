from django.db import models

class Block(models.Model):
    producto_id = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    stock = models.IntegerField()
    hash = models.CharField(max_length=64)
    prev_hash = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f'Bloque {self.id} - {self.nombre}'
