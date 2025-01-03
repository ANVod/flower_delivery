# Generated by Django 5.1.1 on 2024-10-19 09:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('rating', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('flower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catalog_reviews', to='catalog.flower')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catalog_reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
