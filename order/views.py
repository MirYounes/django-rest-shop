from rest_framework import generics, serializers , status, permissions
from rest_framework.response import Response
from .serializers import OrderListSerializer, OrderDetailSerializer , OrderSeializer
from .models import Order, OrderItem


class OrderListApi(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user 
        queryset = Order.objects.filter(user = user)

        return queryset

class OrderDetailApi(generics.GenericAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try :
            querysset = Order.objects.get(user=request.user, pk=pk)
        except Order.DoesNotExist :
            content = {'error':'order does not exist'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(querysset)

        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCreateApi(generics.GenericAPIView):
    serializer_class = OrderSeializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data , context = {'request':request,})
        serializer.is_valid(raise_exception=True)

        order = serializer.save()

        content = {'success': 'order created'}
        return Response(content, status=status.HTTP_201_CREATED)        