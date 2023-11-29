from django.urls import path
from . import views

urlpatterns = [

    path('item/get/<str:identifier>/', views.item_get),
    path('item/show/<str:identifier>/', views.item_show),
    path('item/init/<str:identifier>/', views.item_init),
    path('item/check/<str:identifier>/', views.url_check),


    path('item/', views.main, name='item'),
    path('item/random/<str:identifier>', views.item_result),

]