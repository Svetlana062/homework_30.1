import django_filters
from rest_framework import viewsets, generics
from .models import CustomUser, Payment
from .serializers import CustomUserSerializer, UserPaymentHistorySerializer, PaymentSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework import filters


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


class PaymentFilter(django_filters.FilterSet):
    """Фильтрация и сортировка для списка платежей."""
    course_id = django_filters.NumberFilter(field_name='course__id')
    lesson_id = django_filters.NumberFilter(field_name='lesson__id')
    payment_method = django_filters.CharFilter(field_name='payment_method')

    class Meta:
        model = Payment
        fields = ['course_id', 'lesson_id', 'payment_method']


class PaymentViewSet(viewsets.ModelViewSet):
    """Обновленный ViewSet для платежей."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
