from rest_framework import serializers

from .models import Course, Lesson
from .validators import validate_youtube_url


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор модели Course для преобразования данных в формат JSON и обратно."""

    lessons_count = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source="owner.email")
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "preview_image",
            "description",
            "lessons_count",
            "is_subscribed",
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.subscribers.filter(user=user).exists()
        return False


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор модели Lesson для преобразования данных в формат JSON и обратно."""

    owner = serializers.ReadOnlyField(source="owner.email")
    url = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            "id",
            "course",
            "title",
            "description",
            "preview_image",
            "video_link",
            "owner",
            "url",
        ]

    def get_url(self, obj):
        request = self.context.get("request")
        if hasattr(obj, "get_absolute_url"):
            url = obj.get_absolute_url()
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return ""

    def validate_video_link(self, value):
        # Здесь вызывается ваш валидатор
        validate_youtube_url(value)
        return value


class CourseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор курса для вывода поля с уроками (подробный вывод)."""

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "preview_image",
            "description",
            "lessons_count",
            "lessons",
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.count()
