from django.db import models

class Flower(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='flowers/')  # Изображение цветка
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField()  # Количество на складе

    def __str__(self):
        return self.name
