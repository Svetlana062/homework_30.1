from rest_framework import serializers

from .models import CustomUser, Payment


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор модели CustomUser для преобразования данных в формат JSON и обратно."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "phone_number", "city", "avatar", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей."""

    user_email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Payment
        fields = [
            "id",
            "user_email",
            "payment_date",
            "course",
            "lesson",
            "amount",
            "payment_method",
        ]


class UserPaymentHistorySerializer(serializers.ModelSerializer):
    """Вывод истории платежей для профиля пользователя."""

    payments = PaymentSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "payments"]

class UserPublicSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра чужих профилей."""

    class Meta:
        model = CustomUser
        fields = ["id", "email", "phone_number", "city", "avatar"]
        # исключаем пароль, фамилию, историю платежей


class UserFullSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования своего профиля."""

    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "phone_number", "city", "avatar", "password"]
