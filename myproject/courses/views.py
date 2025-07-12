from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Course, Lesson, Subscription
from .paginations import CustomPagination
from .permissions import IsOwnerOrReadOnly, IsModeratorOrReadOnly
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для курса (поддерживает все CRUD операции)."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class LessonListCreate(generics.ListCreateAPIView):
    """Generic-классы для урока (поддерживают все операции)."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorOrReadOnly]
    pagination_class = CustomPagination

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


class SubscriptionToggleAPIView(APIView):
    """Эндпоинт для установки подписки пользователя и на удаление подписки у пользователя."""

    permission_classes = [IsAuthenticated]  # Требуется авторизация

    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response({"error": "Не указан ID курса."}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, id=course_id)

        subscription_qs = Subscription.objects.filter(user=user, course=course)

        if subscription_qs.exists():
            # Удаляем подписку
            subscription_qs.delete()
            message = 'Подписка удалена'
        else:
            # Создаём подписку
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response({"message": message})
