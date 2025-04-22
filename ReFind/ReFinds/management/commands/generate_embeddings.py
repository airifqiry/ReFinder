from django.core.management.base import BaseCommand
from ReFinds.models import Ad
from ReFinds.uttils import get_image_embedding
import json
import os

class Command(BaseCommand):
    help = 'Re-generates all ad embeddings using Clarifai'

    def handle(self, *args, **kwargs):
        updated = 0
        failed = 0

        ads = Ad.objects.all()

        for ad in ads:
            if not ad.image:
                continue

            try:
                print(f"🔄 Updating embedding for: {ad.title} (ID {ad.id})")
                image_path = ad.image.path

                if not os.path.exists(image_path):
                    print(f"❌ Image not found: {image_path}")
                    failed += 1
                    continue

                new_emb = get_image_embedding(image_path)

                if new_emb and isinstance(new_emb, list) and len(new_emb) >= 100:
                    ad.embedding = json.dumps(new_emb)
                    ad.save()
                    print(f"✅ Updated: {ad.title}")
                    updated += 1
                else:
                    print(f"⚠️ Skipped (invalid embedding): {ad.title}")
                    failed += 1

            except Exception as e:
                print(f"❌ Failed to update '{ad.title}' (ID {ad.id}): {e}")
                failed += 1

        print(f"\n✅ Embedding update complete: {updated} ads updated, {failed} failed.")