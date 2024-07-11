from django.db import models

class InventoryItem(models.Model):
    item_id = models.IntegerField()
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
