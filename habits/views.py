from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Habit
from .permissions import IsOwnerOrReadOnly
from .serializers import HabitSerializer


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Habit.objects.filter(Q(user=self.request.user) | Q(is_public=True))
        return Habit.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicHabitListView(ListAPIView):
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class UserHabitListView(ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
