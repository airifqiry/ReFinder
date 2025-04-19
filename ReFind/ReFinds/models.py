

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField  
import replicate 
import json


class Ad(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Изгубено'),
        ('found', 'Намерено'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='lost')
    image = models.ImageField(upload_to='ads_images/', blank=True, null=True)
    embedding = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.image and not self.embedding:
            try:
                model = replicate.models.get("laion-ai/clip-vit-b-32")
                image_url = self.image.url

                # ако URL не започва с http (локален път), добавяме домейн
                if not image_url.startswith("http"):
                    image_url = f"http://127.0.0.1:8000{self.image.url}"

                output = model.predict(image=image_url, input_type="image")
                self.embedding = json.dumps(output)
            except Exception as e:
                print("⚠️ Грешка при генериране на embedding:", e)

        super().save(*args, **kwargs)
        return self.title
    


class Chat(models.Model):
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Чат между: {', '.join([u.username for u in self.participants.all()])}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:30]}"




