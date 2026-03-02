from django.urls import path
from .views import blog_list, city_detail

urlpatterns = [
    path('', blog_list, name='blog_list'),
    path('<str:city_name>/', city_detail, name='city_detail'),
]
