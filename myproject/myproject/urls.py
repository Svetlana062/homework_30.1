from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from users.views import RegisterAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),  # маршруты для приложения users
    path("courses/", include("courses.urls")),  # маршруты для приложения courses
]

urlpatterns += [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register/", RegisterAPIView.as_view(), name="register"),
]

# Обслуживание медиафайлов при DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
