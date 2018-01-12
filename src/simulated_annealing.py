import math
from random import random, choice

def anneal(solution, sorted_tasks, total_hrs):
    """
    Approach: Simulated Annealing Algorithm
    =======================================
    :return: a sequence of tasks for a day
    """
    def cost(sol):
        # variety score
        var_score = 0
        distinct_set = set()
        for task in sol:
            if task not in distinct_set:
                distinct_set.add(task)
                var_score += 1

        # priority score
        prio_score = 0
        for task in sol:
            prio_score += task.duration * task.priority

        # deadline score
        deadline_score = 0
        for task in sol:
            if not task.deadline:
                deadline_score += 1 / task.deadline

        return var_score + prio_score + deadline_score

    def acceptance_probability(old_c, new_c, T):
        # > 1 when new_c has a higher cost than old_c
        return math.e ** (new_c - old_c / T)

    def neighbor(sol):
        # need to meet constraint of < total hour
        while True:
            new_task, to_be_swapped_task = choice(sorted_tasks), choice(sol)
            i = sol.index(to_be_swapped_task)
            sol[i] = new_task
            if sum(task.duration for task in sol) < total_hrs:
                break
            else:
                sol[i] = to_be_swapped_task
        return sol

    old_cost = cost(solution)
    T, T_min, alpha = 1.0, 0.00001, 0.9
    while T > T_min:
        i = 1
        while i <= 100:
            new_solution = neighbor(solution)
            new_cost = cost(new_solution)
            ap = acceptance_probability(old_cost, new_cost, T)
            if ap > random():
                solution = new_solution
                old_cost = new_cost
            i += 1
        T = T*alpha

    return solution
