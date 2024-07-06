from django.contrib.auth.models import User
from .models import Perfil
from django.db.models.signals import post_save
from django.dispatch import receiver 


@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(Staff=instance)


@receiver(post_save, sender=User)
def save_perfil(sender, instance, **kwargs):
    instance.perfil.save()