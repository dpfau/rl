
import random

class MDP(object):

	action_set = set([])

	def __init__(self, state):
		self._state = state

	def state(self):
		return self._state

	def actions(self):
		''' return set of allowed actions '''
		return self.action_set

	def act(self, action):
		''' update state, return reward '''
		pass

class Grid(MDP):
	action_set = set(['u','d','l','r'])
	max_reward = -1

	def __init__(self, h=10, w=10, state=(0,0)):
		self.h = int(h)
		self.w  = int(w)
		self._state = state
		x, y = self._state
		assert x >=0 and x < self.h and y >= 0 and y < self.w, 'State is out of allowed range: x = %i y = %i' % self._state
		self.borders = [self.w*[None], self.h*[None], self.w*[None], self.h*[None]] # N, E, S, W border

	def discount(self):
		return 0.9

	def new_state(self, action):
		x, y = self._state
		if action is 'u':
			if x is not 0:
				return x-1, y
		elif action is 'l':
			if y is not 0:
				return x, y-1
		elif action is 'r':
			if y is not self.w-1:
				return x, y+1
		elif action is 'd':
			if x is not self.h-1:
				return x+1, y
		else:
			raise Error('Action not in allowed set')

	def act(self, action):
		new_state = self.new_state(action)
		if new_state is not None:
			self._state = new_state
			return (1, -1)
		return (1, -10)

	@staticmethod
	def one_way(grid1, grid2, border1, border2):
		i, j = border1
		p, q = border2
		if p is 0:
			state = 0, q
		elif p is 1:
			state = q, grid2.w-1
		elif p is 2:
			state = grid2.h-1, q
		elif p is 3:
			state = q, 0
		else:
			raise Error('Improper coordinates')
		grid1.borders[i][j] = (grid2, state)

	@staticmethod
	def join(grid1, grid2, border1, border2):
		one_way(grid1, grid2, border1, border2)
		one_way(grid2, grid1, border2, border1)

class GridWorld(MDP):
	''' Grid world environment, made up of list of Grid objects, as well as a list of borders, 
	    which map a particular point on the boundary to a Grid object and state tuple for that
	    Grid object. '''

	action_set = set(['u','d','l','r'])
	dir_to_idx = {'u':0, 'r':1, 'd':2, 'l':3} # map direction to index of 'borders' tuple corresponding to that border

	def __init__(self, grids=[Grid()], state=(0,0,0)):
		idx, x, y = state
		self._state = grids[idx], x, y
		self.grids = grids

	def act(self, action):
		if action in self.action_set:
			grid, x, y = self._state
			r = grid.act(action)
			if r is -10: # if we hit the border, check if we go to another grid
				border = grid.borders[self.dir_to_idx[action]]
				if border is None: # Nope, just hit a wall
					return r
				else:
					x, y = border[1]
					border[0].state = x, y
					self._state = border[0], x, y
					return -1
			else:
				return r
		else:
			raise Error('Action not in allowed set') 		

class TwoRooms(GridWorld):
	''' A gridworld consisting of two rooms, each of the same height and width
	    with a door connecting them at half the height of the room. '''

	def __init__(self, h=10, w=10, state=(0,0)):
		left  = Grid(h, w, state)
		right = Grid(h, w)
		link  = Grid(1, 1)
		left.borders[1][h//2] = (link,(0,0))
		right.borders[3][h//2] = (link,(0,0))
		link.borders = [[None], [(right,(h//2,0))], [None], [(left,(h//2,w-1))]]
		GridWorld.__init__(self, [left, right, link])

class Taxi(MDP):
	# Actions:
	# u - up
	# d - down
	# l - left
	# r - right
	# p - pickup
	# q - drop off (quit?)
	action_set = set(['u','d','l','r','p','q'])

	def __init__(self, goal=(1,0,2), state=(0,0,0,5,1,1,0)):
		grids = [Grid(2, 2), Grid(2, 3), Grid(1, 5), Grid(2, 1), Grid(2, 2), Grid(2, 2)]
		join(grids[2],grids[0],(0,0),(2,0))
		join(grids[2],grids[0],(0,1),(2,1))
		join(grids[2],grids[1],(0,2),(2,0))
		join(grids[2],grids[1],(0,3),(2,1))
		join(grids[2],grids[1],(0,4),(2,2))
		join(grids[2],grids[3],(2,0),(0,0))
		join(grids[2],grids[4],(2,1),(0,0))
		join(grids[2],grids[4],(2,2),(0,1))
		join(grids[2],grids[5],(2,3),(0,0))
		join(grids[2],grids[5],(2,4),(0,1))
		self.world = GridWorld(grids)
		self.goal = goal
		tg, tx, ty, pg, px, py, inCab = state
		self._state = self.world.grids[tg], tx, ty, self.world.grids[pg], px, py, inCab

	def act(self,action):
		if action in self.action_set:
			tg, tx, ty, pg, px, py, inCab = self._state # state is tuple consisting of grid, x, and y position of taxi and person, 
													   # and a binary variable for whether the person is in the cab or not
			if action in self.world.action_set:
				r = self.world.act(action)
				tg, tx, ty = self.world.state()
				if inCab:
					self._state = tg, tx, ty, tg, tx, ty, inCab
				else:
					self._state = tg, tx, ty, pg, px, py, inCab
				return r
			elif action is 'p':
				if tg is pg and tx is px and ty is py:
					self._state = tg, tx, ty, tg, tx, ty, 1
			elif action is 'q':
				if inCab is 1:
					self._state = tg, tx, ty, pg, px, py, 0
					gg, gx, gy = self.goal
					if gg == pg and gx == px and gy == py:
						return 1000 # Achieve the goal of dropping off the passenger
			return -1
		else:
			raise Error('Not a recognized action')

class Hanoi(MDP):
	pass

class Maze(Grid):
        def __init__(self, h=10, w=10, walls=[], state=(0,0)):
                self.h = int(h)
                self.w  = int(w)
                self._state = state
                self.walls = walls
                x, y = self._state
                assert x >=0 and x < self.h and y >= 0 and y < self.w, 'State is out of allowed range: x = %i y = %i' % self._state
                assert (x, y) not in walls, 'State inside a wall: x = %i y = %i' % self._state
                self.borders = [self.w*[None], self.h*[None], self.w*[None], self.h*[None]] # N, E, S, W border

        def new_state(self, action):
                res = Grid.new_state(self, action)
                if res not in self.walls:
                        return res
