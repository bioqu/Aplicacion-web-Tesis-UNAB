from django.contrib import admin
from .models import Block

class BloqueAdmin(admin.ModelAdmin):
    list_display = ('producto_id', 'nombre', 'cantidad', 'stock', 'hash', 'prev_hash')
    search_fields = ('producto_id', 'nombre', 'hash')

admin.site.register(Block, BloqueAdmin)


