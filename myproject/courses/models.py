from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Course(models.Model):
    """Модель курса обучения."""

    title = models.CharField(max_length=255, verbose_name="Название курса")
    preview_image = models.ImageField(
        upload_to="course_previews/", verbose_name="Превью (изображение) курса"
    )
    description = models.TextField(verbose_name="Описание курса")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="courses", verbose_name="Владелец"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Модель урока внутри курса."""

    course: "Course" = models.ForeignKey(
        "Course", related_name="lessons", on_delete=models.CASCADE, verbose_name="Курс"
    )
    title = models.CharField(max_length=255, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока")
    preview_image = models.ImageField(
        upload_to="lesson_previews/", verbose_name="Превью (изображение) урока"
    )
    video_link = models.URLField(verbose_name="Ссылка на видео")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="lessons", verbose_name="Владелец"
    )

    def __str__(self):
        return f"{self.title} ({self.course.title})"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    """Модель подписки."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='subscribers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f"{self.user.username} подписан на {self.course.title}"
