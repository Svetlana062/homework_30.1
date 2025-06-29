from rest_framework import viewsets, generics
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAdminUser

from ..courses.serializers import UserPaymentHistorySerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    """ViewSet для модели CustomUser."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer  # сериализатор для преобразования данных
    permission_classes = [IsAdminUser]  # права доступа только у администратора


class UserProfileView(generics.RetrieveAPIView):
    """View для профиля пользователя."""
    queryset = CustomUser.objects.all()
    serializer_class = UserPaymentHistorySerializer

    def get_object(self):
        return self.request.user
