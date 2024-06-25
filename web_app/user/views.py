from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            #user = 
            #group = Group.objects.get(name='Customers')
            #user.groups.add(group)
            return redirect("api-index")
    else:
        form = CreateUserForm()
    context = {
        "form": form
    }
    return render(request, 'user/register.html', context)

