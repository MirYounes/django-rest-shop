from rest_framework import serializers
from product.serializers import OrderItemProductSerializer
from cart.cart import Cart
from product.models import Product, Color
from .models import Order, OrderItem



class OrderSeializer(serializers.Serializer):
    address = serializers.CharField(max_length=300)

    def create(self, validated_data):
        user = self.context['request'].user
        items = Cart.get_cart(user_id=user.id)
        if items == []:
            raise serializers.ValidationError('cart is empty')
        total_price = 0
        for item in items :
            total_price += float(item['price'])*int(item['quantity'])

        coupon = Cart.get_coupon_from_cart(user.id)
        discount = 0
        if coupon :
            discount = (coupon.discount / float(100)) * total_price    

        order = Order.objects.create(
            user = user,
            price = total_price-discount ,
            address = validated_data['address']
        )

        for item in items :
            OrderItem.objects.create(
                product = Product.objects.get(id=item['product_id']),
                order = order,
                color = Color.objects.get(name = item['color']),
                quantity = int(item['quantity']) 
            )
        Cart.delete_cart(user_id=user.id)
        return order


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderItemProductSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_items(self, obj):
        items = obj.items.all()
        return OrderItemSerializer(items, many=True).data
