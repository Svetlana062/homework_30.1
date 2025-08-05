import os
from datetime import timedelta
from pathlib import Path
from celery.schedules import crontab

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",  # администрирование данных в Django-приложениях
    "django.contrib.auth",  # система аутентификации и авторизации пользователей
    "django.contrib.contenttypes",  # инфраструктура для работы с типами моделей, зарегистрированными в проекте
    "django.contrib.sessions",  # часть фреймворка, для обеспечения поддержки сессий для веб-приложений
    "django.contrib.messages",  # встроенный фреймворк сообщений, для отображения сообщения пользователям
    "django.contrib.staticfiles",  # встроенное приложение, для управления и обслуживания статических файлов
    "django_extensions", #  дополнительные команды и утилиты для фреймворка Django
    "django_celery_beat",  # расширение, позволяющее хранить расписание периодических задач в бд

    "rest_framework",  # подключаем DRF
    "rest_framework_simplejwt",  # подключаем JWT
    "drf_yasg",  # подключаем drf-yasg

    "users",  # приложение для регистрации/авторизации
    "courses",  # приложение для создания курса и уроков
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "myproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "myproject.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DATABASE_NAME"),
        "USER": os.getenv("DATABASE_USER"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "HOST": os.getenv("DATABASE_HOST"),
        "PORT": os.getenv("DATABASE_PORT", default="5432"),
        'CONN_MAX_AGE': 0,  # отключить persistent connections
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# использование кастомной модели пользователя для авторизации
AUTH_USER_MODEL = "users.CustomUser"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Настройки почты (для отправки писем)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.rambler.ru"  # используемый SMTP сервер
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# Используем Redis в качестве кеша
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",  # правильный путь для django-redis
        "LOCATION": os.getenv("REDIS_URL", "redis://redis:6379/1"),  # расположение Redis-сервера
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Настройки JWT-токенов
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",  # по умолчанию все защищены
    ),
}

# Настройки срока действия токенов
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

# Конфигурация для Swagger (инструмента для документирования и тестирования
# REST API), которая определяет способы аутентификации, используемые в нашем API.
SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {  # словарь, где описываются методы безопасности (аутентификации)
      'Basic': {  # базовая аутентификация HTTP (клиент отправляет логин и пароль в заголовке запроса)
            'type': 'basic'
      },
      'Bearer': {  # аутентификация по токену (у нас JWT), где токен передается в заголовке Authorization
            'type': 'apiKey',  # аутентификация происходит через API-ключ.
            'name': 'Authorization',  # имя HTTP-заголовка, в котором передается токен
            'in': 'header'  # указывает, что ключ (токен) передается в заголовке запроса
      }
   }
}

# Настройки для Celery

# URL-адрес брокера сообщений (Redis по умолчанию работает на порту 6379)
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')

# URL-адрес брокера результатов, также Redis
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", 'redis://redis:6379/0')

# Часовой пояс для работы Celery
CELERY_TIMEZONE = "UTC"

# Флаг отслеживания выполнения задач
CELERY_TASK_TRACK_STARTED = True

# Максимальное время на выполнение задачи
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_BEAT_SCHEDULE = {
    'deactivate_inactive_users_every_day': {
    'task': 'users.tasks.deactivate_inactive_users',
    'schedule': crontab(hour=0, minute=0),  # каждый день в 00:00
    },
}
