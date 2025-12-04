from django.shortcuts import render
from rest_framework import generics, filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task, SubTask, Category
from .serializers import TaskDetailSerializer, SubTaskSerializer, SubTaskCreateSerializer
from .serializers.category import CategorySerializer


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

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_destroy(self, instance):
        instance.delete()

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        category = self.get_object()
        count = category.tasks.count()

        return Response({
            'category': category.name,
            'category_id': category.id,
            'tasks_count': count
        })