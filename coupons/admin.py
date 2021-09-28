from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CategroyAdmin(admin.ModelAdmin):
    list_display = ['code','valid_to','discount']

