from django.shortcuts import render
from .models import Task
# Create your views here.

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
        context={'num_tasks':num_tasks},
    )