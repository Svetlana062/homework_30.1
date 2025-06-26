from django.contrib import admin
from .models import Course, Lesson

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Административный класс для модели Course.
    Определяет отображение в админке: поля для отображения и поиска."""
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Административный класс для модели Lesson.
    Настраивает отображение уроков в админке: поля для отображения и поиска."""
    list_display = ('title', 'course')
    search_fields = ('title', 'course__title')
