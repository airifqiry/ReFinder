from django.core.management.base import BaseCommand
from ReFinds.models import Ad
import replicate
import os
import json
from dotenv import load_dotenv

load_dotenv()  # зареждаме .env файла

class Command(BaseCommand):
    help = 'Генерира embedding-и за всички обяви без такива'

    def handle(self, *args, **kwargs):
        print("🔐 Replicate API ключ:", os.getenv("REPLICATE_API_TOKEN"))  # За проверка

        # 👉 Използваме работещ модел
        model = replicate.models.get("kakaobrain/clip-vit-base-patch32")

        ads = Ad.objects.filter(embedding__isnull=True, image__isnull=False)

        if not ads.exists():
            self.stdout.write(self.style.SUCCESS("✅ Всички обяви вече имат embedding."))
            return

        for ad in ads:
            try:
                print(f"🔄 Генерирам embedding за: {ad.title}")
                ad_embedding = model.predict(image=ad.image.file)
                ad.embedding = json.dumps(ad_embedding)
                ad.save()
                print(f"✅ Успешно за {ad.title}")
            except Exception as e:
                print(f"❌ Проблем с {ad.title}: {e}")
