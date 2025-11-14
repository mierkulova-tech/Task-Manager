# python queries.py

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


from datetime import timedelta
from django.utils import timezone
from tasks.models import Task, SubTask


# Create a Task
task = Task.objects.create(
    title="Prepare presentation 1",
    description="Prepare materials and slides for the presentation 1",
    status="New",
    deadline=timezone.now() + timedelta(days=3)
)
print(f"Task '{task.title}' is born! Deadline at {task.deadline}")

# Create SubTasks for the Task
subtask1 = SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation 1",
    status="New",
    task=task, # Link to the parent task
    deadline=timezone.now() + timedelta(days=2)  # Deadline in 2 days
)
print(f"SubTask '{subtask1.title}' ready to collect info!")

subtask2 = SubTask.objects.create(
    title="Create slides",
    description="Create presentation slides",
    status="New",
    task=task, # Link to the parent task
    deadline=timezone.now() + timedelta(days=1) # Deadline in 1 day
)
print(f"SubTask '{subtask2.title}' slides on the way!")

# Tasks with status "New"
new_tasks = Task.objects.filter(status="New")
print("Tasks with status 'New'.")
for t in new_tasks:
    print(f"Task {t.title} — Status: {t.status} — Deadline: {t.deadline}")

# SubTasks with status "Done" but deadline passed
overdue_done_subtasks = SubTask.objects.filter(
    status="Done",
    deadline__lt=timezone.now()
)
print("SubTasks done but overdue.")

# Change status of "Prepare presentation" to "In progress"
task_to_update = Task.objects.get(title="Prepare presentation 1")
task_to_update.status = "In progress"
task_to_update.save()

# Change deadline of "Gather information" to two days ago
subtask_to_update = SubTask.objects.get(title="Gather information")
subtask_to_update.deadline = timezone.now() - timedelta(days=2)
subtask_to_update.save()

# Update description of "Create slides"
subtask_to_update = SubTask.objects.get(title="Create slides")
subtask_to_update.description = "Create and format presentation slides"
subtask_to_update.save()

# Delete "Prepare presentation" and all its SubTasks
task_to_delete = Task.objects.get(title="Prepare presentation 1")
task_to_delete.delete()
