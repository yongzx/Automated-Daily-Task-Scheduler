import datetime


def hill_climbing(slots, tasks):
    # Use Hill Climbing local search algorithm to generate the schedule by modifying the list slots.

    def cost(slot, task):
        # aim to maximize the cost for optimization
        return slot.energy * task.priority / (task.deadline - datetime.date.today())

    task_input = None
    task_time = None
    for slot in slots:
        if slot.act:
            continue

        max_cost = 0
        if task_input is None:
            for task in tasks:
                if cost(slot, task) > max_cost:
                    task_input = task
                    max_cost = cost(slot, task)
            task_time = task_input.task_time_per_day()

        slot.put_act(task_input)
        task_time -= slot.DURATION
        task_input.done(slot.DURATION)

        if task_input.isDone():
            tasks.remove(task_input)

        if task_time == 0:
            task_input = None
            task_time = None
