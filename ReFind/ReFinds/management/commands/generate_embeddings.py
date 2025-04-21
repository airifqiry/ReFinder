from django.core.management.base import BaseCommand
from ReFinds.models import Ad
from ReFinds.uttils import get_image_embedding
import json

class Command(BaseCommand):
    help = 'Генерира embedding-и за обяви без embedding'

    def handle(self, *args, **kwargs):
        ads = Ad.objects.filter(embedding__isnull=True).exclude(image='')

        if not ads.exists():
            self.stdout.write("✅ Всички обяви имат embedding.")
            return

        for ad in ads:
            try:
                print(f"🔄 Генерирам embedding за: {ad.title}")
                embedding = get_image_embedding(ad.image.path)
                ad.embedding = json.dumps(embedding)
                ad.save()
                print(f"✅ Успешно за {ad.title}")
            except Exception as e:
                print(f"❌ Проблем с {ad.title}: {e}")
