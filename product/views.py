from django.db.models import query
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import  serializers, status, generics
from django.core.cache import cache
from django.conf import settings
from comment.serializers import CommentSeralizer
from comment.models import Comment
from .serializers import ProductListSerializer, ProductDetailSerializer
from .models import Product


class ProductPagination(PageNumberPagination):
    page_size = settings.PAGINATION_PRODUCT 
    page_size_query_param = 'page_size'
    max_page_size = settings.PAGINATION_MAX_PRODUCT   


class ProductListApi(generics.ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = ProductPagination
    filterset_fields = ('category','available','price',)
    search_fields = ('title','description')
    order_fileds = ('price',)

    def get_queryset(self):
        queryset = None
        if 'products' in cache:
            queryset = cache.get('products')
        else :
            queryset = Product.objects.all()
            cache.set('products', queryset, settings.CACHE_TIMEOUT_PRODUCTS)

        return queryset



class ProductDetailApi(generics.GenericAPIView):
    serializer_class = ProductDetailSerializer

    def get(self, request, slug, pk):
        queryset = None
        try :
            queryset = Product.objects.get(slug=slug, pk=pk)
        except Product.DoesNotExist:
            content = {'error':'product does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        related_queryset = queryset.tags.similar_objects()[:5]
        product = self.serializer_class(queryset).data
        similar_products = ProductListSerializer(related_queryset, many=True).data 

        content = {
            'product': product,
            'similar_products': similar_products
        }
        return Response(content, status=status.HTTP_200_OK)


class ProductCommentApi(generics.GenericAPIView):
    serializer_class = CommentSeralizer

    def get(self, requset , pk):
        print(pk)
        try :
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            content = {'error':'product does notfds exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter_by_instance(product)
        data = self.serializer_class(comments,many=True)

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        try :
            product = Product.objects.get(id=validated_data['object_id'])
        except Product.DoesNotExist:
            content = {'error':'product does notfd exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        Comment.objects.create(
            fullname = validated_data['fullname'],
            body = validated_data['body'],
            rate = validated_data['rate'],
            content_object = product
        )

        content = {'success':'comment added'}
        return Response(content, status=status.HTTP_201_CREATED)                                
