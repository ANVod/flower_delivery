from django.urls import path
from . import views

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('reviews/add/<int:flower_id>/', views.add_review, name='add_review'),
]
