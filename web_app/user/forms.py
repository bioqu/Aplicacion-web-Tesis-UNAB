from django import forms
from .models import Perfil
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class PerfilUpdateForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['Direccion', 'Telefono', 'Imagen']