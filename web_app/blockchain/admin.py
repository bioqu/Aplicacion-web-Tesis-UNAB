from django.contrib import admin
from .models import Block

class BloqueAdmin(admin.ModelAdmin):
    list_display = ('orden_id', 'nombre', 'cantidad', 'stock', 'hash', 'prev_hash')
    search_fields = ('orden_id', 'nombre__name', 'hash')

admin.site.register(Block, BloqueAdmin)


