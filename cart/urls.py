from abc import abstractproperty
from django.urls import path
from .views import CartDetailApi, AddToCartApi, DeleteProductFromCartApi, DeleteCartApi


app_name = 'cart'
urlpatterns = [
    path('', CartDetailApi.as_view(), name='cart_detail_api'),
    path('add/', AddToCartApi.as_view(), name='add_to_cart_api'),
    path('delete/', DeleteProductFromCartApi.as_view(),
         name='delete_product_from_cart_api'),
    path('clear/', DeleteCartApi.as_view(), name='clear_cart_api')
]
