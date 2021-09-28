from rest_framework import serializers
from .models import Article

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id','slug','user','status')


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        exclude = ('created',)