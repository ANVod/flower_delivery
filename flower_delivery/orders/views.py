from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from catalog.models import Flower
from .cart import Cart
from django.db.models import Sum, Count
from .forms import OrderForm

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})

def cart_add(request, flower_id):
    cart = Cart(request)
    flower = get_object_or_404(Flower, id=flower_id)
    cart.add(flower=flower)
    return redirect('cart_detail')

def cart_remove(request, flower_id):
    cart = Cart(request)
    flower = get_object_or_404(Flower, id=flower_id)
    cart.remove(flower)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart_detail.html', {'cart': cart})

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            # Привязываем товары из корзины к заказу
            for item in cart:
                order.items.create(flower=item['flower'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {
        'form': form,
        'cart': cart,  # Передаем корзину в шаблон
        'total_price': cart.get_total_price()  # Передаем общую стоимость
    })

def order_report(request):
    orders = Order.objects.all()
    total_orders = orders.count()
    total_revenue = orders.aggregate(Sum('flowers__price'))['flowers__price__sum']
    orders_by_status = orders.values('status').annotate(total=Count('id'))

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'orders_by_status': orders_by_status,
        'orders': orders,
    }

    return render(request, 'orders/order_report.html', context)

def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})
