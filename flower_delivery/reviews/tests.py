from django.test import TestCase
from django.urls import reverse
from .models import Review
from catalog.models import Flower
from users.models import CustomUser

class ReviewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='Testpass123')
        self.flower = Flower.objects.create(name='Test Flower', price=10)

    def test_add_review(self):
        self.client.login(username='testuser', password='Testpass123')
        response = self.client.post(reverse('add_review', args=[self.flower.id]), {
            'rating': 5,
            'comment': 'Great flower!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(user=self.user, flower=self.flower).exists())
