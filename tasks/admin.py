from django.contrib import admin

from .models import Task, SubTask, Category

@admin.action(description="Mark selected subtasks as Done")
def mark_subtasks_as_done(modeladmin, request, queryset):
    """Mark selected subtasks as Done."""
    to_update = queryset.exclude(status='Done')
    updated_count = to_update.update(status='Done')
    modeladmin.message_user(request, f"{updated_count} subtasks marked as Done.")


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
    fields = ('title', 'description','status', 'deadline')
    show_change_link = True  # allow editing from inline

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""

    list_display = ['name',] # Show category name in admin list
    search_fields = ['name',] # Enable search by name

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin configuration for Task model."""
    list_display = ['short_title', 'status', 'deadline', 'created_at'] # Display key fields
    filter_horizontal = ['categories']  ## Widget for ManyToMany selection
    list_filter = ['status', 'created_at', 'deadline'] # Filter sidebar
    search_fields = ['title', 'description'] # Search by title or description
    inlines = [SubTaskInline] # add inlines

    def short_title(self, obj):
        title = obj.title[:10] + '...' if len(obj.title) > 10 else obj.title
        return f"{title} (ID: {obj.id})"
    short_title.short_description = "Title"


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    """Admin configuration for SubTask model."""

    list_display = ['title', 'task', 'status', 'deadline', 'created_at'] # Display fields
    list_filter = ['status', 'created_at'] # Filters for quick lookup
    search_fields = ['title', 'task__title'] # Search by subtask or parent task title
    autocomplete_fields = ['task'] # Autocomplete widget for foreign key
    actions = [mark_subtasks_as_done]