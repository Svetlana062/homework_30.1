import django_filters
import stripe
from django.conf import settings
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser, Payment
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CustomUserSerializer,
    PaymentSerializer,
    UserFullSerializer,
    UserPublicSerializer,
)

# Инициализируем Stripe с нашим API ключом
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name):
    """Создание продукта в Stripe."""
    product = stripe.Product.create(name=name)
    return product


def create_stripe_price(product_id, amount):
    """Создание цены для продукта в Stripe (принимает сумму в копейках)."""
    price = stripe.Price.create(
        unit_amount=amount,
        currency="rub",
        product=product_id,
    )
    return price


def create_checkout_session(price_id, success_url, cancel_url):
    """Создание сессии оформления заказа в Stripe."""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session


class CustomUserViewSet(viewsets.ModelViewSet):
    """ViewSet для модели CustomUser."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer  # сериализатор для преобразования данных

    def get_permissions(self):
        if self.action == "create":
            # регистрация — открыта всем
            permission_classes = []
        elif self.action in ["retrieve", "update", "partial_update"]:
            # просмотр и редактирование своих данных
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            # остальные действия (например, list, destroy) — только админ
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class UserProfileView(generics.RetrieveAPIView):
    """View для профиля пользователя."""

    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        # Используем сериализатор для просмотра своего профиля
        if self.request.user.is_authenticated:
            if self.request.method in ["PUT", "PATCH"]:
                return UserFullSerializer
            # если запрашивается свой профиль
            if self.get_object() == self.request.user:
                return UserFullSerializer
        # Иначе — публичный сериализатор
        return UserPublicSerializer

    def get_object(self):
        # Получение объекта по pk из URL или текущего пользователя
        pk = self.kwargs.get("pk")
        if pk:
            return super().get_object()
        else:
            # если pk не передан — возвращаем текущего пользователя
            return self.request.user

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            # Только владелец может редактировать
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class PaymentFilter(django_filters.FilterSet):
    """Фильтрация и сортировка для списка платежей."""

    course_id = django_filters.NumberFilter(field_name="course__id")
    lesson_id = django_filters.NumberFilter(field_name="lesson__id")
    payment_method = django_filters.CharFilter(field_name="payment_method")

    class Meta:
        model = Payment
        fields = ["course_id", "lesson_id", "payment_method"]


class PaymentViewSet(viewsets.ModelViewSet):
    """Обновленный ViewSet для платежей."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date"]

    @action(detail=True, methods=["post"])
    def create_stripe_payment(self, request, pk=None):
        payment = self.get_object()

        # Создаем продукт на Stripe (можно делать один раз и сохранять ID)
        product_response = create_stripe_product(
            name=f"Курс: {payment.course.title if payment.course else 'Платеж'}"
        )

        # Создаем цену (учитываем сумму платежа в копейках)
        amount_kopecks = int(payment.amount * 100)
        price_response = create_stripe_price(product_response.id, amount_kopecks)

        # URL-ы для редиректа после оплаты (замените на ваши реальные URL)
        success_url = request.build_absolute_uri(
            "/payment/success/"
        )  # например, ваш фронт или бекенд URL
        cancel_url = request.build_absolute_uri("/payment/cancel/")

        # Создаем сессию оплаты
        session = create_checkout_session(price_response.id, success_url, cancel_url)

        # Сохраняем данные о сессии в модель платежа
        payment.stripe_session_id = session.id
        payment.payment_url = session.url
        payment.payment_status = session.payment_status
        payment.save()

        return Response(
            {
                "checkout_url": session.url,
                "session_id": session.id,
                "payment_status": session.payment_status,
            }
        )


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
