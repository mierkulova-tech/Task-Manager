from django.urls import path
from . import views
from .api import views_api



#API HTML
urlpatterns = [
    path('', views.tasks_list, name='tasks_list'),


#API URL

    path('create_task', views_api.api_create_task, name='create_task'),
    path('list/', views_api.api_task_list, name='list_tasks'),
    path('<int:task_id>/', views_api.api_task_detail, name='get_task'),
    path('stats/', views_api.api_task_stats, name='task_stats'),
]