from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db.models.fields import PositiveIntegerField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email_validator = EmailValidator()
    email = models.EmailField(_('email'), unique=True,
                              validators=[email_validator, ])
    is_provider = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(
        upload_to='avtars/', default='avatars/default.png')
    age = PositiveIntegerField(null=True, blank=True)
