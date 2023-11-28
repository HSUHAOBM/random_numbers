from django.urls import path
from . import views

urlpatterns = [
    path('number/get/<int:num_count>/<str:identifier>/', views.number_get),
    path('number/show/<int:num_count>/<str:identifier>/', views.number_show),
    path('number/init/<int:num_count>/<str:identifier>/', views.number_init),

    path('', views.main),
    path('random_number/<int:num_count>/<str:identifier>/', views.random_number, name='random_number'),

]