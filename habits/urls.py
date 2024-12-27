from django.urls import path
from .views import HabitViewSet, PublicHabitListView, UserHabitListView

urlpatterns = [
    path('habits/', UserHabitListView.as_view({'get': 'list', 'post': 'create'}), name='habit-list'),
    path('habits/public/', PublicHabitListView.as_view(), name='public-habit-list'),
    path('habits/<int:pk>/', HabitViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='habit-detail'),
]