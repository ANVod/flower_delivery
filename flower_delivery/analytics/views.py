from django.shortcuts import render
from orders.models import Order, OrderItem
from django.db.models import Count, Sum
from django.http import HttpResponse
import csv

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

# Представление для отчета в формате CSV
def order_report_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="order_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'User', 'Total Price', 'Status', 'Created At'])

    orders = Order.objects.all()
    for order in orders:
        writer.writerow([order.id, order.user.username, order.total_price, order.status, order.created_at])

    return response
