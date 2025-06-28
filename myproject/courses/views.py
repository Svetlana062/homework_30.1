from rest_framework import viewsets, generics

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


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
