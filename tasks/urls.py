from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import api_views

# DRF router CategoryViewSet
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    # HTML
    path('', views.tasks_list, name='tasks_list'),

    # API TASKS
    path('api/tasks/', views.TaskListCreateView.as_view(), name='task-list-create'),
    path('api/tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),

    # API SUBTASKS
    path('api/subtasks/', views.SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('api/subtasks/<int:pk>/', views.SubTaskDetailView.as_view(), name='subtask-detail'),

    # API STATS
    path('api/stats/', api_views.task_stats, name='task_stats'),

    # API router
    path('api/', include(router.urls)),
]
