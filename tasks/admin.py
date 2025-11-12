from django.contrib import admin
from .models import Task, SubTask, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""

    list_display = ['name'] # Show category name in admin list
    search_fields = ['name'] # Enable search by name

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin configuration for Task model."""
    list_display = ['title', 'status', 'deadline', 'created_at'] # Display key fields
    filter_horizontal = ['categories']  ## Widget for ManyToMany selection
    list_filter = ['status', 'created_at', 'deadline'] # Filter sidebar
    search_fields = ['title', 'description'] # Search by title or description

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    """Admin configuration for SubTask model."""

    list_display = ['title', 'task', 'status', 'deadline', 'created_at'] # Display fields
    list_filter = ['status', 'created_at'] # Filters for quick lookup
    search_fields = ['title', 'task__title'] # Search by subtask or parent task title
    autocomplete_fields = ['task'] # Autocomplete widget for foreign key