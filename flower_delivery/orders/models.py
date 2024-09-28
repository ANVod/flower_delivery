from django.conf import settings
from django.db import models
from catalog.models import Flower

class Order(models.Model):
    # Используем AUTH_USER_MODEL для поддержки кастомной модели пользователя
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flowers = models.ManyToManyField(Flower)
    status = models.CharField(max_length=20, choices=[('new', 'New'), ('processing', 'Processing'), ('delivered', 'Delivered')])
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_address = models.CharField(max_length=255)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.flower.name}'

