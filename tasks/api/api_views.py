from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from tasks.models import Task, SubTask
from tasks.serializers import TaskDetailSerializer, SubTaskSerializer


@api_view(['POST'])
def create_task(request):
    serializer = TaskDetailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()
    serializer = TaskDetailSerializer(tasks, many=True)
    return Response(serializer.data, status= status.HTTP_200_OK)

@api_view(['GET'])
def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TaskDetailSerializer(task)
    return Response(data=serializer.data, status= status.HTTP_200_OK)

@api_view(['GET'])
def task_stats(request):
    total = Task.objects.count()
    status_counts = {}
    # _ переменная которая не используется, мусорный атрибут
    for value, _ in Task.STATUS_CHOICES:
        status_counts[value] = Task.objects.filter(status=value).count()

    overdue = (Task.objects.filter(
        deadline__lt=timezone.now(),
    ).exclude(status='Done')
    .count())

    return Response(
        data={
        'total_tasks': total,
        'tasks_by_status': status_counts,
        'overdue_tasks': overdue
    },
    status=status.HTTP_200_OK
    )


class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all().select_related('task')
        task_id = request.query_params.get('task_id')
        if task_id:
            subtasks = subtasks.filter(task_id=task_id)


        status_filter = request.query_params.get('status')
        if status_filter:
            subtasks = subtasks.filter(status=status_filter)


        serializer = SubTaskSerializer(subtasks, many=True)

        return Response({
            'count': subtasks.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubTaskSerializer(data=request.data)

        if serializer.is_valid():
            subtask = serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        return get_object_or_404(SubTask.objects.select_related('task'), pk=pk)

    def get(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskSerializer(subtask, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskSerializer(subtask, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        subtask.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)