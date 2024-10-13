from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from .forms import ReviewForm
from catalog.models import Flower
from django.contrib.auth.decorators import login_required

@login_required
def add_review(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.flower = flower
            review.save()
            return redirect('catalog:flower_detail', flower_id=flower.id)  # Редирект на страницу деталей цветка
    else:
        form = ReviewForm()
    return render(request, 'reviews/add_review.html', {'form': form, 'flower': flower})

def flower_reviews(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)
    reviews = Review.objects.filter(flower=flower)
    return render(request, 'reviews/flower_reviews.html', {'reviews': reviews, 'flower': flower})

def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})
