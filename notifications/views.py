from django.shortcuts import render

from notifications.tasks import send_habit_reminder

# Create your views here.
def perform_update(self, serializer):
    instance = serializer.save()
    send_habit_reminder.delay(self.request.user.id, instance.id)
