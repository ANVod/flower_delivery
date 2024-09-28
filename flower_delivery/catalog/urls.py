from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog_list, name='catalog_list'),
    path('<int:flower_id>/', views.flower_detail, name='flower_detail'),
]
