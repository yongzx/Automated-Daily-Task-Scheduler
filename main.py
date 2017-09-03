import random

class TernaryTree:

	def __init__(self):
		self.left = None
		self.mid = None
		self.right = None

class Time:
	
	def __init__(self, time):
		self.time = time
		self.hr = int(time[:2])
		self.min = int(time[2:])

	def __repr__(self):
		return self.time

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
		# for now, assume other is duration in minutes.
		# return a time
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
	# for now, assume other is duration in minutes.
	# return a time
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

class Slots(TernaryTree):

	class Slot:
		def __init__(self, start_t, end_t, name = None, energy_level = None):
			self.start_t = start_t
			self.end_t = end_t
			self.name = name
			self.energy_level = energy_level

		def __str__(self):
			return "{}-{}".format(self.start_t.time, self.end_t.time)

	class ListNode:
		def __init__(self, slot, nxt = None, prev = None):
			self.slot = slot
			self.next = nxt
			self.prev = prev
	
	def __init__(self):
		TernaryTree.__init__(self)
		self.left, self.mid, self.right = self.ListNode("E1"), self.ListNode("E2"), self.ListNode("E3")

	def initialize_slots(self, fixed_intervals):
		# improve by taking input instead of pre-setting the slots 
		
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
				
				start_t = slow.next
				slow.next = None
				
				left = shuffle_helper(linked_list)
				right = shuffle_helper(start_t)
				
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

	def get_slot(self):
		start = self.right.next
		while start:
			yield start.slot
			start = start.next

		start = self.mid.next
		while start:
			yield start.slot
			start = start.next

		start = self.left.next
		while start:
			yield start.slot
			start = start.next

"""
S = Slots()
S.initialize_slots([])

tmp_left = S.left
tmp_mid = S.mid
tmp_right= S.right
for tmp in (tmp_left, tmp_mid, tmp_right):
	while tmp:
		print(tmp.slot.start.hr if isinstance(tmp.slot, Slots.Slot) else tmp.slot)
		tmp = tmp.next
	print("-----------------")

for s in S.get_slot():
	print(s.slot.energy_level, s.slot.start_t.hr, s.slot.end_t.hr)
"""

from bintrees import RBTree

class Tasks(TernaryTree):

	def __init__(self):
		TernaryTree.__init__(self)
		self.left = RBTree()
		self.mid = RBTree()
		self.right = RBTree()

	def __str__(self):
		return "{0} \n{1} \n{2} ".format(self.left.__repr__(), self.mid.__repr__(), self.right.__repr__())

	def get_task_from_user(self, name, priority, duration_in_min, deadline):
		if priority == 3:
			self.right[(deadline,name)] = duration_in_min
		elif priority == 2:
			self.mid[(deadline,name)] = duration_in_min
		elif priority == 1:
			self.left[(deadline,name)] = duration_in_min

	def get_task(self):
		iterator = self.right.iter_items(reverse=True)
		for task in iterator:
			yield task

		iterator = self.mid.iter_items(reverse=True)
		for task in iterator:
			yield task

		iterator = self.left.iter_items(reverse=True)
		for task in iterator:
			yield task

	def update_task(self, task_storage):
		for task in task_storage:
			deadline = task[0][0]
			name = task[0][1]

			if task[0] in self.right:
				self.right.pop((deadline,name))
				if deadline > 1:
					self.right[(deadline, name)] = task[1] - task[1]/deadline

			elif task[0] in self.mid:
				self.mid.pop((deadline, name))
				if deadline > 1:
					self.mid[(deadline, name)] = task[1] - task[1]/deadline 

			else:
				self.left.pop((deadline, name))
				if deadline > 1:
					self.left[(deadline, name)] = task[1] - task[1]/deadline 

		for task in self.right:
			deadline = task[0]
			name = task[1]
			duration = self.right[task]

			self.right.pop((deadline, name))
			if deadline - 1 > 0:
				self.right[(deadline - 1, name)] = duration

		for task in self.mid:
			deadline = task[0]
			name = task[1]
			duration = self.mid[task]

			self.mid.pop((deadline, name))
			if deadline - 1 > 0:
				self.mid[(deadline - 1, name)] = duration
		
		for task in self.left:
			deadline = task[0]
			name = task[1]
			duration = self.left[task]

			self.left.pop((deadline, name))
			if deadline - 1 > 0:
				self.left[(deadline - 1, name)] = duration

	def update_unfinished_task(self, task, duration):
		if (task[0]) in self.right:
			self.right[task[0]] -= duration

		elif (task[0]) in self.mid:
			self.mid[task[0]] -= duration

		elif (task[0]) in self.left:
			self.left[task[0]] -= duration

"""
T = Tasks()
T.get_task_from_user("Essay", priority = 3, duration_in_hr = 3.5, deadline = 2)
T.get_task_from_user("Event", priority = 3, duration_in_hr = 8, deadline = 4)
T.get_task_from_user("Assigned Reading", priority = 3, duration_in_hr = 10, deadline = 5)
T.get_task_from_user("Reading", priority = 2, duration_in_hr = 10, deadline = 20)
print(T)
"""

class Schedule:
	def __init__(self):
		self.schedule = []

	def create_schedule(self, fixed_intervals = []):
		S = Slots()
		S.initialize_slots(fixed_intervals)

		T = Tasks()
		T.get_task_from_user("Essay", priority = 3, duration_in_min = 3.5*60, deadline = 2)
		T.get_task_from_user("Event", priority = 3, duration_in_min = 8*60, deadline = 2)
		T.get_task_from_user("Assigned Reading", priority = 3, duration_in_min = 10*60, deadline = 5)
		T.get_task_from_user("Reading", priority = 2, duration_in_min = 10*60, deadline = 20)
		
		
		task_storage = set()
		curr_t, duration = 0, 0

		for s in S.get_slot():
			print(s)
			for t in T.get_task():
				if t in task_storage and not curr_t:
					continue

				deadline = t[0][0] if not curr_t else curr_t[0][0]
				name = t[0][1] if not curr_t else curr_t[0][1]
				duration = t[1]/deadline if not duration else duration			
				print(name, deadline, duration)

				if s.end_t - s.start_t == duration:
					self.schedule.append(("{}-{}".format(s.start_t.time, s.end_t.time), name))
					task_storage.add(t)
					curr_t, duration = 0, 0
					break

				elif s.end_t - s.start_t > duration:
					self.schedule.append(("{}-{}".format(s.start_t, s.start_t + duration), name))
					task_storage.add(t)
					curr_t, duration = 0, 0
					s.start_t = Time(s.start_t + duration/deadline)

				else:
					self.schedule.append(("{}-{}".format(s.start_t.time, s.end_t.time), name))
					duration -= (s.end_t - s.start_t)
					curr_t = t
					break

		T.update_task(task_storage)
		if curr_t:
			print(curr_t)
			T.update_unfinished_task(curr_t, duration)
		
		self.schedule.sort()
		return self.schedule

S = Schedule()
print(S.create_schedule())







