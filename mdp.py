import random

class MDP(object):

	self.action_set = set([])

	def __init__(self, state):
		self.state = state

	def state(self):
		return self.state

	def actions(self):
		''' return set of allowed actions '''
		return self.action_set

	def act(self,action):
		''' update state, return reward '''
		pass

class TwoRooms(MDP):
	''' A gridworld consisting of two rooms, each of the same height and width
	    with a door connecting them at half the height of the room.  The state
	    space is represented as (height, width, room), where room is 0 or 1 in
	    a room, and -1 in the doorway between them, in which case the height
	    and width are 0 by (my totally arbitrary) convention. '''

	self.action_set = set(['u','d','l','r'])

	def __init__(self, state, h=10, w=10):
		self.h = int(h)
		self.w  = int(w)
		self.state = state
		x, y, r = self.state
		if x < 0 or x >= h\
	    or y < 0 or y >= w\
	    or r < -1 or r > 1\
	    or (r == 0 and (x != 0 or y != 0)):
	    	raise Error('State is out of allowed range') 

	def act(self,action):
		if action in self.action_set:
			x, y, r = self.state
			if r == -1:
				if action is 'l':
					self.state = self.h/2, self.w-1, 0
					return -1
				elif action is 'r':
					self.state = self.h/2, 0, 1
					return -1
				else:
					return -10
			else:
				if action is 'l':
					if y > 0:
						self.state = x, y-1, r
						return -1
					elif r is 1 and x is self.h/2:
						self.state = 0, 0, -1
						return -1
					else:
						return -10
				if action is 'r':
					if y < self.w-1:
						self.state = x, y+1, r
						return -1
					elif r is 0 and x is self.h/2:
						self.state = 0, 0, -1
						return -1
					else:
						return -10
				if action is 'u':
					if x > 0:
						self.state = x-1, y, r
						return -1
					else:
						return -10
				if action is 'd':
					if x < self.h-1:
						self.state = x+1, y, r
						return -1
					else:
						return -10
		else:
			raise Error('Action not in allowed set') 

class Taxi(MDP):
	pass

class Hanoi(MDP):
	pass
