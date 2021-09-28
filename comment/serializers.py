from django.db.models import fields
from rest_framework import serializers
from .models import Comment


class CommentSeralizer(serializers.ModelSerializer):
    object_id = serializers.IntegerField(write_only=True)
    class Meta :
        model = Comment
        fields = ('object_id','fullname','body','rate')