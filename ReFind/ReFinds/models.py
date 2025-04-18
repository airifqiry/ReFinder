from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Изгубено'),
        ('found', 'Намерено'),
    ]

    CATEGORY_CHOICES = [
        ('ключове', 'Ключове'),
        ('техника', 'Техника'),
        ('документ', 'Документ'),
        ('дреха', 'Дреха'),
        ('друго', 'Друго'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    location_lat = models.FloatField()
    location_lng = models.FloatField()
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Ad(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    image = models.ImageField(upload_to='ads_images/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


