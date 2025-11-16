from django.shortcuts import render
from tasks.models import Task
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .serializers import TaskSerializer

# from django.http import HttpResponse



def homepage(request):
    # return HttpResponse ("Welcome to Task Manager! ")
    return render(request, 'home.html')

def about(request):
    # return HttpResponse("My About page.")
    return render(request, 'about.html')


def tasks_list(request):
    # Загружаем задачи и связанные подзадачи за один запрос (оптимизация)
    #  prefetch_related('subtasks') — предзагружает подзадачи, чтобы избежать множества SQL-запросов.
    tasks = Task.objects.prefetch_related('subtasks').all().order_by('-created_at')
    return render(request, 'tasks/tasks_list.html', {'tasks': tasks})

# Префикс api_ помогает отличать API-представления от обычных (для HTML-страниц).

@api_view(['POST'])
def api_create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_task_list(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TaskSerializer(task)
    return Response(serializer.data)

@api_view(['GET'])
def api_task_stats(request):
    total = Task.objects.count()
    status_counts = {}
    for choice in Task._meta.get_field('status').choices:
        key = choice[0]
        count = Task.objects.filter(status=key).count()
        status_counts[key] = count

    overdue = Task.objects.filter(deadline__lt=timezone.now()).count()

    return Response({
        'total_tasks': total,
        'tasks_by_status': status_counts,
        'overdue_tasks': overdue
    })