from django.urls import path
from .views import CategoryListApi


app_name='category'
urlpatterns = [
    path('list/', CategoryListApi.as_view(), name='category_list_api'),
]

