import math
from random import random, randrange, choice
from copy import deepcopy
from Task import Task
from datetime import datetime

def anneal(slots, tasks, variety_preference, deadline_preference, continuous_preference):
    """
    Use Simulated Annealing Algorithm to optimize the schedule even further by taking into account of three things:
    1. the variety score of the schedule, as some users prefer having a variety of tasks in a day.
    2. deadline_preference, as some users would like to get urgent things done in a short time rather than
    distributing the tasks over a long period of time.
    3. continuous score, as some users prefer interleave the tasks.

    :param slots: List[Slot] which is the schedule. Over here, the input slots is the initial solution
    :param tasks: Set(Task)
    :return: List[Slot]
    """
    def cost(slots, variety_preference, deadline_preference, continuous_preference):
        # variety score
        distinct_task = set()
        var_score = 0
        for slot in slots:
            if isinstance(slot.act, Task):
                distinct_task.add(slot.act)
                var_score += 1

        # priority score, to ensure the schedule still focuses on getting the highly prioritized things done
        prio_score = 0
        for slot in slots:
            if isinstance(slot.act, Task):
                prio_score += slot.act.get_priority() * 0.05

        # deadline score
        deadline_score = 0
        for slot in slots:
            if isinstance(slot.act, Task):
                deadline_score += (slot.act.get_deadline() - datetime.now().date()).days

        # continuous score
        cont_score = 0
        for i in range(1, len(slots)):
            if isinstance(slots[i].act, Task) and isinstance(slots[i-1].act, Task) and slots[i] == slots[i-1]:
                cont_score += 1

        return var_score * variety_preference + prio_score + deadline_score * deadline_preference + cont_score * continuous_preference

    def acceptance_probability(old_c, new_c, T):
        # > 1 when old_c has a higher cost than new_c
        return math.e ** ((old_c - new_c) / T)

    def neighbor(slots):
        s = deepcopy(slots)
        intervals_to_choose_from = []
        tmp = []
        for i in range(len(slots)):
            if not isinstance(slots[i].act, Task):
                continue
            elif i>0 and slots[i].act == slots[i-1].act:
                tmp.append(i)
            elif i == 0:
                tmp.append(i)
            else:
                if tmp:
                    intervals_to_choose_from.append(tmp[:])
                tmp = []

        r = random()
        if r > 0.5:
            # include a task outside the schedule
            print(type(tasks))
            r_task = tasks[randrange(0, len(tasks))]
            intervals_to_change = randrange(len(intervals_to_choose_from))
            r_start = choice(intervals_to_choose_from[intervals_to_change])
            r_end = choice(intervals_to_choose_from[intervals_to_change])

            for i in range(r_start, r_end+1):
                s[i].act = r_task

        else:
            # swap the task inside the schedule
            intervals_to_change1 = randrange(len(intervals_to_choose_from))
            intervals_to_change2 = randrange(len(intervals_to_choose_from))
            r_start1 = choice(intervals_to_choose_from[intervals_to_change1])
            r_end1 = choice(intervals_to_choose_from[intervals_to_change1])
            r_start2 = choice(intervals_to_choose_from[intervals_to_change2])
            r_end2 = choice(intervals_to_choose_from[intervals_to_change2])
            s[r_start1:r_end1+1], s[r_start2:r_end2+1] = s[r_start2:r_end2+1], s[r_start1:r_end1+1]

        return s

    solution = deepcopy(slots)
    old_cost = cost(solution, variety_preference, deadline_preference, continuous_preference)
    T, T_min, alpha = 1.0, 0.00001, 0.9

    while T > T_min:
        i = 1
        while i <= 100:
            new_solution = neighbor(solution)
            new_cost = cost(new_solution, variety_preference, deadline_preference, continuous_preference)
            ap = acceptance_probability(old_cost, new_cost, T)
            if ap > random():
                solution = new_solution
                old_cost = new_cost
            i += 1
        T = T*alpha

    return solution
