from django.db import models
from django.conf import settings

class Flower(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='flowers/')  # Изображение цветка
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField()  # Количество на складе

    def __str__(self):
        return self.name

class Review(models.Model):#
    flower = models.ForeignKey(Flower, related_name='catalog_reviews', on_delete=models.CASCADE)  # Изменен related_name
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='catalog_reviews', on_delete=models.CASCADE)  # Изменен related_name
    text = models.TextField()
    rating = models.PositiveIntegerField()  # Рейтинг от 1 до 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отзыв {self.user.username} на {self.flower.name}"
