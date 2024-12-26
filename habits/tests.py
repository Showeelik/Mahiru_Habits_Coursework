from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from habits.models import Habit

User = get_user_model()

class HabitTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="password")
        self.client.force_authenticate(user=self.user)
        Habit.objects.create(user=self.user, action="Прогулка", place="Парк", time="18:00:00", is_public=True)

    def test_get_habits(self):
        response = self.client.get("/api/habits/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_habit(self):
        data = {"action": "Зарядка", "place": "Дом", "time": "08:00:00"}
        response = self.client.post("/api/habits/", data)
        self.assertEqual(response.status_code, 201)
