from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор модели CustomUser для преобразования данных в формат JSON и обратно."""
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone_number', 'city', 'avatar']
