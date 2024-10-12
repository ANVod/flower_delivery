from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # URL для регистрации и авторизации
    path('catalog/', include('catalog.urls')),  # URL для каталога цветов
    path('orders/', include('orders.urls', namespace='orders')),  # Подключение заказов с пространством имен
    path('', include('main.urls')),  # URL для главной страницы
    path('reviews/', include('reviews.urls')),  # URL для отзывов
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
