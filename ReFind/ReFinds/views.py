
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login,authenticate
from django.contrib import messages
from .forms import LoginForm

def index_view(request):
    return render(request,'index.html')


def home_view(request):
    return render(request, 'home.html')




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


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') 
            else:
                messages.error(request, 'Невалидно потребителско име или парола.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
