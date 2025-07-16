from django.contrib.auth.models import Group
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, Lesson, Subscription
from django.contrib.auth import get_user_model

User = get_user_model()


class CoursesLessonsSubscriptionsTests(APITestCase):
    def setUp(self):
        # Создаем группы
        self.moderators_group = Group.objects.create(name="Модераторы")

        # Создаем пользователей
        self.owner = User.objects.create_user(
            username="owner", email="owner@example.com", password="pass1234"
        )
        self.moderator = User.objects.create_user(
            username="moderator", email="moderator@example.com", password="pass1234"
        )
        self.moderator.groups.add(self.moderators_group)

        self.other_user = User.objects.create_user(
            username="other", email="other@example.com", password="pass1234"
        )

        # Создаем курс владельцем
        self.course = Course.objects.create(
            title="Test Course",
            preview_image="course_previews/test.jpg",
            description="Test course description",
            owner=self.owner,
        )

        # Создаем урок владельцем
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Test Lesson",
            description="Test lesson description",
            preview_image="lesson_previews/test.jpg",
            video_link="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            owner=self.owner,
        )

    # Тесты CRUD уроков

    def test_owner_can_create_lesson(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("lesson-list")

        image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\
                x00\x00\xff\xff\xff\x21\xf9\x04\x00\x00\x00\x00\x00\x2c\x00\x00\x00\
                x00\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b",
            content_type="image/gif",
        )

        data = {
            "course": self.course.id,
            "title": "New Lesson",
            "description": "New lesson description",
            "preview_image": image,
            "video_link": "https://www.youtube.com/watch?v=3JZ_D3ELwOQ",
        }
        response = self.client.post(
            url, data, format="multipart"
        )  # multipart для файлов
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_other_user_cannot_update_lesson(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse("lesson-detail", kwargs={"pk": self.lesson.id})
        data = {"title": "Hacked Title"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_update_own_lesson(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("lesson-detail", kwargs={"pk": self.lesson.id})
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Title")

    def test_moderator_can_update_any_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("lesson-detail", kwargs={"pk": self.lesson.id})
        data = {"title": "Moderator Updated"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Moderator Updated")

    def test_unauthenticated_user_cannot_create_lesson(self):
        url = reverse("lesson-list")
        data = {
            "course": self.course.id,
            "title": "Unauthorized Lesson",
            "description": "Should fail",
            "preview_image": None,
            "video_link": "https://www.youtube.com/watch?v=3JZ_D3ELwOQ",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_owner_can_delete_own_lesson(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("lesson-detail", kwargs={"pk": self.lesson.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_other_user_cannot_delete_lesson(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse("lesson-detail", kwargs={"pk": self.lesson.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Тесты подписки

    def test_user_can_subscribe_and_unsubscribe(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse("subscription-toggle")
        # Подписаться
        response = self.client.post(url, {"course_id": self.course.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Подписка добавлена", response.data["message"])
        self.assertTrue(
            Subscription.objects.filter(
                user=self.other_user, course=self.course
            ).exists()
        )

        # Отписаться
        response = self.client.post(url, {"course_id": self.course.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Подписка удалена", response.data["message"])
        self.assertFalse(
            Subscription.objects.filter(
                user=self.other_user, course=self.course
            ).exists()
        )

    def test_subscription_without_course_id_returns_400(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse("subscription-toggle")
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_user_cannot_subscribe(self):
        url = reverse("subscription-toggle")
        response = self.client.post(url, {"course_id": self.course.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
