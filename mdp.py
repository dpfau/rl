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

	def act(self, action):
		''' update state, return reward '''
		pass

class Grid(MDP):
	self.action_set = set(['u','d','l','r'])

	def __init__(self, state=(0,0), h=10, w=10):
		self.h = int(h)
		self.w  = int(w)
		self.state = state
		x, y = self.state
		assert x >=0 and x < self.h and y >= 0 and y < self.w, 'State is out of allowed range: x = %i y = %i' % self.state

	def act(self, action):
		if action in self.action_set:
			x, y = self.state
			if action is 'u':
				if x is not 0:
					self.state = x-1, y
					return -1
				else:
					return -10
			elif action is 'l':
				if y is not 0:
					self.state = x, y-1
					return -1
				else:
					return -10
			elif action is 'r':
				if y is not self.w-1:
					self.state = x, y+1
					return -1
				else:
					return -10
			else:
				if x is not self.h-1:
					self.state = x+1, y
					return -1
				else:
					return -10
		else:
			raise Error('Action not in allowed set') 		

class GridWorld(MDP):
	''' Grid world environment, made up of list of Grid objects, as well as a list of borders, 
	    which map a particular point on the boundary to a Grid object and state tuple for that
	    Grid object. '''

	self.action_set = set(['u','d','l','r'])
	self.dir_to_idx = {'u':0, 'r':1, 'd':2, 'l':3} # map direction to index of 'borders' tuple corresponding to that border

	def __init__(self, state=(0,0,0), grids=[Grid()], borders=None):
		idx, x, y = self.state
		self.state = grids[idx], x, y
		self.grids = grids
		if borders is None:
			for grid in self.grids
				grid.borders = (grid.w*[None], grid.h*[None], grid.w*[None], grid.h*[None]) # N, E, W, S border
		else:
			assert len(self.grids) == len(borders), 'Borders and grids must be one-to-one'
			for i in range(len(self.grids)):
				self.grids[i].borders = borders[i]

	def act(self, action):
		if action in self.action_set:
			grid, x, y = self.state
			r = grid.act(action)
			if r is -10: # if we hit the border, check if we go to another grid
				border = grid.borders[self.dir_to_idx[action]]
				if border is None: # Nope, just hit a wall
					return r
				else:
					x, y = border[1]
					border[0].state = x, y
					self.state = border[0], x, y
					return -1
			else:
				return r
		else:
			raise Error('Action not in allowed set') 		

class TwoRooms(GridWorld):
	''' A gridworld consisting of two rooms, each of the same height and width
	    with a door connecting them at half the height of the room. '''

	def __init__(self, state=(0,0), h=10, w=10):
		x, y = state
		left  = Grid((x,y), h, w)
		right = Grid((0,0), h, w)
		link  = Grid((0,0), 1, 1)
		leftborder  = [w*[None], h*[None], w*[None], h*[None]]
		leftborder[1][h/2] = (link,(0,0))
		rightborder = [w*[None], h*[None], w*[None], h*[None]]
		rightborder[3][h/2] = (link,(0,0))
		linkborder  = ([None], [(right,(h/2,0))], [None], [(left,(h/2,w-1))])
		GridWorld.__init__(self, (0,x,y), [left, right, link], [tuple(leftborder), tuple(rightborder), tuple(link)])

class Taxi(MDP):
	# Actions:
	# u - up
	# d - down
	# l - left
	# r - right
	# p - pickup
	# q - drop off (quit?)
	self.action_set = set(['u','d','l','r','p','q'])

	def __init__(self, state, goal):
		

	def act(self,action):


class Hanoi(MDP):
	pass
