from django.core.management import BaseCommand
from myproject.users.models import CustomUser


class Command(BaseCommand):
    """Команда для создания суперпользователя с предустановленными
    данными (email, пароль, активность, статус администратора)."""
    def handle(self, *args, **options):
        user = CustomUser.objects.create(email="admin@example.com")
        user.set_password("123qwe")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
