from rest_framework.pagination import PageNumberPagination
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework import  status, generics
from django.core.cache import cache
from django.conf import settings
from comment.serializers import CommentSeralizer
from comment.models import Comment
from .serilalizers import ArticleListSerializer, ArticleDetailSerializer
from .models import Article


class ArticlePagination(PageNumberPagination):
    page_size = settings.PAGINATION_PRODUCT 
    page_size_query_param = 'page_size'
    max_page_size = settings.PAGINATION_MAX_PRODUCT   


class ArticleListApi(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    pagination_class = ArticlePagination
    search_fields = ('title','body')

    def get_queryset(self):
        queryset = None
        if 'articles' in cache:
            queryset = cache.get('articles')
        else :
            queryset = Article.objects.all()
            cache.set('articles', queryset, settings.CACHE_TIMEOUT_PRODUCTS)

        return queryset


class ArticleDetailApi(generics.GenericAPIView):
    serializer_class =ArticleDetailSerializer

    def get(self, request, slug, pk):

        try :
            queryset = Article.objects.get(pk=pk, slug=slug)
        except Article.DoesNotExist:
            content = {'error':'article does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        data = self.serializer_class(queryset).data
        return Response(data, status=status.HTTP_200_OK)


class ArticleCommentApi(generics.GenericAPIView):
    serializer_class = CommentSeralizer

    def get(self, requset , pk):
        print(pk)
        try :
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            content = {'error':'article doesfd not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter_by_instance(article)
        data = self.serializer_class(comments,many=True)

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        try :
            article = Article.objects.get(id=validated_data['object_id'])
        except Article.DoesNotExist:
            content = {'error':'article doesfd not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        Comment.objects.create(
            fullname = validated_data['fullname'],
            body = validated_data['body'],
            rate = validated_data['rate'],
            content_object = article
        )

        content = {'success':'comment added'}
        return Response(content, status=status.HTTP_201_CREATED)           