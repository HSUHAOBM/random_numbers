from django.urls import path
from . import views

urlpatterns = [
    # 取值
    path('item/get/<str:identifier>/', views.item_get),
    # 顯示未抽
    path('item/show/<str:identifier>/', views.item_show),
    # 顯示已抽
    path('item/show_get/<str:identifier>/', views.item_get_show),
    # 初始化
    path('item/init/<str:identifier>/', views.item_init),
    # 網址檢查
    path('item/check/<str:identifier>/', views.url_check),
    # 值輸入
    path('item/', views.main, name='item'),
    # 抽取頁
    path('item/random/<str:identifier>', views.item_result),
]
