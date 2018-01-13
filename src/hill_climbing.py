from datetime import datetime
from copy import deepcopy

def hill_climbing(slots, tasks):
    # Use Hill Climbing local search algorithm to generate the schedule by modifying the list slots.

    tmp_tasks = deepcopy(tasks)

    def cost(slot, task):
        # aim to maximize the cost for optimization
        return slot.energy * task.get_priority() / (task.get_deadline() - datetime.now().date()).days

    task_input = None
    task_time = None
    for slot in slots:
        if slot.act:
            continue

        max_cost = 0
        if task_input is None:
            for task in tmp_tasks:
                if cost(slot, task) > max_cost:
                    task_input = task
                    max_cost = cost(slot, task)
            if task_input:
                task_time = task_input.task_time_per_day()

        if not task_input:
            break

        slot.put_act(task_input)
        task_time -= slot.DURATION
        task_input.done(slot.DURATION)

        if task_input.isDone():
            tasks.remove(task_input)
            tmp_tasks.remove(task_input)

        if task_time == 0:
            tmp_tasks.remove(task_input)
            task_input = None
            task_time = None

