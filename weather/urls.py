from django.urls import path
from . import views

urlpatterns = [
    path('alerts/', views.weather_dashboard, name='weather_dashboard'),
]
