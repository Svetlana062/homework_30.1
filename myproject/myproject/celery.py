
from __future__ import absolute_import, unicode_literals
import eventlet
import os
from celery import Celery



eventlet.monkey_patch()

# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Создание экземпляра объекта Celery
app = Celery('myproject')

# Загрузка настроек из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()
