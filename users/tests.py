from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from users.serializers import UserSerializer
from datetime import timedelta
from django.utils import timezone

class UserModelTests(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        """Тест создания пользователя"""
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertEqual(self.user.username, self.user_data['username'])
        self.assertTrue(self.user.check_password(self.user_data['password']))

    def test_user_str_method(self):
        """Тест строкового представления пользователя"""
        self.assertEqual(str(self.user), self.user_data['email'])

class UserAPITests(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123'
        }
        self.register_url = reverse('register')
        self.token_url = reverse('token_obtain_pair')

    def test_user_registration(self):
        """Тест регистрации пользователя через API"""
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, self.user_data['email'])

    def test_user_login(self):
        """Тест авторизации пользователя"""
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.token_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class UserSerializerTests(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_serializer_with_valid_data(self):
        """Тест сериализатора с валидными данными"""
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_with_invalid_email(self):
        """Тест сериализатора с невалидным email"""
        self.user_data['email'] = 'invalid-email'
        serializer = UserSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

class UserTasksTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )

    def test_deactivate_inactive_users(self):
        """Тест деактивации неактивных пользователей"""
        # Устанавливаем last_login на 31 день назад
        self.user.last_login = timezone.now() - timedelta(days=31)
        self.user.save()

        from users.tasks import deactivate_inactive_users
        deactivate_inactive_users()

        # Обновляем пользователя из БД
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)