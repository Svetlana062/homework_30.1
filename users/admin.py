from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Административный класс для модели CustomUser."""

    model = CustomUser
    list_display = ("id", "email", "username", "is_staff", "is_active")
    search_fields = ("email", "username")
    ordering = ("email",)
