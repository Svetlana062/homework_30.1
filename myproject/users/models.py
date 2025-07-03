from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    """Модель пользователя, содержащая поля для авторизации."""
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


class Payment(models.Model):
    """Модель платежей."""
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('bank_transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь'
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey('courses.Course', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Курс')
    lesson = models.ForeignKey('courses.Lesson', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Урок')
    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты')

    def __str__(self):
        return f"Платеж {self.id} пользователя {self.user.email}"
