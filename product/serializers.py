from django.db.models import fields
from category.serializers import CategorySerializer
from taggit_serializer.serializers import (
    TagListSerializerField,
    TaggitSerializer
)
from rest_framework import serializers
from .models import Color, Gallery, Product


class ColorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('name', 'id')


class GallerySerializer(serializers.Serializer):
    class Meta:
        models = Gallery
        fields = ('image',)


class ProductDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    color = ColorListSerializer(many=True)
    gallery = serializers.SerializerMethodField()
    category = CategorySerializer()
    tags = TagListSerializerField()

    class Meta:
        model = Product
        exclude = ('created','slug')
    
    def get_gallery(self, obj):
        gallery = obj.gallery.all()
        return GallerySerializer(gallery, many=True).data


class ProductListSerializer(TaggitSerializer, serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ('title','price', 'available', 'category')


class OrderItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','title','price',)
    

