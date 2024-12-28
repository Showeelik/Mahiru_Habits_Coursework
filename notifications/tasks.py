from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

from habits.models import Habit
from notifications.telegram import send_telegram_message

User = get_user_model()

@shared_task
def send_habit_reminder(user_id, habit_id):
    try:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

        try:
            habit = Habit.objects.get(pk=habit_id)
        except Habit.DoesNotExist:
            return None
            
        if not user.telegram_id:
            return "Telegram chat ID не установлен"
            
        message = f"Напоминание: {habit.action} в {habit.place} в {habit.time}"
        return send_telegram_message(user.telegram_id, message)
        
    except Exception as e:
        return f"Ошибка: {str(e)}"

@shared_task
def check_habits():
    """
    Проверяет привычки и отправляет напоминания
    """
    current_time = timezone.now()
    habits = Habit.objects.filter(
        time=current_time.time(),
        is_active=True
    )
    
    for habit in habits:
        send_habit_reminder.delay(habit.user.id, habit.id)