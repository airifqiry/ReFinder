import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ad
from .uttils import get_image_embedding

@receiver(post_save, sender=Ad)
def generate_embedding_for_new_ad(sender, instance, created, **kwargs):
    if created:  # само при създаване на нова обява
        print(f"Generating embedding for new ad: {instance.id}")
        image_path = instance.image.path  # Път до изображението
        embedding = get_image_embedding(image_path)  # Генериране на embedding
        # Сериализиране на embedding към текст (JSON низ)
        instance.embedding = json.dumps(embedding)  # Записване на embedding като текст
        instance.save()  # Спестяваме промените
