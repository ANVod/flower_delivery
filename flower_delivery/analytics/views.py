from django.shortcuts import render
from orders.models import Order, OrderItem
from django.db.models import Count, Sum

# Представление для отчета по заказам
def order_report(request):
    # Количество заказов по статусам
    order_status = Order.objects.values('status').annotate(count=Count('id'))

    # Сумма всех заказов
    total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0

    # Самые популярные товары
    popular_items = OrderItem.objects.values('flower__name').annotate(total_quantity=Sum('quantity')).order_by(
        '-total_quantity')[:5]

    context = {
        'order_status': order_status,
        'total_revenue': total_revenue,
        'popular_items': popular_items,
    }
    return render(request, 'analytics/order_report.html', context)
