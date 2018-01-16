from Task import Task
from Slots import Slots
from hill_climbing import hill_climbing
from simulated_annealing import anneal
from random import random
import numpy as np
from artificial_neural_network import predict

# Initialize or update the slots' energy
schedule = Slots()
schedule.put_energy(3, "06:00", "10:00")
schedule.put_energy(2, "10:00", "12:00")
schedule.put_energy(1, "13:00", "15:00")
schedule.put_energy(3, "16:00", "18:00")
schedule.put_energy(2, "20:00", "23:59")

# Fix schedule such as the time for sleeping\

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


# schedule.put_act("Sleep", "00:00", "06:00")
# schedule.put_act("Lunch", "12:00", "13:00")
# schedule.put_act("Dinner", "17:00", "18:00")

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

# tasks.add(Task("Essay", priority=3, end_date="2018-01-20", estimated_time=10*60, category="Assignment"))
# tasks.add(Task("Programming", priority=3, end_date="2018-01-20", estimated_time=10*60, category="Assignment"))
# tasks.add(Task("Writing", priority=3, end_date="2018-01-20", estimated_time=10*60, category="Assignment"))
# tasks.add(Task("Manga", priority=3, end_date="2018-01-20", estimated_time=10*60, category="Assignment"))

training_x = []
training_y = []

while True:
    var_score, deadline_score, cont_score = random(), random(), random()

    # Generate the Schedule
    # Use machine learning algorithm to check the variability, deadline and continuity preference

    hill_climbing(schedule, tasks)
    schedule = anneal(schedule, list(tasks), var_score, deadline_score, cont_score)

    if len(training_x) < 100:
        print(schedule)

    else:
        prediction = predict(np.array([var_score, deadline_score, cont_score]), np.array(training_x),
                             np.array(training_y))
        if not prediction:
            continue
        else:
            print(schedule)

    satisfied = input("Are you satisfied with the schedule? (Y/N)\n")
    answer = None
    if satisfied == "Y":
        answer = 1
    else:
        answer = 0

    training_x.append(np.array([var_score, deadline_score, cont_score]))
    training_y.append(answer)







