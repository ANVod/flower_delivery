from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.catalog_list, name='catalog_list'),
    path('flower/<int:flower_id>/', views.flower_detail, name='flower_detail'),
    path('add_review/<int:flower_id>/', views.add_review, name='add_review'),
]
