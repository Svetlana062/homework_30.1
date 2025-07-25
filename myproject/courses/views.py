from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Lesson, Subscription
from .paginations import CustomPagination
from .permissions import IsModerator, IsOwnerOrReadOnly
from .serializers import CourseSerializer, LessonSerializer
from .tasks import send_course_update_email


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для курса (поддерживает все CRUD операции)."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly | IsModerator,
    ]

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
        context["request"] = self.request
        return context

    def update(self, request, *args, **kwargs):
        """Асинхронная рассылка писем при обновлении курса."""
        # Выполняем стандартное обновление
        response = super().update(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            # Получаем курс из сериализатора
            course = self.get_object()
            # Получение текущего времени
            now = timezone.now()

            # Проверяем, если last_updated отсутствует или прошло более 4 часов
            if not course.last_updated or (now - course.last_updated) > timedelta(
                hours=4
            ):
                # Получаем подписанных пользователей
                subscribers = course.subscribers.values_list("email", flat=True)
                for email in subscribers:
                    send_course_update_email.delay(email, course.title)
                # Обновить поле last_updated текущим временем
                course.last_updated = now
                course.save(update_fields=["last_updated"])
        return response


class LessonViewSet(viewsets.ModelViewSet):
    """ViewSet для урока (поддерживает все CRUD операции)."""

    queryset = Lesson.objects.all().order_by("id")
    serializer_class = LessonSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly | IsModerator,
    ]
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        elif self.action == "create":
            permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            # Разрешаем владельцу или модератору
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly | IsModerator]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        """При обновлении урока уведомляем подписчиков курса."""
        response = super().update(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            lesson = self.get_object()
            course = lesson.course
            now = timezone.now()
            # Проверяем, если last_updated отсутствует или прошло более 4 часов
            if not course.last_updated or (now - course.last_updated) > timedelta(
                hours=4
            ):
                subscribers = course.subscribers.values_list("email", flat=True)
                for email in subscribers:
                    send_course_update_email.delay(email, course.title)
                course.last_updated = now
                course.save(update_fields=["last_updated"])
        return response


class SubscriptionToggleAPIView(APIView):
    """Эндпоинт для установки подписки пользователя и на удаление подписки у пользователя."""

    permission_classes = [IsAuthenticated]  # Требуется авторизация

    def post(self, request):
        user = request.user
        course_id = request.data.get("course_id")

        if not course_id:
            return Response(
                {"error": "Не указан ID курса."}, status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)

        subscription_qs = Subscription.objects.filter(user=user, course=course)

        if subscription_qs.exists():
            # Удаляем подписку
            subscription_qs.delete()
            message = "Подписка удалена"
        else:
            # Создаём подписку
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})
