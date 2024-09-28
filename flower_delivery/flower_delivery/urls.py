from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # URL для регистрации и авторизации
    path('catalog/', include('catalog.urls')),  # URL для каталога цветов
    path('orders/', include('orders.urls')),  # URL для оформления заказов
    path('', include('main.urls')),  # URL для главной страницы (создадим позже)
]
