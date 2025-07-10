from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Course, Lesson
from .permissions import IsOwnerOrReadOnly, IsModeratorOrReadOnly
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для курса (поддерживает все CRUD операции)."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            # Всем разрешено просматривать
            permission_classes = [AllowAny]
        elif self.action == "create":
            # Создавать могут все авторизованные
            permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            # Обновлять и удалять — только модераторы или владельцы
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Автоматическая привязка текущего пользователя к создаваемому курсу."""
        serializer.save(owner=self.request.user)


class LessonListCreate(generics.ListCreateAPIView):
    """Generic-классы для урока (поддерживают все операции)."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            # Всем разрешено просматривать
            permission_classes = [AllowAny]
        elif self.action == "create":
            # Создавать могут все авторизованные
            permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            # Обновлять и удалять — только модераторы или владельцы
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Автоматическая привязка текущего пользователя к создаваемому уроку."""
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """APIView для получения, обновления или удаления конкретного урока по его ID."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorOrReadOnly]
