from Task import Task
from Slots import Slots
from hill_climbing import hill_climbing
from simulated_annealing import anneal

# Initialize or update the slots' energy
schedule = Slots()
schedule.put_energy(3, "08:00", "10:00")
schedule.put_energy(2, "10:00", "12:00")
schedule.put_energy(1, "13:00", "15:00")
schedule.put_energy(3, "16:00", "18:00")
schedule.put_energy(2, "20:00", "23:59")

# Fix schedule such as the time for sleeping
schedule.put_act("Sleep", "00:00", "08:00")
schedule.put_act("Lunch", "12:00", "13:00")
schedule.put_act("Nap", "15:00", "16:00")
schedule.put_act("Dinner", "18:00", "20:00")

# Take in tasks
tasks = set()
tasks.add(Task("Essay", priority=3, end_date="2018-01-14", estimated_time=8*60, category="Assignment"))
tasks.add(Task("Programming", priority=3, end_date="2018-01-19", estimated_time=4*60, category="Assignment"))
tasks.add(Task("Writing", priority=3, end_date="2018-01-30", estimated_time=8*60, category="Assignment"))

# Generate the Schedule and check with Machine Learning algorithm
hill_climbing(schedule, tasks)
anneal(schedule, list(tasks), 0.1, 0.1, 0.1)
print(schedule)