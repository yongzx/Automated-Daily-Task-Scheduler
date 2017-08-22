"""
Tasks
=====
Use ternary tree and linked list to store all the tasks. 
(Reason: 
1. 	Three categories of priority	
2.	Modify the nodes by increasing and decreasing duration while traversing. 
3.	Frequent addition and deletion in the middle of the list.)

Use max heap to store the tasks for a day.
(Reason: We consider the allocation of tasks with higher priority before
considering those with lower priority.)

Slots
=====
Use ternary tree and linked list with three trackers pointing to the E1, E2, E3 slot. 
(Reason: Easy to check the continuity of the time slots of different energy levels.)
""" 

import heapq

class TernaryTree:

	def __init__(self):
		self.left = None
		self.mid = None
		self.right = None

class ListNode:

	def __init__(self, val, nxt = None, prev = None):
		self.val = val
		self.next = nxt
		self.prev = prev

class Tasks:

	class Task:

		def __init__(self, name, priority = None, duration = None):
			self.name = name
			self.priority = priority
			self.duration = duration*60

		def __lt__(self, other):
			return self.priority > other.priority if self.priority != other.priority\
				else (self.duration > other.duration)

	def __init__(self):
		self.all_tasks = TernaryTree()
		self.all_tasks.left, self.all_tasks.mid, self.all_tasks.right = \
			ListNode("P1"), ListNode("P2"), ListNode("P3")
		self.P1_last, self.P2_last, self.P3_last = \
			self.all_tasks.left, self.all_tasks.mid, self.all_tasks.right
		
		self.daily_tasks = []

	def get_task_from_user(self, name, priority, duration, deadline):

		if int(priority) == 1:
			self.P1_last.next = ListNode([name, int(duration), int(deadline)])
			self.P1_last.next.prev = self.P1_last
			self.P1_last = self.P1_last.next
		elif int(priority) == 2:
			self.P2_last.next = ListNode([name, int(duration), int(deadline)])
			self.P2_last.next.prev = self.P2_last
			self.P2_last = self.P2_last.next
		elif int(priority) == 3:
			self.P3_last.next = ListNode([name, int(duration), int(deadline)])
			self.P3_last.next.prev = self.P3_last
			self.P3_last = self.P3_last.next

	def get_tasks_for_today(self):
		# the duration of the daily task of priority 3 
		# has the minimum hour of 1 hour to maximum duration given
		# Reason: tasks with closer deadline should have a longer duration in daily schedule
		hours = 24
		P3 = self.all_tasks.right.next
		while P3 and hours:
			task_duration = P3.val[1] / P3.val[2] if (P3.val[1] / P3.val[2]) > 1 else 1
			if hours > task_duration:
				P3.val[1] -= task_duration
				hours -= task_duration
			else:
				P3.val[1] -= hours
				hours = 0
			if P3.val[1] == 0:
				if P3.next:
					P3.next.prev = P3.prev
				P3.prev.next = P3.next
			heapq.heappush(self.daily_tasks, self.Task(P3.val[0], 3, task_duration))
			P3 = P3.next

		P2 = self.all_tasks.mid.next
		while P2 and hours:
			task_duration = P2.val[1] / P2.val[2] if (P2.val[1] / P2.val[2]) > 1 else 1
			if hours > task_duration:
				P2.val[1] -= task_duration
				hours -= task_duration
			else:
				P2.val[1] -= hours
				hours = 0
			if P2.val[1] == 0:
				if P2.next:
					P2.next.prev = P2.prev
				P2.prev.next = P2.next
			heapq.heappush(self.daily_tasks, self.Task(P2.val[0], 2, task_duration))
			P2 = P2.next

		P1 = self.all_tasks.left.next
		while P1 and hours:
			task_duration = P1.val[1] / P1.val[2] if (P1.val[1] / P1.val[2]) > 1 else 1
			if hours > task_duration:
				P1.val[1] -= task_duration
				hours -= task_duration
			else:
				P1.val[1] -= hours
				hours = 0
			if P1.val[1] == 0:
				if P1.next:
					P1.next.prev = P1.prev
				P1.prev.next = P1.next
			heapq.heappush(self.daily_tasks, self.Task(P1.val[0], 1, task_duration))
			P1 = P1.next

		return self.daily_tasks

class Slot:
	def __init__(self, start, end, name, energy_level = None):
		self.start = start
		self.end = end
		self.name = name
		self.energy_level = energy_level

class Schedule:

	def __init__(self):
		self.occupied_slots = []
		self.available_slots = TernaryTree()
		self.available_slots.left, self.available_slots.mid, self.available_slots.right \
			= ListNode("E1"), ListNode("E2"), ListNode("E3")

	def initialize_slots(self):
		# improve by taking input instead of pre-setting the slots 
		self.occupied_slots = [Slot(Time("0000"), Time("0500"), "Sleep"), Slot(Time("0900"), Time("1200"), "Classes"),
								Slot(Time("1700"), Time("2000"), "Evening Execises") ,Slot(Time("2300"), Time("2359"), "Sleep")]
		
		free_slots = [Slot(Time("0500"), Time("0700"), None, 3), Slot(Time("0700"),Time("0900"), None, 2),
				Slot(Time("1200"), Time("1400"), None, 2), Slot(Time("1400"), Time("1700"), None, 1),
				Slot(Time("2000"), Time("2200"), None, 3), Slot(Time("2200"), Time("2300"), None, 2)]

		E1_tracker, E2_tracker, E3_tracker = self.available_slots.left, \
											self.available_slots.mid, self.available_slots.right
		for slot in free_slots:
			if slot.energy_level == 1:
				E1_tracker.next = ListNode(slot)
				E1_tracker.next.prev = E1_tracker
				E1_tracker = E1_tracker.next
			elif slot.energy_level == 2:
				E2_tracker.next = ListNode(slot)
				E2_tracker.next.prev = E2_tracker
				E2_tracker = E2_tracker.next
			elif slot.energy_level == 3:
				E3_tracker.next = ListNode(slot)
				E3_tracker.next.prev = E3_tracker
				E3_tracker = E3_tracker.next

class Time:
	
	def __init__(self, time):
		self.time = time
		self.hr = int(time[:2])
		self.min = int(time[2:])

	def __sub__(self, other):
		
		if type(other) is Time:
		#return duration in minutes
			if self.min >= other.min:
				minute = self.min - other.min
			else:
				self.hr -= 1
				minute = self.min+60 - other.min

			hour = self.hr - other.hr
			return hour*60+minute

		else:
		#return a time
			total = self.hr*60 + self.min
			total -= int(other)
			new_min = str(total%60)
			if len(new_min) < 2:
				new_min = "0" + new_min
			
			new_hr = str(total//60)
			if len(new_hr) < 2:
				new_hr = "0" + new_hr
			
			return new_hr + new_min

	def __add__(self, other):
		total = self.hr*60 + self.min
		total += int(other)
		new_min = str(total%60)
		if len(new_min) < 2:
			new_min = "0" + new_min
		new_hr = str(total//60)
		if len(new_hr) < 2:
			new_hr = "0" + new_hr
		return new_hr + new_min

	def __lt__(self, other):
		return self.time < other.time
			
def generate(tasks, slots, occupied_slots):
	current = heapq.heappop(tasks) if tasks else None
	
	slot_node = slots.right.next
	while slot_node and current:
		
		if slot_node.val.end - slot_node.val.start == current.duration:
			slot_node.val.name = current.name
			occupied_slots.append(slot_node.val)
			slot_node = slot_node.next
			current = heapq.heappop(tasks) if tasks else None

		elif slot_node.val.end - slot_node.val.start > current.duration:
			new_slot_end = slot_node.val.start + current.duration
			new_slot = Slot(slot_node.val.start, Time(new_slot_end), current.name)
			occupied_slots.append(new_slot)

			slot_start = slot_node.val.start + current.duration
			slot_node.val.start = Time(slot_start)
			current = heapq.heappop(tasks) if tasks else None

		else:
			slot_node.val.name = current.name
			occupied_slots.append(slot_node.val)
			current.duration -= slot_node.val.end - slot_node.val.start
			slot_node = slot_node.next


	slot_node = slots.mid.next
	while slot_node and current:

		if slot_node.val.end - slot_node.val.start == current.duration:
			slot_node.val.name = current.name
			occupied_slots.append(slot_node.val)
			slot_node = slot_node.next
			current = heapq.heappop(tasks) if tasks else None

		elif slot_node.val.end - slot_node.val.start > current.duration:
			new_slot_end = slot_node.val.start + current.duration
			new_slot = Slot(slot_node.val.start, Time(new_slot_end), current.name)
			occupied_slots.append(new_slot)

			slot_start = slot_node.val.start + current.duration
			slot_node.val.start = Time(slot_start)
			current = heapq.heappop(tasks) if tasks else None

		else:
			slot_node.val.name = current.name
			occupied_slots.append(slot_node.val)
			current.duration -= slot_node.val.end - slot_node.val.start
			slot_node = slot_node.next
	
	slot_node = slots.left.next
	while slot_node and current:
		if slot_node.val.end - slot_node.val.start == current.duration:
			slot_node.val.name = current.name
			occupied_slots.append(slot_node.val)
			slot_node = slot_node.next
			current = heapq.heappop(tasks) if tasks else None

		elif slot_node.val.end - slot_node.val.start > current.duration:
			new_slot_end = slot_node.val.start + current.duration
			new_slot = Slot(slot_node.val.start, Time(new_slot_end), current.name)
			occupied_slots.append(new_slot)

			slot_start = slot_node.val.start + current.duration
			slot_node.val.start = Time(slot_start)
			current = heapq.heappop(tasks) if tasks else None

		else:
			slot_node.val.name = current.name
			occupied_slots.append(slot_node.val)
			current.duration -= slot_node.val.end - slot_node.val.start
			slot_node = slot_node.next

	occupied_slots.sort(key = lambda x: x.start)
	return ["{} - {} : {}".format(slot.start.time, slot.end.time, slot.name) for slot in occupied_slots]


S = Schedule()
S.initialize_slots()
task = Tasks()
task.get_task_from_user("Essay", 3, 9, 6)
task.get_task_from_user("Event", 3, 8, 4)
task.get_task_from_user("Assigned Reading", 3, 10, 5)
task.get_task_from_user("Reading", 2, 10, 20)

ready_tasks = task.get_tasks_for_today()
print(generate(ready_tasks, S.available_slots, S.occupied_slots))
print()

# new day
S.initialize_slots()
ready_tasks = task.get_tasks_for_today()
print(generate(ready_tasks, S.available_slots, S.occupied_slots))
print()

# new day
S.initialize_slots()
ready_tasks = task.get_tasks_for_today()
print(generate(ready_tasks, S.available_slots, S.occupied_slots))
print()

