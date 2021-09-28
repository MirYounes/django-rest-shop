from django.urls import path
from .views import ArticleListApi, ArticleDetailApi, ArticleCommentApi

app_name = 'blog'
urlpatterns = [
    path('',ArticleListApi.as_view(), name='article_list_api'),
    path('comments/<int:pk>/',ArticleCommentApi.as_view(), name='comments_list_api'),
    path('comments/add/<int:pk>/',ArticleCommentApi.as_view(), name='add_comment_api'),
    path('<slug:slug>/<int:pk>/', ArticleDetailApi.as_view(), name='article_detail_api'),

]
