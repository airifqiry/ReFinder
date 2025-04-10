
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрацията беше успешна! Моля, влез в профила си.')
            return redirect('login')  
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

