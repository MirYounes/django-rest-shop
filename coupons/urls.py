from django.urls import path
from .views import AddCouponApi


app_name = "coupons"
urlpatterns = [
    path('add/',AddCouponApi.as_view(), name="add_coupon")
]
