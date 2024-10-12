from django.shortcuts import render
from catalog.models import Flower

def index(request):
    flowers = Flower.objects.all()  # Получаем все цветы из базы данных
    return render(request, 'index.html', {'flowers': flowers})  # Передаем список цветов в шаблон
