# tasks/urls.py
from django.urls import path
from . import views  # ← импортируем из нового views.py
from .api import api_views  # оставляем stats

urlpatterns = [
    # HTML-страницы (оставляем как есть)
    path('', views.tasks_list, name='tasks_list'),

    # API — задачи (новые Generic Views)
    path('api/tasks/', views.TaskListCreateView.as_view(), name='task-list-create'),
    path('api/tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),

    # API — подзадачи (новые Generic Views)
    path('api/subtasks/', views.SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('api/subtasks/<int:pk>/', views.SubTaskDetailView.as_view(), name='subtask-detail'),

    # Статистика — оставляем как есть
    path('api/stats/', api_views.task_stats, name='task_stats'),
]