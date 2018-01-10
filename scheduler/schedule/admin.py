from django.contrib import admin
from .models import Task

# admin.site.register(Task)
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'estimated_total_duration','deadline', 'priority')
    list_filter = ('priority', 'deadline')