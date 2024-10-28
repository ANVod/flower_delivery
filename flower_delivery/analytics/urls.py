from django.urls import path
from . import views

app_name = 'analytics'  # Пространство имен для маршрутов

urlpatterns = [
    path('order-report/', views.order_report, name='order_report'),
    path('order-report/csv/', views.order_report_csv, name='order_report_csv'),
    path('order-report/pdf/', views.order_report_pdf, name='order_report_pdf'),  # Новый маршрут для PDF
]
