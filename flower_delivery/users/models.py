from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True)  # Добавляем поле для Telegram

    def __str__(self):
        return self.username
