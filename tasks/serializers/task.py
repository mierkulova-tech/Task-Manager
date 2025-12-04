from django.utils import timezone
from rest_framework import serializers

from .subtask import SubTaskSerializer
from ..models import Task


class TaskDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving task details.
    Includes nested subtasks and aggregated information
    such as total subtasks and completed subtasks count.
    """

    subtasks = SubTaskSerializer(many=True, read_only=True)
    subtasks_count = serializers.SerializerMethodField()
    completed_subtasks_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        read_only_fields = ['id', 'created_at']
        fields = [
            'id', 'title', 'description', 'status', 'deadline',
            'created_at', 'updated_at', 'subtasks', 'subtasks_count',
            'completed_subtasks_count'
        ]

    def get_subtasks_count(self, obj):
        """Return the total number of subtasks for this task."""
        return obj.subtasks.count()

    def get_completed_subtasks_count(self, obj):
        """Return the number of completed subtasks (status = DONE)."""
        return obj.subtasks.filter(status='Done').count()


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new task.
    Validates that the deadline is not in the past
    and prevents creating a task directly with status 'Done'.
    """

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'categories']
        read_only_fields = ['id']

    def validate_deadline(self, value):
        """
        Ensure the deadline is not earlier than the current time.
        """
        now = timezone.now()

        if value < now:
            raise serializers.ValidationError(
                f"Deadline cannot be in the past. "
                f"Received: {value.strftime('%d.%m.%Y %H:%M')}, "
                f"Current time: {now.strftime('%d.%m.%Y %H:%M')}"
            )
        return value

    def validate(self, attrs):
        """
        Prevent creation of a task with status 'Done'.
        The task must first be created and only then updated.
        """
        status = attrs.get('status')
        if status == 'Done':
            raise serializers.ValidationError(
                "A task cannot be created with status 'Done'. "
                "Create the task first, then update its status."
            )
        return attrs