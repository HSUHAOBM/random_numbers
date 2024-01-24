from django.urls import path
from . import views

urlpatterns = [
    # 取數字
    path('number/get/<str:identifier>/', views.number_get),
    # 顯示未抽
    path('number/show/<str:identifier>/', views.number_show),
    # 顯示已抽
    path('number/show_get/<str:identifier>/', views.number_get_show),
    # 初始化
    path('number/init/<str:identifier>/', views.number_init),
    # 網址檢查
    path('number/check/<str:identifier>/', views.url_check),
    # 數字輸入
    path('number/', views.main),
    # 數字抽取頁
    path('number/random/<str:identifier>',
         views.random_number, name='random_number'),
]
