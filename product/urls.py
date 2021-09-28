from django.urls import path
from .views import ProductListApi, ProductDetailApi, ProductCommentApi


app_name = 'product'
urlpatterns = [
    path('comments/<int:pk>/',ProductCommentApi.as_view(), name='comments_list_api'),
    path('comments/add/<int:pk>/',ProductCommentApi.as_view(), name='add_comment_api'),
    path('', ProductListApi.as_view(), name='product_list_api'),
    path('<slug:slug>/<int:pk>/', ProductDetailApi.as_view(), name="product_detail_api"),

]
