from rest_framework import serializers
from .models import CustomUser, Payment


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор модели CustomUser для преобразования данных в формат JSON и обратно."""
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone_number', 'city', 'avatar']


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
