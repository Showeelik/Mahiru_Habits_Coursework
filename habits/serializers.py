from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = (
            'id', 
            'user',
            'action',
            'place', 
            'time',
            'is_pleasant',
            'linked_habit',
            'reward',
            'period',
            'duration',
            'is_public'
        )