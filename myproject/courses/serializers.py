from rest_framework import serializers
from .models import Course, Lesson
from ..users.models import CustomUser, Payment


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор модели Course для преобразования данных в формат JSON и обратно."""
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview_image', 'description', 'lessons_count']

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор модели Lesson для преобразования данных в формат JSON и обратно."""
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


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей."""
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Payment
        fields = ['id', 'user_email', 'payment_date', 'course', 'lesson', 'amount', 'payment_method']


class UserPaymentHistorySerializer(serializers.ModelSerializer):
    """Вывод истории платежей для профиля пользователя."""
    payments = PaymentSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'payments']
