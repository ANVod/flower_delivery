from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('catalog/', include('catalog.urls')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('', include('main.urls')),
    path('reviews/', include('reviews.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('analytics/', include('analytics.urls', namespace='analytics')),  # Добавлено пространство имен
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
