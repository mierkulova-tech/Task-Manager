from django.db import models

# Task status options
TASK_STATUS_CHOICES = [
    ('New', 'New'),
    ('In progress', 'In progress'),
    ('Pending', 'Pending'),
    ('Blocked', 'Blocked'),
    ('Done', 'Done'),
]

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

    title = models.CharField(max_length=200, unique=True)  # Task title, unique
    description = models.TextField(blank=True) # Optional task description
    categories = models.ManyToManyField(Category, related_name="tasks") # Task can belong to multiple categories
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='New') # Current task status
    deadline = models.DateTimeField() # Deadline date and time
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

    def __str__(self):
        return self.title


class SubTask(models.Model):
    """Model representing a subtask of a parent task."""

    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="subtasks"
    ) # Linked parent task
    status = models.CharField(
        max_length=20,
        choices=TASK_STATUS_CHOICES,
        default='New'
    ) # Current subtask status
    deadline = models.DateTimeField() # Deadline date and time
    created_at = models.DateTimeField(auto_now_add=True) # Creation timestamp

    def __str__(self):
        return f"{self.title} (subtask of {self.task.title})"

    class Meta:
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"
        db_table = 'task_manager_subtask'
        ordering = ['-created_at'] # Sort newest first
