# Generated by Django 5.1.1 on 2024-10-24 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='flower',
            name='is_on_sale',
            field=models.BooleanField(default=False),
        ),
    ]