from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from habits.models import Habit
from .tasks import send_habit_reminder
from .telegram import send_telegram_message

User = get_user_model()
class TelegramNotificationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password",
            telegram_id="123456789"
        )
        
        self.habit = Habit.objects.create(
            user=self.user,
            action="Тест",
            place="Дом",
            time="12:00:00",
            duration=60,
            period=1
        )

    @patch('notifications.telegram.requests.post')
    def test_send_telegram_message(self, mock_post):
        """Тест отправки сообщения в Telegram"""
        # Подготовка теста
        chat_id = 123456789
        message = 'Тестовое сообщение'
        
        # Вызов тестируемой функции
        send_telegram_message(chat_id, message)
        
        # Проверка вызова мок-объекта
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertIn('chat_id', kwargs['data'])
        self.assertEqual(kwargs['data']['chat_id'], chat_id)
        self.assertEqual(kwargs['data']['text'], message)

    @patch('notifications.telegram.send_telegram_message')
    def test_habit_reminder_task(self, mock_send_message):
        """Тест задачи напоминания о привычке"""
        # Настройка мока
        mock_send_message.return_value = True
        
        # Вызов тестируемой функции
        result = send_habit_reminder(self.user.id, self.habit.id)
        
        # Проверка вызова мок-объекта
        mock_send_message.assert_called_once()
        args, kwargs = mock_send_message.call_args
        self.assertEqual(args[0], self.user.telegram_id)
        self.assertIn(self.habit.action, args[1])

    @patch('notifications.telegram.requests.post')
    def test_telegram_api_error_handling(self, mock_post):
        mock_post.side_effect = Exception("Telegram API Error")
        try:
            send_telegram_message(123456789, "test message")
        except Exception:
            self.fail("Функция не должна пробрасывать исключение")

    def test_invalid_habit_reminder(self):
        """Тест напоминания для несуществующей привычки"""
        habit_id = 99999
        result = send_habit_reminder(self.user.id, habit_id)
        self.assertIsNone(result)

    def test_invalid_user_habit_reminder(self):
        """Тест напоминания для несуществующего пользователя"""
        user_id = 99999
        result = send_habit_reminder(user_id, self.habit.id)
        self.assertIsNone(result)