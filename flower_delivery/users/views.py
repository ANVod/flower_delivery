from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserUpdateForm
from orders.models import Order

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
from django.shortcuts import render

@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Перенаправление на страницу профиля после сохранения
    else:
        form = CustomUserUpdateForm(instance=request.user)

    return render(request, 'users/profile_update.html', {'form': form})
# Create your views here.
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'users/order_history.html', {'orders': orders})