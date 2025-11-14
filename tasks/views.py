from django.shortcuts import render

from tasks.models import Task


# from django.http import HttpResponse



def homepage(request):
    # return HttpResponse ("Welcome to Task Manager! ")
    return render(request, 'home.html')

def about(request):
    # return HttpResponse("My About page.")
    return render(request, 'about.html')


def tasks_list(request):
    # Загружаем задачи и связанные подзадачи за один запрос (оптимизация)
    #  prefetch_related('subtasks') — предзагружает подзадачи, чтобы избежать множества SQL-запросов.
    tasks = Task.objects.prefetch_related('subtasks').all().order_by('-created_at')
    return render(request, 'tasks/tasks_list.html', {'tasks': tasks})