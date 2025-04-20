from django.db import models
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim


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
    location = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if (not self.latitude or not self.longitude) and self.location:
            try:
                geolocator = Nominatim(user_agent="refinder")
                location_data = geolocator.geocode(self.location)
                if location_data:
                    self.latitude = location_data.latitude
                    self.longitude = location_data.longitude
            except Exception as e:
                print(f"❌ Грешка при геокодиране: {e}")

        super().save(*args, **kwargs)



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
