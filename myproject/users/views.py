from rest_framework import viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAdminUser

class CustomUserViewSet(viewsets.ModelViewSet):
    """ViewSet для модели CustomUser."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer  # сериализатор для преобразования данных
    permission_classes = [IsAdminUser]  # права доступа только у администратора
