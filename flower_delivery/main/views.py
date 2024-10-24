from django.shortcuts import render
from catalog.models import Flower

def index(request):
    # Фильтруем цветы по критерию распродажи или новинок сезона
    flowers = Flower.objects.filter(is_on_sale=True)  # Добавьте поле в модели для распродаж или новинок
    return render(request, 'index.html', {'flowers': flowers})
