from django.urls import path
from . import views



urlpatterns = [
    path('', views.tasks_list, name='tasks_list'),

    path('create_task', views.create_task, name='create_task'),
    path('list/', views.task_list, name='list_tasks'),
    path('<int:task_id>/', views.task_detail, name='get_task'),
    path('stats/', views.task_stats, name='task_stats'),
]