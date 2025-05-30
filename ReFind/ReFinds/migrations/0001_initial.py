

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=300)),
                ('image', models.ImageField(blank=True, null=True, upload_to='ads_images/')),
                ('location', models.CharField(blank=True, max_length=100)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=300)),
                ('status', models.CharField(choices=[('lost', 'Изгубено'), ('found', 'Намерено')], max_length=10)),
                ('category', models.CharField(choices=[('ключове', 'Ключове'), ('техника', 'Техника'), ('документ', 'Документ'), ('дреха', 'Дреха'), ('друго', 'Друго')], max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='item_images/')),
                ('location_lat', models.FloatField()),
                ('location_lng', models.FloatField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
