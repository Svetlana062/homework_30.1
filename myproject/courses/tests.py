from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser

from .models import Course, Lesson


class LessonAPITests(APITestCase):
    def setUp(self):
        # Создаем двух пользователей
        self.user1 = CustomUser.objects.create_user(
            email="user1@example.com", username="user1", password="pass1234"
        )
        self.user2 = CustomUser.objects.create_user(
            email="user2@example.com", username="user2", password="pass5678"
        )

        # Создаем изображения для уроков
        self.image1 = SimpleUploadedFile(
            name="image1.jpg",
            content=b"file_content",  # Можно оставить пустым или добавить реальные байты изображения
            content_type="image/jpeg",
        )
        self.image2 = SimpleUploadedFile(
            name="image2.jpg", content=b"file_content", content_type="image/jpeg"
        )

        # Создаем курс
        self.course1 = Course.objects.create(
            title="Course 1",
            description="Description",
            owner=self.user1,
        )

        # Создаем уроки
        self.lesson1 = Lesson.objects.create(
            title="Lesson 1",
            description="Content 1",
            course=self.course1,
            preview_image=self.image1,
            video_link="https://www.youtube.com/watch?v=r_C22jf81gg",
            owner=self.user1,
        )
        self.lesson2 = Lesson.objects.create(
            title="Lesson 2",
            description="Content 2",
            course=self.course1,
            preview_image=self.image2,
            video_link="https://www.youtube.com/watch?v=M6n0Kl_qg3Q",
            owner=self.user2,
        )

        # URL для списка уроков
        self.lesson_list_url = reverse(
            "lesson-list"
        )  # предполагается, что роутер использует basename='lesson'

    def authenticate(self, user):
        # Аутентификация пользователя (например, через токен или сессию)
        self.client.force_authenticate(user=user)

    def test_list_lessons_unauthenticated(self):
        # Проверка получения списка без авторизации (должно работать, если AllowAny)
        response = self.client.get(self.lesson_list_url)
        print("Status code:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что возвращается список уроков
        self.assertEqual(len(response.data), Lesson.objects.count())

    def test_create_lesson_authenticated(self):
        self.authenticate(self.user1)

        # Создаем файл для загрузки
        image = SimpleUploadedFile(
            name="test.jpg", content=b"file_content", content_type="image/jpeg"
        )

        data = {
            "title": "New Lesson",
            "description": "New Content",
            "course": self.course1.id,
            "preview_image": image,
            "video_link": "https://www.youtube.com/watch?v=w-ITLbRfhnA",
        }
        response = self.client.post(self.lesson_list_url, data, format="multipart")

        print("Status code:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверяем, что урок создан и владелец — текущий пользователь
        lesson_id = response.data["id"]
        lesson = Lesson.objects.get(id=lesson_id)
        self.assertEqual(lesson.owner, self.user1)

    def test_create_lesson_unauthenticated(self):
        data = {
            "title": "Unauthorized Lesson",
            "description": "No auth",
            "course": self.course1.id,
            "preview_image": SimpleUploadedFile(
                name="test.jpg", content=b"file_content", content_type="image/jpeg"
            ),
            "video_link": "https://www.youtube.com/watch?v=somevideo",
        }
        response = self.client.post(self.lesson_list_url, data, format="multipart")
        print("Status code:", response.status_code)
        print("Response data:", response.data)
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    def test_retrieve_lesson_detail(self):
        url = reverse("lesson-detail", args=[self.lesson1.id])
        response = self.client.get(url)
        print("Status code:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверка содержимого ответа (название урока)
        self.assertEqual(response.data["title"], self.lesson1.title)

    def test_update_lesson_owner(self):
        url = reverse("lesson-detail", args=[self.lesson1.id])

        # Аутентификация владельца урока
        self.authenticate(self.user1)

        new_data = {"title": "Updated Title"}

        response = self.client.put(url, new_data)
        print("Status code:", response.status_code)
        print("Response data:", response.data)
        # У владельца должно получиться обновить
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем изменение в базе
        self.lesson1.refresh_from_db()
        print("Updated title:", self.lesson1.title)
        self.assertEqual(self.lesson1.title, "Updated Title")

    def test_update_lesson_not_owner_forbidden(self):
        url = reverse("lesson-detail", args=[self.lesson1.id])

        # Аутентификация другого пользователя — обновление должно быть запрещено
        self.authenticate(self.user2)

        new_data = {"title": "Hacked Title"}

        response = self.client.put(url, new_data)
        print("Status code:", response.status_code)
        print("Response data:", response.data)
        # Ожидаем Forbidden (403) или Unauthorized (401)
        self.assertIn(
            response.status_code,
            [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED],
        )

    def test_partial_update_lesson_owner(self):
        url = reverse("lesson-detail", args=[self.lesson2.id])

        # Аутентификация владельца урока
        self.authenticate(self.user2)

        patch_data = {"content": "Updated Content"}

        response = self.client.patch(url, patch_data)
        print("Status code:", response.status_code)
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка изменения в базе
        self.lesson2.refresh_from_db()
        print("Updated description:", self.lesson2.description)
        self.assertEqual(self.lesson2.description, "Updated Content")

    def test_delete_lesson_owner(self):
        url = reverse("lesson-detail", args=[self.lesson2.id])

        # Аутентификация владельца урока (user2 — владелец lesson2)
        self.authenticate(self.user2)

        response = self.client.delete(url)
        print("Status code:", response.status_code)
        print("Response data:", response.data)
        # Удаление должно быть успешным (204 No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Урок должен исчезнуть из базы
        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(id=self.lesson2.id)

    def test_delete_lesson_not_owner_forbidden(self):
        url = reverse("lesson-detail", args=[self.lesson1.id])

        # Аутентификация другого пользователя — удаление запрещено
        self.authenticate(self.user2)

        response = self.client.delete(url)

        print("Status code:", response.status_code)
        print("Response data:", response.data)
        # Ожидаем Forbidden или Unauthorized
        self.assertIn(
            response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]
        )
