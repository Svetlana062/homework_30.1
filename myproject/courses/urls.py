from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, LessonListCreate, LessonRetrieveUpdateDestroy, SubscriptionToggleAPIView

router = DefaultRouter()
router.register(r"courses", CourseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonListCreate.as_view(), name="lesson-list-create"),
    path(
        "lessons/<int:pk>/", LessonRetrieveUpdateDestroy.as_view(), name="lesson-detail"
    ),
    path('subscription/', SubscriptionToggleAPIView.as_view(), name="subscription-toggle"),
]
