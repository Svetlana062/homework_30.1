from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Форма для создания нового пользователя."""

    class Meta:
        model = CustomUser
        fields = ["username", "email", "avatar", "phone_number", "city"]


class RegistrationForm(UserCreationForm):
    """Форма для регистрации нового пользователя."""

    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "avatar",
            "phone_number",
            "city",
        )


class LoginForm(AuthenticationForm):
    """Форма входа пользователя."""

    username = forms.EmailField(label="Email")
