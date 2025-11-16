from django.urls import path
from . import views

urlpatterns = [
    # HTML views
    path('', views.tasks_list, name='tasks_list'),

   # API endpoints
    path('api/tasks/create/', views.api_create_task, name='api_create_task'),
    path('api/tasks/', views.api_task_list, name='api_task_list'),
    path('api/tasks/<int:task_id>/', views.api_task_detail, name='api_task_detail'),
    path('api/tasks/stats/', views.api_task_stats, name='api_task_stats'),
]