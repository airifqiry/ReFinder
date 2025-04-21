from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import uuid
from .forms import LoginForm, RegisterForm, AdForm, ImageSearchForm
from .models import Ad, Chat, Message
from .uttils import get_image_embedding, cosine_similarity
import requests
import json
import numpy as np

# === Основни изгледи ===
def index_view(request):
    return render(request, 'index.html')

def home_view(request):
    return render(request, 'home.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

# === Регистрация и вход ===
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрацията беше успешна!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('home')
            messages.error(request, 'Невалидно потребителско име или парола.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# === Обяви ===
def ad_list_view(request):
    query = request.GET.get('q')
    status = request.GET.get('status')
    ads = Ad.objects.all()
    if query:
        ads = ads.filter(title__icontains=query)
    if status:
        ads = ads.filter(status=status)
    return render(request, 'ads_list.html', {'ads': ads.order_by('-created_at'), 'query': query, 'selected_status': status})


def get_location_name(lat, lng):
    try:
        url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}&zoom=16&addressdetails=1'
        headers = {'User-Agent': 'refinder-app'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('display_name', '')
    except:
        pass
    return ''

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
            if ad.image:
                try:
                    ad.embedding = json.dumps(get_image_embedding(ad.image.path))
                except Exception as e:
                    print(f"❌ Грешка при embedding: {e}")
            ad.save()
            messages.success(request, "Обявата беше добавена успешно!")
            return redirect('home')
        print("❌ Форма невалидна:", form.errors)
    else:
        form = AdForm()
    return render(request, 'listing.html', {'form': form})

# === Обяви в JSON формат за картата ===
def ad_list_json(request):
    query = request.GET.get('q')
    ads = Ad.objects.all()
    if query:
        ads = ads.filter(title__icontains=query)
    data = [
        {
            'id': ad.id,
            'title': ad.title,
            'description': ad.description,
            'image': ad.image.url if ad.image else '',
            'latitude': ad.latitude,
            'longitude': ad.longitude,
            'location': ad.location,
        }
        for ad in ads if ad.latitude and ad.longitude
    ]
    return JsonResponse(data, safe=False)



def image_search_view(request):
    results = []

    if request.method == 'POST':
        form = ImageSearchForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            path = default_storage.save('temp_search.jpg', image_file)
            full_path = default_storage.path(path)

            try:
                uploaded_embedding = get_image_embedding(full_path)
                if all(v == 0.0 for v in uploaded_embedding):
                    print("⚠️ Uploaded image resulted in zero embedding — possibly failed to process the image.")
                    return render(request, 'image_search.html', {
                        'form': form,
                        'results': [],
                        'error': 'Image could not be processed. Please try a different one.'
                    })

                scored_ads = []

                for ad in Ad.objects.all():
                    try:
                        # Generate embedding if missing
                        if not ad.embedding and ad.image:
                            emb = get_image_embedding(ad.image.path)
                            ad.embedding = json.dumps(emb)
                            ad.save()
                            print(f"🧠 Embedding generated and saved for '{ad.title}'")

                        if not ad.embedding:
                            continue  # Skip if still no embedding

                        ad_embedding = json.loads(ad.embedding)

                        # Skip if embedding is invalid (e.g. all zeros)
                        if not isinstance(ad_embedding, list) or all(v == 0.0 for v in ad_embedding):
                            print(f"⚠️ Invalid or zero embedding for ad ID {ad.id}")
                            continue

                        score = cosine_similarity(uploaded_embedding, ad_embedding)
                        similarity_percent = round(score * 100, 2)

                        scored_ads.append({
                            'ad': ad,
                            'similarity': similarity_percent
                        })

                    except Exception as e:
                        print(f"⚠️ Error processing ad '{ad.title}' (ID {ad.id}): {e}")
                        continue

                scored_ads.sort(key=lambda x: x['similarity'], reverse=True)
                results = scored_ads[:6]

            except Exception as e:
                print(f"❌ Error processing uploaded image: {e}")
    else:
        form = ImageSearchForm()

    return render(request, 'image_search.html', {
        'form': form,
        'results': results
    })





def ad_detail_view(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ad_detail.html', {'ad': ad})



#def add_ad(request):
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


def add_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            lat = form.cleaned_data.get('latitude')
            lng = form.cleaned_data.get('longitude')
            
            # Проверка за задължителни координати
            if not lat or not lng:
                messages.error(request, "Моля, изберете място на картата или използвайте автоматично местоположение.")
                return render(request, 'listing.html', {'form': form})

            ad.latitude = float(lat)
            ad.longitude = float(lng)
            ad.location = get_location_name(lat, lng)

            if ad.image:
                try:
                    ad.embedding = json.dumps(get_image_embedding(ad.image.path))
                except Exception as e:
                    print(f"❌ Грешка при embedding: {e}")

            ad.save()
            messages.success(request, "Обявата беше добавена успешно!")
            return redirect('home')
        else:
            print("❌ Формата невалидна:", form.errors)
            messages.error(request, "Моля, попълнете всички задължителни полета.")
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


@csrf_exempt
def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        filename = f"{uuid.uuid4()}.{image.name.split('.')[-1]}"
        path = default_storage.save(f"chat_images/{filename}", image)
        return JsonResponse({"url": f"{settings.MEDIA_URL}{path}"})
    return JsonResponse({"error": "Невалидна заявка"}, status=400)
