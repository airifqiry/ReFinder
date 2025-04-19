from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm,RegisterForm,AdForm
from .models import Ad
from django.http import JsonResponse


def index_view(request):
    return render(request,'index.html')


def home_view(request):
    return render(request, 'home.html')
@login_required 
def user_logout(request):
    logout(request)
    return redirect('index')


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




def ad_list_view(request):
    ads = Ad.objects.all().order_by('-created_at')
    return render(request, 'ads_list.html', {'ads': ads})

def ad_detail_view(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ad_detail.html', {'ad': ad})



def add_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save()
            ad.user=request.user
            messages.success(request, "Обявата беше добавена успешно!")
            return redirect('home')
    else:
        form = AdForm()
    return render(request, 'listing.html', {'form': form})



def ad_list_json(request):
    ads = Ad.objects.all()
    data = [{
        'title': ad.title,
        'description': ad.description,
        'latitude': ad.latitude,
        'longitude': ad.longitude,
        'image': ad.image.url if ad.image else '',
    } for ad in ads if ad.latitude and ad.longitude]
    return JsonResponse(data, safe=False)

