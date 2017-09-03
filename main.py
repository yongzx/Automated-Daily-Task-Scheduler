import heapq
import random

class TernaryTree:

	def __init__(self):
		self.left = None
		self.mid = None
		self.right = None

class Time:
	
	def __init__(self, time):
		self.hr = int(time[:2])
		self.min = int(time[2:])

	def __sub__(self, other):
		
		if isinstance(other, Time):
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
			print(type(other))
			total = self.hr*60 + self.min
			print(total)
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

class Schedule(TernaryTree):

	class Slot:
		def __init__(self, start, end, name = None, energy_level = None):
			self.start = start
			self.end = end
			self.name = name
			self.energy_level = energy_level

	class ListNode:
		def __init__(self, data, nxt = None, prev = None):
			self.data = data
			self.next = nxt
			self.prev = prev
	
	def __init__(self):
		TernaryTree.__init__(self)
		self.occupied_slots = []
		self.left, self.mid, self.right = self.ListNode("E1"), self.ListNode("E2"), self.ListNode("E3")

	def initialize_slots(self, fixed_intervals):
		# improve by taking input instead of pre-setting the slots 
		self.occupied_slots.extend(self.fixed_slots(fixed_intervals))
		
		E1_tracker, E2_tracker, E3_tracker = self.left, self.mid, self.right
											
		for slot in self.free_slots(fixed_intervals):
			if slot.energy_level == 1:
				E1_tracker.next = self.ListNode(slot)
				E1_tracker.next.prev = E1_tracker
				E1_tracker = E1_tracker.next
			elif slot.energy_level == 2:
				E2_tracker.next = self.ListNode(slot)
				E2_tracker.next.prev = E2_tracker
				E2_tracker = E2_tracker.next
			elif slot.energy_level == 3:
				E3_tracker.next = self.ListNode(slot)
				E3_tracker.next.prev = E3_tracker
				E3_tracker = E3_tracker.next

		for list_vary_E_level in [self.left, self.mid, self.right]:
			head = self.shuffle(list_vary_E_level.next)
			list_vary_E_level.next = head
			

	def fixed_slots(self, fixed_intervals):
		result = []
		for start_t, end_t, act in fixed_intervals:
			result.append(self.Slot(start_t, end_t, act))
		return result

	def free_slots(self, fixed_intervals):
		# database is needed
		# requires user input if database is empty
		return [self.Slot(Time("0500"), Time("0700"), None, 3), self.Slot(Time("0700"),Time("0900"), None, 2),
		self.Slot(Time("1200"), Time("1400"), None, 2), self.Slot(Time("1400"), Time("1700"), None, 1),
		self.Slot(Time("2000"), Time("2200"), None, 3), self.Slot(Time("2200"), Time("2300"), None, 2)]

	def shuffle(self, linked_list):

		def shuffle_helper(linked_list):
			if linked_list and linked_list.next:

				slow = linked_list
				fast = linked_list.next

				while fast.next and fast.next.next:
					slow = slow.next
					fast = fast.next.next
				
				start = slow.next
				slow.next = None
				
				left = shuffle_helper(linked_list)
				right = shuffle_helper(start)
				
				head = merge(left, right)
				return head
			
			return linked_list

		def merge(list1, list2):
			dummy = curr = self.ListNode(None)

			while list1 and list2:
				decider = random.randint(0,1)
				if not decider:
					curr.next = list1
					list1 = list1.next
				else:
					curr.next = list2
					list2 = list2.next

				curr.next.prev = curr
				curr = curr.next


			curr.next = (list1 if list1 else list2)
			
			return dummy.next

		return shuffle_helper(linked_list)

"""
S = Schedule()
S.initialize_slots([])
tmp_left = S.left
tmp_mid = S.mid
tmp_right= S.right
for tmp in (tmp_left, tmp_mid, tmp_right):
	while tmp:
		print(tmp.data.start.hr if isinstance(tmp.data, Schedule.Slot) else tmp.data)
		tmp = tmp.next
	print("-----------------")
"""

class Tasks:

	class Task:

		def __init__(self, name, priority = None, duration = None):
			HR_TO_MIN = 60
			self.name = name
			self.priority = priority
			self.duration = duration*HR_TO_MIN

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

	def get_task_from_user(self, name, priority, duration_in_hr, deadline):
		### improve by using input from user

		if int(priority) == 1:
			self.P1_last.next = ListNode({'name':name, 'duration':int(duration_in_hr), 'deadline':int(deadline), 'count_down':int(duration_in_hr)})
			self.P1_last.next.prev = self.P1_last
			self.P1_last = self.P1_last.next
		elif int(priority) == 2:
			self.P2_last.next = ListNode({'name':name, 'duration':int(duration_in_hr), 'deadline':int(deadline), 'count_down':int(duration_in_hr)})
			self.P2_last.next.prev = self.P2_last
			self.P2_last = self.P2_last.next
		elif int(priority) == 3:
			self.P3_last.next = ListNode({'name':name, 'duration':int(duration_in_hr), 'deadline':int(deadline), 'count_down':int(duration_in_hr)})
			self.P3_last.next.prev = self.P3_last
			self.P3_last = self.P3_last.next

	def get_tasks_for_today(self):
		# the duration of the daily task of priority 3 
		# has the minimum hour of 1 hour to maximum duration given
		# Reason: tasks with closer deadline should have a longer duration in daily schedule
		
		available_hrs = 24
		P3 = self.all_tasks.right.next
		while P3 and available_hrs:
			task_duration = P3.val['duration'] / P3.val['deadline'] if P3.val['duration'] / P3.val['deadline'] > 1 else 1
			print(P3.val['name'], task_duration)
			if available_hrs > task_duration:
				P3.val['count_down'] -= task_duration
				available_hrs -= task_duration
			else:
				task_duration = available_hrs
				P3.val['count_down'] -= available_hrs
				available_hrs = 0
			if P3.val['count_down'] == 0:
				if P3.next:
					P3.next.prev = P3.prev
				P3.prev.next = P3.next
			heapq.heappush(self.daily_tasks, self.Task(P3.val['name'], 3, task_duration))
			P3 = P3.next

		P2 = self.all_tasks.mid.next
		while P2 and available_hrs:
			task_duration = P2.val['duration'] / P2.val['deadline'] if P2.val['duration'] / P2.val['deadline'] > 1 else 1
			if available_hrs > task_duration:
				P2.val['count_down'] -= task_duration
				available_hrs -= task_duration
			else:
				task_duration = available_hrs
				P2.val['count_down'] -= available_hrs
				available_hrs = 0
			if P2.val['count_down'] == 0:
				if P2.next:
					P2.next.prev = P2.prev
				P2.prev.next = P2.next
			heapq.heappush(self.daily_tasks, self.Task(P2.val['name'], 2, task_duration))
			P2 = P2.next

		P1 = self.all_tasks.left.next
		while P1 and available_hrs:
			task_duration = P1.val['duration'] / P1.val['deadline'] if P1.val['duration'] / P1.val['deadline'] > 1 else 1
			if available_hrs > task_duration:
				P1.val['count_down'] -= task_duration
				available_hrs -= task_duration
			else:
				task_duration = available_hrs
				P1.val['count_down'] -= available_hrs
				available_hrs = 0
			if P1.val['count_down'] == 0:
				if P1.next:
					P1.next.prev = P1.prev
				P1.prev.next = P1.next
			heapq.heappush(self.daily_tasks, self.Task(P1.val['name'], 1, task_duration))
			P1 = P1.next

		return self.daily_tasks



			
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
task.get_task_from_user("Essay", priority = 3, duration_in_hr = 3.5, deadline = 2)
task.get_task_from_user("Event", priority = 3, duration_in_hr = 8, deadline = 4)
task.get_task_from_user("Assigned Reading", priority = 3, duration_in_hr = 10, deadline = 5)
task.get_task_from_user("Reading", priority = 2, duration_in_hr = 10, deadline = 20)

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

