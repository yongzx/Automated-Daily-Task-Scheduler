import datetime


class Task:
    def __init__(self, name, priority, end_date, estimated_time):
        self._name = name
        self._priority = priority
        self._start_date = datetime.date.today()
        self._end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self._estimated_time = estimated_time

    def get_name(self):
        return self._name

    def get_priority(self):
        return self._priority

    def get_estimated_time(self):
        return self._estimated_time
