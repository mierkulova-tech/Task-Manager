from django.shortcuts import render
from rest_framework import generics, filters
from .models import Task, SubTask
from .serializers import TaskDetailSerializer, SubTaskSerializer, SubTaskCreateSerializer

def homepage(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


def tasks_list(request):
    tasks = Task.objects.prefetch_related('subtasks').all().order_by('-created_at')
    return render(request, 'tasks/tasks_list.html', {'tasks': tasks})

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.prefetch_related('categories', 'subtasks')
    serializer_class = TaskDetailSerializer
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.prefetch_related('categories', 'subtasks')
    serializer_class = TaskDetailSerializer


class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.select_related('task')
    serializer_class = SubTaskSerializer
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer


class SubTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.select_related('task')
    serializer_class = SubTaskSerializer