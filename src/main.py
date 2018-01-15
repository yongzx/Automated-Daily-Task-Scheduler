from Task import Task
from Slots import Slots
from hill_climbing import hill_climbing
from simulated_annealing import anneal
from random import random

# Initialize or update the slots' energy
schedule = Slots()
schedule.put_energy(3, "06:00", "10:00")
schedule.put_energy(2, "10:00", "12:00")
schedule.put_energy(1, "13:00", "15:00")
schedule.put_energy(3, "16:00", "18:00")
schedule.put_energy(2, "20:00", "23:59")

# Fix schedule such as the time for sleeping
fixed_act = []
current_act = "Current Fixed Activities: "
while True:
    act = input("Fixed Activity: ")
    start_time = input("Start Time (HH:MM): ")
    end_time = input("End Time (HH:MM): ")
    schedule.put_act(act, start_time, end_time)
    current_act += act
    print(current_act)
    current_act += ", "
    next_step = input("Type Y and press ENTER if done. Else type any key and press ENTER.\n")
    if next_step == "Y":
        break

# Take in tasks
tasks = set()
while True:
    task_name = input("Name of Task: ")
    prio = input("Priority (1-3):")
    end_date = input("Deadline (YYYY-MM-DD): ")
    estimated_time = input("Number of hours estimated to finish the task: ")
    category = input("Nature of Task: ")
    tasks.add(Task(task_name, priority=int(prio), end_date=end_date, estimated_time=float(estimated_time)*60, category=category))
    next_step = input("Type Y and press ENTER if done. Else type any key and press ENTER.\n")
    if next_step == "Y":
        break

var_score, deadline_score, cont_score = random(), random(), random()

# Generate the Schedule
# Use machine learning algorithm to check the variability, deadline and continuity preference

hill_climbing(schedule, tasks)
schedule = anneal(schedule, list(tasks), var_score, deadline_score, cont_score)
print(schedule)
