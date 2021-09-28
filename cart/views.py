from .cart import Cart
from rest_framework import generics, serializers, status, permissions
from rest_framework.response import Response
from product.models import Product, Color
from.serializers import (
    AddToCartSerializer, DeleteFormCartSerializer
)


class CartDetailApi(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user_id = request.user.id
        data = Cart.get_cart(user_id)
        total_price = 0
        for item in data:
            total_price += float(item['price'])*int(item['quantity'])

        coupon = Cart.get_coupon_from_cart(user_id)
        discount = 0
        coupon_content = None
        if coupon:
            discount = (coupon.discount / float(100)) * total_price
            coupon_content = {
                'code': coupon.code or None,
                'discount': f'{coupon.discount}% ({discount})'
            }

        content = {
            'products': data,
            'coupon': coupon_content,
            'total_price': total_price - discount
        }

        return Response(content, status=status.HTTP_200_OK)


class AddToCartApi(generics.GenericAPIView):
    serializer_class = AddToCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user_id = request.user.id
        data = serializer.validated_data

        try:
            product = Product.objects.get(id=data['product_id'])
        except Product.DoesNotExist:
            raise serializers.ValidationError('product does not exist')

        try:
            color = Color.objects.get(name=data['color'])
        except Color.DoesNotExist:
            raise serializers.ValidationError('color does not exist')

        if color not in product.color.all():
            raise serializers.ValidationError(
                'this product does not have this color')

        Cart.add_cart(
            user_id=user_id,
            product_id=data['product_id'],
            color=data['color'],
            quantity=data['quantity'],
            price=str(product.price)
        )

        content = {'success': 'product added to cart'}
        return Response(content, status=status.HTTP_201_CREATED)


class DeleteProductFromCartApi(generics.GenericAPIView):
    serializer_class = DeleteFormCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = request.user.id
        product_id = serializer.validated_data['product_id']

        Cart.delete_product(user_id, product_id)
        content = {'success': 'product deleted from cart'}

        return Response(content, status=status.HTTP_200_OK)


class DeleteCartApi(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        user_id = request.user.id
        Cart.delete_cart(user_id)

        content = {'success': 'cart deleted'}
        return Response(content, status=status.HTTP_200_OK)
