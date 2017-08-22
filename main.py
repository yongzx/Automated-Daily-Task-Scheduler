"""
Tasks
=====
Use tri-nary tree to store all the tasks. 
(Reason: 
1. 	Modify the nodes by increasing and decreasing duration while traversing. 
2.	Frequent addition and deletion.)

Use max heap to store the tasks for a day.
(We consider the allocation of tasks with higher priority before
considering those with lower priority.)

Slots
=====
Use tri-nary tree with three trackers pointing to the E1, E2, E3 slot. 
(Reason: Easy to check the continuity of the time slots of different energy levels.)
""" 
