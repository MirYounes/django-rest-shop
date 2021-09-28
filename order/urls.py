from django.urls import path
from .views import OrderCreateApi, OrderListApi, OrderDetailApi


app_name = 'order'
urlpatterns = [
    path('',OrderListApi.as_view(), name='order_list_api'),
    path('<int:pk>/',OrderDetailApi.as_view(), name='order_detail_api'),
    path('create/', OrderCreateApi.as_view(), name='order_create_api')
]
