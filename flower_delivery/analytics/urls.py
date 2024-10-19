from django.urls import path
from . import views

urlpatterns = [
    path('order-report/', views.order_report, name='order_report'),
    path('order-report/csv/', views.order_report_csv, name='order_report_csv'),
]
