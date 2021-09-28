from rest_framework.response import Response
from rest_framework import status, generics , permissions
from cart.cart import Cart
from .serializers import AddCouponSerializer


class AddCouponApi(generics.GenericAPIView):
    serializer_class = AddCouponSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        # Return a 400 response if the data was invalid.
        serializer.is_valid(raise_exception=True)

        user_id = request.user.id
        code = serializer.validated_data['code']
        
        # delete old coupon
        Cart.delete_coupon_from_cart(user_id)

        # add new coupon
        Cart.add_coupon_to_cart(
            user_id=user_id,
            code = code
        )

        content = {"message":"coupon added"}
        return Response(content, status=status.HTTP_200_OK)        