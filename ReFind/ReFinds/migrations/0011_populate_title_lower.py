# Generated by Django 5.2 on 2025-04-26 15:34

from django.db import migrations

def update_title_lower(apps, schema_editor):
    Ad = apps.get_model('ReFinds', 'Ad')
    for ad in Ad.objects.all():
        ad.title_lower = ad.title.lower()
        ad.save()

class Migration(migrations.Migration):

    dependencies = [
        ('ReFinds', '0009_merge_20250422_0600'),  # <--- this must match your previous migration
    ]

    operations = [
        migrations.RunPython(update_title_lower),
    ]
