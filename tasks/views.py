from django.shortcuts import render
from tasks.models import Task
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .serializers import TaskSerializer, SubTaskSerializer
def homepage(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


def tasks_list(request):
    tasks = Task.objects.prefetch_related('subtasks').all().order_by('-created_at')
    return render(request, 'tasks/tasks_list.html', {'tasks': tasks})



