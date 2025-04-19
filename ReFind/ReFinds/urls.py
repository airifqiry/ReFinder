from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('home/', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('listing/', views.add_ad, name='listing'),
    path('ads-json/', views.ad_list_json, name='ads_json'),
    path('ads/', views.ad_list_view, name='ad_list'),
    path('ads/<int:ad_id>/', views.ad_detail_view, name='ad_detail'),
    path('chat/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('chat/start/<int:user_id>/', views.start_chat, name='start_chat'),
    path('chat/send/<int:chat_id>/', views.send_message, name='send_message'),
    path('chat/', views.chat_list, name='chat_list'),
    path('image-search/', views.image_search_view, name='image_search'),


]


