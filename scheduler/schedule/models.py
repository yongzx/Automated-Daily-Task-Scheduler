from django.db import models

class Task(models.Model):
    """
    Event represent a task to be done within a time slot in a schedule
    """
    PRIORITY_STATUS = (
        (1, "Very Important"),
        (2, "Important"),
        (3, "Not that Important"),
    )
    task_name = models.CharField(max_length=200, help_text="Enter the name of the task")
    estimated_total_duration = models.IntegerField(blank=True, null=True,
                                                   help_text="How much time (in hours) would you estimate for the task to be completed?")
    deadline = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=1, choices = PRIORITY_STATUS)

    def __str__(self):
        return self.task_name