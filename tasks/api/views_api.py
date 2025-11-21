from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tasks.models import Task
from tasks.serializers import TaskSerializer


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
    for value, label in Task.STATUS_CHOICES:
        status_counts[value] = Task.objects.filter(status=value).count()

    overdue = Task.objects.filter(
        deadline__lt=timezone.now(),
        status__in=['New', 'In progress', 'Pending', 'Blocked']
    ).count()

    return Response({
        'total_tasks': total,
        'tasks_by_status': status_counts,
        'overdue_tasks': overdue
    })