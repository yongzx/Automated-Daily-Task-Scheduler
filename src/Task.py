import datetime


class Task:
    def __init__(self, name, priority, end_date, estimated_time, category):
        self._name = name
        self._priority = priority
        self._start_date = datetime.date.today()
        self._end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        self._estimated_time = estimated_time       # in minutes
        self.category = category

    def get_name(self):
        return self._name

    def get_priority(self):
        return self._priority

    def get_deadline(self):
        return self._end_date

    def get_estimated_time(self):
        return self._estimated_time

    def task_time_per_day(self):
        task_time = self._estimated_time / (self._end_date - datetime.date.today()).days # in minutes in multiple of tens
        if task_time % 10:
            task_time = (task_time // 10 + 1) * 10
        return task_time

    def done(self, t):
        self._estimated_time -= t

    def isDone(self):
        return not self._estimated_time
