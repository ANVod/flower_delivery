from django.urls import path
from . import views

app_name = 'orders'  # Пространство имен для маршрутов

urlpatterns = [
    path('create/', views.order_create, name='order_create'),  # Маршрут для создания заказа
    path('history/', views.order_history, name='order_history'),
    path('report/', views.order_report, name='order_report'),  # Отчет в HTML
    path('report/csv/', views.order_report_csv, name='order_report_csv'),  # Отчет в формате CSV
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:flower_id>/', views.cart_add, name='cart_add'),  # Добавление товара в корзину
    path('cart/remove/<int:flower_id>/', views.cart_remove, name='cart_remove'),
]
