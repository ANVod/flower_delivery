from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Cart, CartItem
from catalog.models import Flower
from .forms import OrderForm
from django.db.models import Sum, Count
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import csv
import telegram

# Отправка email о статусе заказа
def send_order_status_email(order):
    subject = f'Ваш заказ #{order.id} изменил статус'
    message = f'Уважаемый {order.user.username},\n\nВаш заказ #{order.id} был обновлен. Текущий статус: {order.status}.'
    recipient = order.user.email
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])

# Отправка уведомления в Telegram о статусе заказа
def send_order_status_telegram(order):
    bot_token = 'YOUR_BOT_TOKEN'
    chat_id = order.user.telegram_chat_id
    message = f'Ваш заказ #{order.id} изменил статус на: {order.status}'
    bot = telegram.Bot(token=bot_token)
    bot.send_message(chat_id=chat_id, text=message)

# Повторный заказ
@login_required
def repeat_order(request, order_id):
    previous_order = get_object_or_404(Order, id=order_id, user=request.user)
    cart, created = Cart.objects.get_or_create(user=request.user)

    for item in previous_order.items.all():
        cart_item, created = CartItem.objects.get_or_create(cart=cart, flower=item.flower)
        cart_item.quantity = item.quantity
        cart_item.save()

    return redirect('orders:cart_detail')

# Создание заказа
@login_required
def order_create(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()  # Получаем все элементы корзины
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total_price()
            order.save()

            # Добавляем товары из корзины в заказ
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    flower=item.flower,
                    quantity=item.quantity
                )
            cart_items.delete()  # Очищаем корзину после оформления заказа
            return redirect('orders:order_detail', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {
        'form': form,
        'cart_items': cart_items,  # Передаем элементы корзины, а не сам объект корзины
        'total_price': cart.get_total_price()
    })

# История заказов
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})

# Отчет по заказам (HTML)
@login_required
def order_report(request):
    orders = Order.objects.all()

    total_orders = orders.count()
    total_revenue = orders.aggregate(Sum('total_price'))['total_price__sum']
    orders_by_status = orders.values('status').annotate(total=Count('id'))

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'orders_by_status': orders_by_status,
        'orders': orders,
    }

    return render(request, 'orders/order_report.html', context)

# Отчет по заказам (CSV)
@login_required
def order_report_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="order_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Customer', 'Total', 'Date'])

    orders = Order.objects.all()
    for order in orders:
        writer.writerow([order.id, order.user.username, order.total_price, order.created_at])

    return response

# Детали заказа
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})

# Детали корзины
@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'orders/cart_detail.html', {'cart': cart})

# Добавление товара в корзину
@login_required
def cart_add(request, flower_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    flower = get_object_or_404(Flower, id=flower_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, flower=flower)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('orders:cart_detail')

# Удаление товара из корзины
@login_required
def cart_remove(request, flower_id):
    cart = get_object_or_404(Cart, user=request.user)
    flower = get_object_or_404(Flower, id=flower_id)
    CartItem.objects.filter(cart=cart, flower=flower).delete()
    return redirect('orders:cart_detail')
