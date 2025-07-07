from rest_framework import serializers
from .models import Course, Lesson
from users.models import CustomUser


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор модели Course для преобразования данных в формат JSON и обратно."""
    lessons_count = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.email')


    class Meta:
        model = Course
        fields = ['id', 'title', 'preview_image', 'description', 'lessons_count']

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор модели Lesson для преобразования данных в формат JSON и обратно."""
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'description', 'preview_image', 'video_link']


class CourseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор курса для вывода поля с уроками (подробный вывод)."""
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview_image', 'description', 'lessons_count', 'lessons']

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class UserPublicSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра чужих профилей."""
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone_number', 'city', 'avatar']
        # исключаем пароль, фамилию, историю платежей

class UserFullSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования своего профиля."""
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone_number', 'city', 'avatar', 'password']
