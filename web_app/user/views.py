from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, UserUpdateForm, PerfilUpdateForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            #user = 
            #group = Group.objects.get(name='Customers')
            #user.groups.add(group)
            return redirect("user-login")
    else:
        form = CreateUserForm()
    context = {
        "form": form
    }
    return render(request, 'user/login.html', context)

def perfil(request):
    return render(request, "user/perfil.html")

def perfil_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = PerfilUpdateForm(request.POST, request.FILES, instance=request.user.perfil)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('user-perfil')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = PerfilUpdateForm(instance=request.user.perfil)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'user/perfil_update.html', context)