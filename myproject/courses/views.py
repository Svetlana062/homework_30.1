import django_filters
from rest_framework import viewsets, generics, filters

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from ..users.models import Payment


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для курса (поддерживает все CRUD операции)."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreate(generics.ListCreateAPIView):
    """Generic-классы для урока (поддерживают все операции)."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """APIView для получения, обновления или удаления конкретного урока по его ID."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class PaymentFilter(django_filters.FilterSet):
    """Фильтрация и сортировка для списка платежей."""
    course_id = django_filters.NumberFilter(field_name='course__id')
    lesson_id = django_filters.NumberFilter(field_name='lesson__id')
    payment_method = django_filters.CharFilter(field_name='payment_method')

    class Meta:
        model = Payment
        fields = ['course_id', 'lesson_id', 'payment_method']


class PaymentViewSet(viewsets.ModelViewSet):
    """Обновленный ViewSet для платежей."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
