# ReFinds/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ad
from .uttils import get_image_embedding
import json
import os
import time  # ⬅️ Добавено за изчакване

@receiver(post_save, sender=Ad)
def generate_embedding_on_save(sender, instance, created, **kwargs):
    if not instance.image:
        return  # No image, skip

    try:
        # Check if embedding already exists and is valid
        if instance.embedding:
            data = json.loads(instance.embedding)
            if isinstance(data, list) and any(data):
                return  # Already has a valid embedding

        # Get image path
        image_path = instance.image.path

        # ⏳ Изчакай до 5 пъти (макс 2.5 секунди), докато файлът се появи
        for _ in range(5):
            if os.path.exists(image_path):
                break
            time.sleep(0.5)
        else:
            print(f"⚠️ Image not found at path after waiting: {image_path}")
            return

        # Генериране на embedding
        emb = get_image_embedding(image_path)
        if all(v == 0.0 for v in emb):
            print(f"⚠️ Skipped embedding: zero vector for Ad ID {instance.id}")
            return

        instance.embedding = json.dumps(emb)
        instance.save(update_fields=["embedding"])
        print(f"🧠 Embedding auto-saved for '{instance.title}' (ID {instance.id})")

    except Exception as e:
        print(f"❌ Embedding generation failed for Ad ID {instance.id}: {e}")
