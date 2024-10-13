from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser

# Форма для регистрации пользователя
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()  # Используем кастомную модель пользователя
        fields = ['username', 'email', 'password1', 'password2']

# Форма для обновления профиля пользователя
class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'address']  # Поля кастомной модели
