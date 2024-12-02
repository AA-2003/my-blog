from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')  # Replace 'home' with your app's home URL name
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})
