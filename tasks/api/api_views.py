from django.utils import timezone
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models.functions import ExtractIsoWeekDay
from tasks.models import Task, SubTask
from tasks.pagination import SubTaskPagination
from tasks.serializers import TaskDetailSerializer, SubTaskSerializer, SubTaskCreateSerializer


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

class TaskByWeekdayView(APIView):
    WEEKDAYS = {
        'monday': 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6,
        'sunday': 7
    }

    def get(self, request):
        queryset = Task.objects.prefetch_related('categories')

        day_param = request.query_params.get('day')
        if day_param:
            day_param = day_param.lower().strip()
            if day_param not in self.WEEKDAYS:
                return Response(
                    {
                        'error': f'Invalid day: {day_param}',
                        'valid_days': list(self.WEEKDAYS.keys())
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            weekday_number = self.WEEKDAYS[day_param]
            queryset = queryset.annotate(
                iso_weekday=ExtractIsoWeekDay('deadline')
            ).filter(iso_weekday=weekday_number)

        serializer = TaskDetailSerializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'day_filter': day_param or 'all',
            'results': serializer.data
        }, status=status.HTTP_200_OK)

class SubTaskListCreateView(APIView):
    def get(self, request):
        queryset = SubTask.objects.all().order_by('-created_at')

        task_title = request.query_params.get('task_title')
        if task_title:
            queryset = queryset.filter(task__title__icontains=task_title)

        status_param = request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        if status_param:
            valid_statuses = [choice[0] for choice in SubTask.STATUS_CHOICES]
            if status_param not in valid_statuses:
                return Response(
                    {
                        'error': f'Invalid status. Valid: {valid_statuses}'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            queryset = queryset.filter(status=status_param)

        paginator = SubTaskPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = SubTaskSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)