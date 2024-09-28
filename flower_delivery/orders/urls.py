from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),  # Страница со списком заказов
    path('<int:order_id>/', views.order_detail, name='order_detail'),# Детали заказа
    path('cart/add/<int:flower_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:flower_id>/', views.cart_remove, name='cart_remove'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('create/', views.order_create, name='order_create'),
]
