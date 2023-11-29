from django.urls import path
from . import views

urlpatterns = [
    path('number/get/<str:identifier>/', views.number_get),
    path('number/show/<str:identifier>/', views.number_show),
    path('number/init/<str:identifier>/', views.number_init),
    path('number/check/<str:identifier>/', views.url_check),

    path('number/', views.main),
    path('number/random/<str:identifier>', views.random_number, name='random_number'),

]