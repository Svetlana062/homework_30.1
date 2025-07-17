from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, PaymentViewSet, RegisterAPIView

router = DefaultRouter()
router.register(r"", CustomUserViewSet, basename="customuserviewset")
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("", include(router.urls)),
]
