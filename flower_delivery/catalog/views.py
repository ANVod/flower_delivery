from django.shortcuts import render, get_object_or_404, redirect
from .models import Flower
from reviews.forms import ReviewForm
from reviews.models import Review

def index(request):
    # Получаем список всех цветов для отображения на главной странице
    flowers = Flower.objects.all()
    return render(request, 'main/index.html', {'flowers': flowers})

def catalog_list(request):
    flowers = Flower.objects.all()  # Получение всех цветов из базы
    return render(request, 'catalog/catalog_list.html', {'flowers': flowers})

def flower_detail(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)
    reviews = flower.reviews.all()  # Получение всех отзывов для конкретного цветка
    return render(request, 'catalog/flower_detail.html', {'flower': flower, 'reviews': reviews})

def add_review(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.flower = flower
            review.user = request.user
            review.save()
            return redirect('catalog:flower_detail', flower_id=flower_id)
    else:
        form = ReviewForm()
    return render(request, 'catalog/add_review.html', {'form': form, 'flower': flower})
