from django.core.exceptions import ValidationError


def validate_youtube_url(value):
    """Валидатор, который проверяет, что ссылка ведёт на youtube.com"""

    if not isinstance(value, str):
        raise ValidationError("Ссылка должна быть строкой.")
    if "youtube.com" not in value:
        raise ValidationError("Можно прикреплять только ссылки на YouTube.")