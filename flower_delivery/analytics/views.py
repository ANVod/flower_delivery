from django.shortcuts import render
from orders.models import Order, OrderItem
from django.db.models import Count, Sum
from django.http import HttpResponse
import csv
import telegram
from django.conf import settings
from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os

# Представление для HTML-отчета
@login_required
def order_report(request):
    order_status = Order.objects.values('status').annotate(count=Count('id'))
    total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    popular_items = OrderItem.objects.values('flower__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]

    context = {
        'order_status': order_status,
        'total_revenue': total_revenue,
        'popular_items': popular_items,
    }
    return render(request, 'analytics/order_report.html', context)

# Представление для скачивания отчета в PDF
@login_required
def order_report_pdf(request):
    user_id = request.user.id
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_report_user_{user_id}.pdf"'

    # Создаем PDF
    pdf = canvas.Canvas(response, pagesize=A4)
    pdf.setTitle("Отчет по заказам")

    # Подключаем шрифт, поддерживающий кириллицу
    font_path = os.path.join(settings.BASE_DIR, 'fonts', 'FreeSans.ttf')
    pdfmetrics.registerFont(TTFont('FreeSans', font_path))
    pdf.setFont("FreeSans", 12)

    # Заголовок
    pdf.drawString(100, 800, f"Отчет по заказам для пользователя ID: {user_id}")

    # Данные для отчета
    orders = Order.objects.all()
    total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    pdf.drawString(100, 780, f"Общий доход: {total_revenue} руб.")

    # Статусы заказов
    pdf.drawString(100, 760, "Статусы заказов:")
    y_position = 740
    for status in Order.objects.values('status').annotate(count=Count('id')):
        pdf.drawString(100, y_position, f"{status['status']}: {status['count']} заказов")
        y_position -= 20

    # Популярные товары
    pdf.drawString(100, y_position - 20, "Популярные товары:")
    y_position -= 40
    popular_items = OrderItem.objects.values('flower__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
    for item in popular_items:
        pdf.drawString(100, y_position, f"{item['flower__name']}: {item['total_quantity']} шт.")
        y_position -= 20

    pdf.showPage()
    pdf.save()

    return response

# Представление для скачивания отчета в CSV
@login_required
def order_report_csv(request):
    user_id = request.user.id
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="order_report_user_{user_id}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'User', 'Total Price', 'Status', 'Created At'])

    # Записываем данные о заказах в CSV
    orders = Order.objects.all()
    for order in orders:
        writer.writerow([order.id, order.user.username, order.total_price, order.status, order.created_at])

    return response
