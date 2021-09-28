from django.db import models
from category.models import Category
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


class Color(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    price = models.DecimalField(max_digits=5 , decimal_places=2)
    category = models.ForeignKey(Category, related_name='profucts', on_delete=models.CASCADE)
    color = models.ManyToManyField(Color)
    available = models.BooleanField(default=True)
    tags = TaggableManager()
    description = RichTextField()
    image = models.ImageField(upload_to='products/image/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.title}-{self.id}'


class Gallery(models.Model):
    product = models.ForeignKey(Product, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'
    
