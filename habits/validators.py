from django.core.exceptions import ValidationError

def validate_habit_fields(instance):
    # Время на выполнение должно быть <= 120 секунд
    if instance.duration > 120:
        raise ValidationError("Время выполнения привычки не может быть больше 120 секунд.")

    # Периодичность не может быть реже 1 раза в 7 дней
    if instance.period > 7:
        raise ValidationError("Привычку нельзя выполнять реже, чем раз в неделю.")

    # Одновременное заполнение "связанной привычки" и "вознаграждения"
    if instance.reward and instance.linked_habit:
        raise ValidationError("Нельзя указать одновременно и вознаграждение, и связанную привычку.")

    # Приятная привычка не может иметь ни "вознаграждения", ни "связанной привычки"
    if instance.is_pleasant and (instance.reward or instance.linked_habit):
        raise ValidationError("Приятная привычка не может иметь вознаграждения или связанную привычку.")
