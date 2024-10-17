from django.urls import path
from . import views

urlpatterns = [
    path('order-report/', views.order_report, name='order_report'),
]
