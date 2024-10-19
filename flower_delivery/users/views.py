from django.shortcuts import render, redirect
from .forms import UserRegisterForm, CustomUserUpdateForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from orders.models import Order

# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Аккаунт создан для {user.username}!')
            return redirect('catalog:catalog_list')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# Профиль пользователя
@login_required
def profile(request):
    return render(request, 'users/profile.html')

# Обновление профиля
@login_required
def profile_update(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен.')
            return redirect('profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)
    return render(request, 'users/profile_update.html', {'form': form})

# История заказов пользователя
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'users/order_history.html', {'orders': orders})
