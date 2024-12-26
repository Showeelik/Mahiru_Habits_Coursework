from celery import shared_task
from .telegram import send_telegram_message

@shared_task
def send_habit_reminder(user_id, habit_id):
    from habits.models import Habit
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    user = User.objects.get(pk=user_id)
    habit = Habit.objects.get(pk=habit_id)
    message = f"Привет, {user.username}! Напоминаем о привычке: {habit.action} в {habit.time} на {habit.place}."
    send_telegram_message(user.telegram_chat_id, message)