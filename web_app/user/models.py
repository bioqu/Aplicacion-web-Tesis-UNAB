from distributed import _
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    Staff = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    Direccion = models.CharField(max_length=200, null=True)
    Telefono = models.CharField(max_length=20, null=True)
    Imagen = models.ImageField(default="avatar.jpg", upload_to="Profile_Images")

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return f"{self.Staff.username}-Perfil"
