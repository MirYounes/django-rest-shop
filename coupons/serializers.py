from rest_framework import serializers
from .models import Coupon


class AddCouponSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, value):
        try :
            coupon = Coupon.objects.get(code=value)
        except Coupon.DoesNotExist:
            raise serializers.ValidationError("coupon does not exist")
        
        return value