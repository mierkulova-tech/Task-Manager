from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone



# Deadline validator: ensures the deadline is not in the past
def validate_deadline(value):
    if value < timezone.now():
        raise ValidationError("Deadline cannot be in the past.")

class Category(models.Model):
    """Model representing a category for tasks."""

    name = models.CharField(max_length=100, unique=True) # Category name, must be unique

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = 'task_manager_category'


class Task(models.Model):
    """Model representing a task."""

    # Task status options
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Pending', 'Pending'),
        ('Blocked', 'Blocked'),
        ('Done', 'Done'),
    ]

    title = models.CharField(max_length=200, unique=True)  # Task title, unique
    description = models.TextField(blank=True) # Optional task description
    categories = models.ManyToManyField(Category, related_name="tasks") # Task can belong to multiple categories
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New') # Current task status
    deadline = models.DateTimeField(validators=[validate_deadline]) # Deadline date and time,  validator added
    created_at = models.DateTimeField(auto_now_add=True) # Creation timestamp

    class Meta:
        # Enforce uniqueness by combination of title and deadline
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'deadline'],
                name='unique_task_title_per_deadline'
            )
        ]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        db_table = 'task_manager_task'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class SubTask(models.Model):
    """Model representing a subtask of a parent task."""

    # Subtask status options
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Pending', 'Pending'),
        ('Blocked', 'Blocked'),
        ('Done', 'Done'),
    ]


    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="subtasks"

    ) # Linked parent task
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='New'

    ) # Current subtask status
    deadline = models.DateTimeField(validators=[validate_deadline]) # Deadline date and time,  validator added
    created_at = models.DateTimeField(auto_now_add=True) # Creation timestamp

    def __str__(self):
        return f"{self.title} (subtask of {self.task.title})"

    class Meta:
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"
        db_table = 'task_manager_subtask'
        ordering = ['-created_at'] # Sort newest first
