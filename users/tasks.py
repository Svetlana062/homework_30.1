from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import close_old_connections

User = get_user_model()


@shared_task
def block_inactive_users():
    """Блокировка неактивных пользователей."""
    close_old_connections()
    cutoff_date = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=cutoff_date, is_active=True)
    count = inactive_users.update(is_active=False)
    return f"Заблокировано {count} пользователей."
