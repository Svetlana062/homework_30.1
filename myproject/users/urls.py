from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, RegisterAPIView



router = DefaultRouter()
router.register(r"", CustomUserViewSet)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("", include(router.urls)),
]
