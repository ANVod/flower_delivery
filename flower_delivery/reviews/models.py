from django.conf import settings
from django.db import models
from catalog.models import Flower
from users.models import CustomUser
from django.db.models import Avg

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(default=1)
    text = models.TextField()  # Текст отзыва
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} on {self.flower.name}'

    @staticmethod
    def get_average_rating(flower_id):
        return Review.objects.filter(flower_id=flower_id).aggregate(Avg('rating'))['rating__avg'] or 0
