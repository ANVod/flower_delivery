from django.shortcuts import render, redirect
from .forms import UserRegisterForm, CustomUserUpdateForm  # Исправляем импорт формы
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from orders.models import Order  # Импортируем модель Order для истории заказов

# Функция отправки подтверждения регистрации
def send_registration_confirmation(user):
    subject = 'Подтверждение регистрации'
    message = f'Добро пожаловать, {user.username}!\n\nСпасибо за регистрацию на нашем сайте.'
    recipient = user.email
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])

# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}!')
            send_registration_confirmation(user)  # Отправляем уведомление после регистрации
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# Профиль пользователя
@login_required
def profile(request):
    return render(request, 'users/profile.html')

# Обновление профиля пользователя
@login_required
def profile_update(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен.')
            return redirect('profile')  # Перенаправление на страницу профиля после сохранения
    else:
        form = CustomUserUpdateForm(instance=request.user)

    return render(request, 'users/profile_update.html', {'form': form})

# История заказов пользователя
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)  # Фильтрация заказов по пользователю
    return render(request, 'users/order_history.html', {'orders': orders})
