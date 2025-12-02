from django.urls import path
from . import views
from .api import api_views

# HTML-страницы
urlpatterns = [
    path('', views.tasks_list, name='tasks_list'),

    # API subtask (class)
    path('api/subtasks/',
         api_views.SubTaskListCreateView.as_view(),
         name='api_subtask_list_create'),

    path('api/subtasks/<int:pk>/',
         api_views.SubTaskDetailUpdateDeleteView.as_view(),
         name='api_subtask_detail'),

    # API (def)
    path('api/create_task/', api_views.create_task, name='create_task'),
    path('api/list/', api_views.task_list, name='list_tasks'),
    path('api/<int:task_id>/', api_views.task_detail, name='get_task'),
    path('api/stats/', api_views.task_stats, name='task_stats'),
]