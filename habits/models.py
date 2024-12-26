from django.db import models
from django.contrib.auth import get_user_model

from .validators import validate_habit_fields

User = get_user_model()

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits", verbose_name="Создатель")
    action = models.CharField(max_length=255, verbose_name="Действие")
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    linked_habit = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL,
        limit_choices_to={'is_pleasant': True},
        verbose_name="Связанная привычка"
    )
    reward = models.CharField(max_length=255, blank=True, verbose_name="Вознаграждение")
    period = models.PositiveSmallIntegerField(default=1, verbose_name="Периодичность (в днях)")
    duration = models.PositiveIntegerField(verbose_name="Время на выполнение (в секундах)")
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return self.action
    
    def save(self, *args, **kwargs):
        validate_habit_fields(self)
        super().save(*args, **kwargs)
