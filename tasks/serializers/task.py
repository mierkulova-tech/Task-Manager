from rest_framework import serializers
from tasks.models import Task
from .subtask import SubTaskSerializer


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'subtasks']
        read_only_fields = ['id', 'created_at']