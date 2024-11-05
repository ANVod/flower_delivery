from django.shortcuts import render
from orders.models import Order, OrderItem
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.conf import settings
from asgiref.sync import sync_to_async  # Импорт для использования асинхронных функций
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
import json
import csv

# Представление для HTML-отчета с кэшированием данных для графиков
@login_required
def order_report(request):
    # Попытка загрузки данных из кэша
    analytics_data = cache.get('order_report_data')

    if not analytics_data:
        # Выполнение агрегационных запросов
        order_status = Order.objects.values('status').annotate(count=Count('id'))
        total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
        popular_items = OrderItem.objects.values('flower__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]

        # Преобразование данных в JSON для использования в JavaScript
        analytics_data = {
            'order_status': list(order_status),
            'total_revenue': total_revenue,
            'popular_items': list(popular_items),
            'order_status_data': json.dumps(list(order_status)),
            'popular_items_data': json.dumps(list(popular_items)),
        }

        # Кэширование данных на 10 минут (600 секунд)
        cache.set('order_report_data', analytics_data, timeout=600)

    return render(request, 'analytics/order_report.html', analytics_data)

# Представление для скачивания отчета в PDF с кэшированием
@login_required
def order_report_pdf(request):
    user_id = request.user.id
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_report_user_{user_id}.pdf"'

    # Проверка кэша для PDF-отчета
    pdf_content = cache.get(f'order_report_pdf_{user_id}')

    if not pdf_content:
        # Создание PDF в памяти, если кэш пуст
        pdf = canvas.Canvas(response, pagesize=A4)
        pdf.setTitle("Отчет по заказам")
        font_path = os.path.join(settings.BASE_DIR, 'fonts', 'FreeSans.ttf')
        pdfmetrics.registerFont(TTFont('FreeSans', font_path))
        pdf.setFont("FreeSans", 12)
        pdf.drawString(100, 800, f"Отчет по заказам для пользователя ID: {user_id}")

        total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
        pdf.drawString(100, 780, f"Общий доход: {total_revenue} руб.")
        pdf.drawString(100, 760, "Статусы заказов:")

        y_position = 740
        for status in Order.objects.values('status').annotate(count=Count('id')):
            pdf.drawString(100, y_position, f"{status['status']}: {status['count']} заказов")
            y_position -= 20

        pdf.drawString(100, y_position - 20, "Популярные товары:")
        y_position -= 40
        popular_items = OrderItem.objects.values('flower__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
        for item in popular_items:
            pdf.drawString(100, y_position, f"{item['flower__name']}: {item['total_quantity']} шт.")
            y_position -= 20

        pdf.showPage()
        pdf.save()

        # Сохранение в кэш
        cache.set(f'order_report_pdf_{user_id}', response, timeout=600)

    return response

# Представление для скачивания отчета в CSV с кэшированием
@login_required
def order_report_csv(request):
    user_id = request.user.id
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="order_report_user_{user_id}.csv"'

    csv_content = cache.get(f'order_report_csv_{user_id}')

    if not csv_content:
        writer = csv.writer(response)
        writer.writerow(['Order ID', 'User', 'Total Price', 'Status', 'Created At'])

        orders = Order.objects.all()
        for order in orders:
            writer.writerow([order.id, order.user.username, order.total_price, order.status, order.created_at])

        # Кэширование CSV-данных
        cache.set(f'order_report_csv_{user_id}', response, timeout=600)

    return response
