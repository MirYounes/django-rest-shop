from django.urls import path, include


app_name = 'api'
urlpatterns = [
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('category/', include('category.urls', namespace='category')),
    path('products/', include('product.urls', namespace='product')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('coupon/',include('coupons.urls',namespace="coupons")),
    path('order/', include('order.urls', namespace='order')),
    path('blog/', include('blog.urls', namespace='blog'))
]
