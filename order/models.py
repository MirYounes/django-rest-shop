from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product, Color


User= get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    address = models.TextField()
    create = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    color = models.ForeignKey(Color , on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
