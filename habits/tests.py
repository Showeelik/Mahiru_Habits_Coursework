from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from habits.models import Habit
from habits.validators import validate_habit_fields

User = get_user_model()

class HabitTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", 
            email="test@example.com", 
            password="password"
        )
        self.client.force_authenticate(user=self.user)
        
        self.habit_data = {
            "action": "Прогулка",
            "place": "Парк",
            "time": "18:00:00",
            "duration": 60,
            "period": 1,
            "is_public": True,
            "reward": "Отдых",
            "is_pleasant": False
        }
        
        # Для прямого создания в БД добавляем пользователя
        self.habit = Habit.objects.create(
            user=self.user,
            **self.habit_data
        )


    def test_create_habit(self):
        """Тест создания привычки"""
        response = self.client.post("/api/habits/", self.habit_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверяем создание новой привычки
        self.assertEqual(Habit.objects.count(), 2)
        
        # Проверяем данные созданной привычки
        new_habit = Habit.objects.latest('id')
        self.assertEqual(new_habit.user, self.user)
        self.assertEqual(new_habit.action, self.habit_data['action'])
        self.assertEqual(new_habit.place, self.habit_data['place'])

    def test_get_habits_list(self):
        """Тест получения списка привычек"""
        response = self.client.get("/api/habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_public_habits(self):
        """Тест получения публичных привычек"""
        response = self.client.get("/api/habits/public/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_update_habit(self):
        """Тест обновления привычки"""
        data = {"action": "Вечерняя прогулка"}
        response = self.client.patch(f"/api/habits/{self.habit.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Вечерняя прогулка")

    def test_delete_habit(self):
        """Тест удаления привычки"""
        response = self.client.delete(f"/api/habits/{self.habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_pagination(self):
        """Тест пагинации и сортировки"""
        # Создаем дополнительные привычки
        for i in range(6):
            Habit.objects.create(
                user=self.user,
                action=f"Привычка {i}",
                place="Дом",
                time="12:00:00",
                duration=60,
                period=1
            )

        response = self.client.get("/api/habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        
        # Проверяем сортировку
        first_id = response.data['results'][0]['id']
        second_id = response.data['results'][1]['id']
        self.assertTrue(first_id > second_id)

    def test_habit_permissions(self):
        """Тест прав доступа к привычкам"""
        # Создаем второго пользователя
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="password"
        )
        self.client.force_authenticate(user=other_user)

        # Попытка изменить чужую привычку
        response = self.client.patch(f"/api/habits/{self.habit.id}/", {"action": "Changed"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Попытка удалить чужую привычку
        response = self.client.delete(f"/api/habits/{self.habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_pagination(self):
        """Тест пагинации"""
        # Создаем дополнительные привычки
        for i in range(7):
            Habit.objects.create(
                user=self.user,
                action=f"Привычка {i}",
                place="Дом",
                time="12:00:00",
                duration=60,
                period=1
            )
        
        response = self.client.get("/api/habits/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)  # Проверяем размер страницы
        self.assertIsNotNone(response.data['next'])  # Проверяем наличие следующей страницы