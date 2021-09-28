from rest_framework import serializers
from product.models import Product , Color
from .cart import Cart


class CartDetailSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    product_id = serializers.CharField()
    color = serializers.CharField()
    price = serializers.CharField()
    quantity = serializers.CharField()


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    color = serializers.CharField()
    quantity= serializers.IntegerField()






class DeleteFormCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()