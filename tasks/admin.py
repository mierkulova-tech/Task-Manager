from django.contrib import admin
from .models import Task, SubTask, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'deadline', 'created_at']
    filter_horizontal = ['categories']  # удобный виджет для ManyToMany
    list_filter = ['status', 'created_at', 'deadline']
    search_fields = ['title']

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task', 'status', 'deadline']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'task__title']