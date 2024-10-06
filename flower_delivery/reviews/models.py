from django.conf import settings
from django.db import models
from catalog.models import Flower
from users.models import CustomUser

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)
    text = models.TextField()  # Проверьте, что это поле присутствует в модели
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} on {self.flower.name}'