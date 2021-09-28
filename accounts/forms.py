from django import forms
from django .contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationFrom(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class CustomUserChangeFrom(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
