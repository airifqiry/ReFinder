

# Create your models here.
from django.db import models
from django.contrib.auth.models import User



class Ad(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Изгубено'),
        ('found', 'Намерено'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='lost')
    image = models.ImageField(upload_to='ads_images/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



