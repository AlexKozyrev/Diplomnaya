# your_app/urls.py
from django.urls import path
from .views import search_car, dashboard

urlpatterns = [
    path('search/', search_car, name='search_car'),
    path('', dashboard, name='dashboard'),
]