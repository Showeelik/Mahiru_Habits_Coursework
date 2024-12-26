from django.urls import path
from .views import HabitViewSet

urlpatterns = [
    path('habits/', HabitViewSet.as_view({'get': 'list', 'post': 'create'}), name='habit-list'),
]