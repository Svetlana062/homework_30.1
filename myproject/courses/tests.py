from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Course, Lesson, Subscription
from myproject.users.models import CustomUser



class CoursesTests(TestCase):
    def setUp(self):
        # Создаем группы: пользователь, модератор
        self.moderator_group = Group.objects.create(name='Модераторы')
        self.regular_group = Group.objects.create(name='Пользователи')

        # Создаем пользователей
        self.owner_user = CustomUser.objects.create_user(username='owner', password='pass123')
        self.owner_user.groups.add(self.regular_group)

        self.moderator_user = CustomUser.objects.create_user(username='moderator', password='pass123', email='moderator@example.com')
        self.moderator_user.groups.add(self.moderator_group)

        self.other_user = CustomUser.objects.create_user(username='other', password='pass123')

        # Создаем курс
        self.course = Course.objects.create(
            title='Test Course',
            preview_image='path/to/image.jpg',
            description='Test description',
            owner=self.owner_user
        )

        # Создаем урок внутри курса
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Test Lesson',
            description='Lesson description',
            preview_image='path/to/lesson_image.jpg',
            video_link='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            owner=self.owner_user
        )

        # Инициализация клиента
        self.client = APIClient()

    def test_create_lesson_as_owner(self):
        """Проверка создания урока авторизованным владельцем курса"""
        self.client.force_authenticate(user=self.owner_user)
        data = {
            'course': self.course.id,
            'title': 'New Lesson',
            'description': 'New lesson description',
            'preview_image': 'path/to/new_image.jpg',
            'video_link': 'https://www.youtube.com/watch?v=abcdefg'
        }
        response = self.client.post('/lessons/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'New Lesson')

    def test_create_lesson_unauthenticated(self):
        """Проверка, что неавторизованный пользователь не может создать урок"""
        response = self.client.post('/lessons/', {})
        self.assertEqual(response.status_code, 403)  # или 401 в зависимости от настроек

    def test_update_lesson_as_owner(self):
        """Редактирование урока владельцем"""
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.patch(f'/lessons/{self.lesson.id}/', {'title': 'Updated Title'})
        self.assertEqual(response.status_code, 200)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Title')

    def test_delete_lesson_as_moderator(self):
        """Удаление урока модератором (если разрешено)"""
        # Предположим, что модератор имеет права на удаление через IsModeratorOrReadOnly
        # В данном случае нужно проверить разрешения.

        # Для этого можно создать отдельный viewset с нужными разрешениями.

        # Для примера:
        self.client.force_authenticate(user=self.moderator_user)
        response = self.client.delete(f'/lessons/{self.lesson.id}/')

        # Предполагается, что модератор может удалять:
        self.assertIn(response.status_code, [204, 200])

    def test_subscription_toggle(self):
        """Тестировать подписку/отписку на курс"""

        url = '/subscription/'

        # Подписка пользователем-авторизованным
        self.client.force_authenticate(user=self.other_user)

        # Подписка (POST или PUT в зависимости от реализации)

        response = self.client.post(url, {'course_id': self.course.id})

        # Проверяем успешность подписки
        self.assertEqual(response.status_code, 200)

        # Проверяем наличие подписки в базе
        exists = Subscription.objects.filter(user=self.other_user, course=self.course).exists()
        self.assertTrue(exists)

    def test_unsubscribe(self):
        """Отписка от курса"""

        # Предположим, что вызов same endpoint с тем же методом отключает подписку

        # Сначала подписываемся вручную

        Subscription.objects.create(user=self.other_user, course=self.course)

        # Аутентификация
        self.client.force_authenticate(user=self.other_user)

        response = self.client.delete('/subscription/', data={'course_id': self.course.id})

        # Проверяем успешное удаление подписки
        exists = Subscription.objects.filter(user=self.other_user, course=self.course).exists()
        self.assertFalse(exists)
