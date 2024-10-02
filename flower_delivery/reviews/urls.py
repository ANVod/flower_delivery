from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:flower_id>/', views.add_review, name='add_review'),
    path('<int:flower_id>/', views.flower_reviews, name='flower_reviews'),
]
