from rest_framework import serializers
from .models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор модели Course для преобразования данных в формат JSON и обратно."""
    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description']

class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор модели Lesson для преобразования данных в формат JSON и обратно."""
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_link']
