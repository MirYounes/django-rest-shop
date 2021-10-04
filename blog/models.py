from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField


User = get_user_model()


class Article(models.Model):
    STATUS = (
        ('draft','Draft'),
        ('publish', 'Publish')
    )
    user = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    body = RichTextField()
    status = models.CharField(choices=STATUS , max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    


