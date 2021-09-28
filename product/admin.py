from django.contrib import admin
from .models import Gallery, Product , Color


class GaleryAdmin(admin.StackedInline):
    model = Gallery


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','price','category','available']
    prepopulated_fields = {'slug':('title',)}
    list_filter = ['category','tags', 'updated']
    inlines = (GaleryAdmin,)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass