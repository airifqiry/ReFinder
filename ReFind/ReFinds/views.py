from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm,RegisterForm,AdForm,ImageSearchForm
from .models import Ad,Chat,Message
from django.http import JsonResponse
import requests,replicate
from django.contrib.auth.models import User
import numpy as np
from django.core.files.storage import default_storage
import json




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
    query = request.GET.get('q')
    status = request.GET.get('status')

    ads = Ad.objects.all()

    if query:
        ads = ads.filter(title__icontains=query)

    if status:
        ads = ads.filter(status=status)

    ads = ads.order_by('-created_at')
    return render(request, 'ads_list.html', {
        'ads': ads,
        'query': query,
        'selected_status': status  # 👉 за да пазим избора в HTML
    })



def ad_detail_view(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ad_detail.html', {'ad': ad})



def add_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user

            lat = form.cleaned_data.get('latitude')
            lng = form.cleaned_data.get('longitude')

            if lat and lng:
                ad.latitude = lat
                ad.longitude = lng
                ad.location = get_location_name(lat, lng)

            ad.save()  # ❗️ без това няма да влезе в базата
            messages.success(request, "Обявата беше добавена успешно!")
            return redirect('home')
        else:
            print("❌ Форма невалидна:", form.errors)  # 🧠 важно за дебъг
    else:
        form = AdForm()
    return render(request, 'listing.html', {'form': form})




def ad_list_json(request):
    query = request.GET.get('q')
    ads = Ad.objects.all()

    if query:
        ads = ads.filter(title__icontains=query)

    data = []
    for ad in ads:
        if ad.latitude and ad.longitude:
            data.append({
                'id': ad.id,
                'title': ad.title,
                'description': ad.description,
                'image': ad.image.url if ad.image else '',
                'latitude': ad.latitude,
                'longitude': ad.longitude,
                'location': ad.location,
            })
    return JsonResponse(data, safe=False)



def get_location_name(lat, lng):
    try:
        url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}&zoom=16&addressdetails=1'
        headers = {'User-Agent': 'refinder-app'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('display_name', '')
        return ''
    except:
        return ''


@login_required
def start_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    chat = Chat.objects.filter(participants=request.user).filter(participants=other_user).first()
    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, other_user)

    return redirect('chat_detail', chat_id=chat.id)


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.user not in chat.participants.all():
        return redirect('home')  # защита

    messages = Message.objects.filter(chat=chat).order_by('timestamp')
    other_user = chat.participants.exclude(id=request.user.id).first()

    return render(request, 'chat_detail.html', {
        'chat': chat,
        'messages': messages,
        'other_user': other_user  # 👈 подаваме другия участник
    })


@login_required
def send_message(request, chat_id):
    if request.method == 'POST':
        chat = get_object_or_404(Chat, id=chat_id)
        text = request.POST.get('text')
        if text:
            Message.objects.create(chat=chat, sender=request.user, text=text)
    return redirect('chat_detail', chat_id=chat_id)



@login_required
def chat_list(request):
    chats = Chat.objects.filter(participants=request.user).order_by('-created_at')
    chat_data = []

    for chat in chats:
        other_user = chat.participants.exclude(id=request.user.id).first()
        chat_data.append({
            'chat': chat,
            'other_user': other_user
        })

    return render(request, 'chat_list.html', {'chat_data': chat_data})





def cosine_similarity(v1, v2):
    v1, v2 = np.array(v1), np.array(v2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def image_search_view(request):
    results = []

    if request.method == 'POST':
        form = ImageSearchForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                image_file = request.FILES['image']
                model = replicate.models.get("laion-ai/clip-vit-b-32")
                uploaded_embedding = model.predict(image=image_file, input_type="image")

                scored_ads = []
                for ad in Ad.objects.all():
                    try:
                        if not ad.embedding:
                            ad_embedding = model.predict(image=ad.image.file, input_type="image")
                            ad.embedding = json.dumps(ad_embedding)
                            ad.save()
                        else:
                            ad_embedding = json.loads(ad.embedding)

                        score = cosine_similarity(uploaded_embedding, ad_embedding)
                        scored_ads.append((score, ad))

                    except Exception as e:
                        print(f"⚠️ Проблем с обява ID {ad.id}: {e}")

                scored_ads.sort(reverse=True, key=lambda x: x[0])
                results = [ad for score, ad in scored_ads[:6]]

            except Exception as e:
                print(f"❌ Replicate грешка: {e}")
    else:
        form = ImageSearchForm()

    return render(request, 'image_search.html', {
        'form': form,
        'results': results
    })
