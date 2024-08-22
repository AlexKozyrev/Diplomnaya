from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_car, name='search_car'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('authenticated/', views.authenticated_home, name='authenticated_home'),
    path('api/reference-description/', views.reference_description, name='reference_description'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('car/<int:car_id>/maintenance/<int:maintenance_id>/', views.maintenance_detail, name='maintenance_detail'),
    path('maintenance/<int:maintenance_id>/', views.maintenance_details, name='maintenance_details'),
    path('car/<int:car_id>/complaint/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    path('complaint/<int:complaint_id>/', views.complaint_details, name='complaint_details'),
    path('reference/<str:category>/<str:name>/', views.reference_detail, name='reference_detail'),
]