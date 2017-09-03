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

from bintrees import RBTree

class Tasks(TernaryTree):

	def __init__(self):
		TernaryTree.__init__(self)
		self.left = RBTree()
		self.mid = RBTree()
		self.right = RBTree()

	def __str__(self):
		return "{0} \n{1} \n{2} ".format(self.left.__repr__(), self.mid.__repr__(), self.right.__repr__())

	def get_task_from_user(self, name, priority, duration_in_hr, deadline):
		if priority == 3:
			self.right[deadline] = [name, duration_in_hr]
		elif priority == 2:
			self.mid[deadline] = [name, duration_in_hr]
		elif priority == 1:
			self.left[deadline] = [name, duration_in_hr]


T = Tasks()
T.get_task_from_user("Essay", priority = 3, duration_in_hr = 3.5, deadline = 2)
T.get_task_from_user("Event", priority = 3, duration_in_hr = 8, deadline = 4)
T.get_task_from_user("Assigned Reading", priority = 3, duration_in_hr = 10, deadline = 5)
T.get_task_from_user("Reading", priority = 2, duration_in_hr = 10, deadline = 20)

print(T)