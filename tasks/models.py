from django.db import models

# Статусы — удобно вынести в переменную
TASK_STATUS_CHOICES = [
    ('New', 'New'),
    ('In progress', 'In progress'),
    ('Pending', 'Pending'),
    ('Blocked', 'Blocked'),
    ('Done', 'Done'),
]

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name="tasks")
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='New')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Уникальность: title + deadline (дата без времени не подойдёт — используем день)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'deadline'],
                name='unique_task_title_per_deadline'
            )
        ]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title


class SubTask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='New')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (subtask of {self.task.title})"

    class Meta:
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"
