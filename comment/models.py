from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Comment(models.Model):
    RATES = (
        ('1','very bad'),
        ('2','bad'),
        ('3','good'),
        ('4','very good'),
        ('5','excellent')
    )
    fullname = models.CharField(max_length=200)
    body = models.TextField()
    rate = models.CharField(choices=RATES, max_length=20)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')