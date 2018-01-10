from django.shortcuts import render
from .models import Task
from django.views import generic


def index(request):
    """
    View function for home page of site.
    Shows the schedule.
    """
    # generate counts of tasks
    num_tasks = Task.objects.all().count()

    return render(
        request,
        'index.html',
        context={'num_tasks': num_tasks},
    )


class TaskListView(generic.ListView):
    model = Task
    template_name = 'tasks/task_list.html'
