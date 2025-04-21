# ReFinds/management/commands/rebuild_embeddings.py

from django.core.management.base import BaseCommand
from ReFinds.models import Ad
from ReFinds.uttils import get_image_embedding
import json

class Command(BaseCommand):
    help = 'Rebuilds image embeddings for all ads'

    def handle(self, *args, **kwargs):
        updated = 0
        failed = 0

        for ad in Ad.objects.all():
            try:
                if not ad.image:
                    continue

                emb = get_image_embedding(ad.image.path)

                if all(v == 0.0 for v in emb):
                    self.stdout.write(self.style.WARNING(f"[{ad.id}] ❌ Invalid embedding"))
                    failed += 1
                    continue

                ad.embedding = json.dumps(emb)
                ad.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"[{ad.id}] ✅ Updated embedding"))

            except Exception as e:
                failed += 1
                self.stdout.write(self.style.ERROR(f"[{ad.id}] ⚠️ Error: {e}"))

        self.stdout.write(self.style.SUCCESS(f"🎉 Done. Updated: {updated}, Failed: {failed}"))
