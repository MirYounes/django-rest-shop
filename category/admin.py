from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategroyAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields ={'slug':('name',)}
