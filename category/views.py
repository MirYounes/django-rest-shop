from rest_framework.response import Response
from rest_framework import status, generics
from django.core.cache import cache
from django.conf import settings
from .models import Category
from .serializers import CategorySerializer


class CategoryListApi(generics.GenericAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = None
        if 'categories' in cache:
            queryset = cache.get('categories')
        else:
            queryset = Category.objects.all()
            cache.set('categories', queryset, settings.CACHE_TIMEOUT_CATEGORY)

        return queryset

    def get(self, request, format=None):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
