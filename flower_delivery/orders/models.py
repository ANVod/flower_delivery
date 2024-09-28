from django.db import models
from users.models import CustomUser
from catalog.models import Flower

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    flowers = models.ManyToManyField(Flower)
    status = models.CharField(max_length=20, choices=[('new', 'New'), ('processing', 'Processing'), ('delivered', 'Delivered')])
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_address = models.CharField(max_length=255)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
