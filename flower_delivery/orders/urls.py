from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('history/', views.order_history, name='order_history'),
    path('repeat/<int:order_id>/', views.repeat_order, name='repeat_order'),
    path('report/', views.order_report, name='order_report'),
    path('report/csv/', views.order_report_csv, name='order_report_csv'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:flower_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:flower_id>/', views.cart_remove, name='cart_remove'),
]
