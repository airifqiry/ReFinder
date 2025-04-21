from django.db import models
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim
from .uttils import get_image_embedding
import json

class Ad(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Изгубено'),
        ('found', 'Намерено'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='lost')
    image = models.ImageField(upload_to='ads_images/', blank=True, null=True)
    embedding = models.TextField(blank=True, null=True)  # JSON-сериализирана листа от числа
    location = models.CharField(max_length=225, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.embedding and self.image:
            # Generate the embedding if it doesn't exist
            embedding = get_image_embedding(self.image.path)  # Assuming self.image.path returns the image path
            self.embedding = json.dumps(embedding)  # Save the embedding as a JSON string

        super().save(*args, **kwargs)  # Call the parent class's save method



class Chat(models.Model):
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Чат между: {', '.join([u.username for u in self.participants.all()])}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    reactions = models.JSONField(default=dict)  # {"❤️": 2, "😂": 1}
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:30]}"
