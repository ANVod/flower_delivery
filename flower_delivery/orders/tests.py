from django.test import TestCase
from django.urls import reverse
from orders.models import Order
from users.models import CustomUser

class OrderTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='Testpass123')

    def test_create_order(self):
        self.client.login(username='testuser', password='Testpass123')
        response = self.client.post(reverse('order_create'), {
            'delivery_address': '123 Test St',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(user=self.user).exists())

    def test_order_history(self):
        order = Order.objects.create(user=self.user, delivery_address='123 Test St', status='new')
        self.client.login(username='testuser', password='Testpass123')
        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 200)
        print(response.content.decode())
        self.assertContains(response, f'Заказ #{order.id}')  # Проверим ID заказа
        self.assertContains(response, '123 Test St')  # Проверим адрес



from django.test import TestCase

# Create your tests here.
