from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser  # Используем CustomUser вместо стандартного User
from orders.models import Order

class UserRegistrationTests(TestCase):
    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'Testpass123',
            'password2': 'Testpass123',
            'email': 'testuser@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление после успешной регистрации
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())  # Проверяем наличие пользователя


class UserLoginTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='Testpass123')  # Создаем пользователя

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'Testpass123',
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление после успешного входа


class ProfileUpdateTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='Testpass123')  # Создаем пользователя
        self.client.login(username='testuser', password='Testpass123')  # Логинимся

    def test_profile_update_view(self):
        response = self.client.get(reverse('profile_update'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_update.html')

    def test_profile_update(self):
        response = self.client.post(reverse('profile_update'), {
            'username': 'updateduser',
            'email': 'updated@example.com',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')


class OrderHistoryTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='Testpass123')  # Создаем пользователя
        self.client.login(username='testuser', password='Testpass123')  # Логинимся
        Order.objects.create(user=self.user, status='new', delivery_address='Test address')  # Создаем заказ

    def test_order_history_view(self):
        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/order_history.html')
        self.assertContains(response, 'Заказ #')
