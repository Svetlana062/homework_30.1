from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя."""
    # поля для авторизации
    email = models.EmailField(unique=True, verbose_name='Email', help_text='Введите свой mail')
    avatar = models.ImageField(upload_to='accounts/avatars/', blank=True, null=True, verbose_name='Аватар', help_text='Загрузите свой аватар')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Телефон', help_text='Введите номер телефона')
    username = models.CharField(max_length=15, blank=True, null=True, verbose_name='Имя', help_text='Введите имя пользователя')
    city = models.CharField(max_length=50, blank=True, verbose_name='Город',help_text='Введите название города проживания')


    USERNAME_FIELD = 'email'  # делаем email полем для входа
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
