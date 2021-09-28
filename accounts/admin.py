from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile
from .forms import CustomUserChangeFrom, CustomUserCreationFrom


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeFrom
    add_form = CustomUserCreationFrom
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': 
            ('is_active', 'is_staff', 'is_superuser', 'is_provider', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    inlines = (ProfileInline,)
