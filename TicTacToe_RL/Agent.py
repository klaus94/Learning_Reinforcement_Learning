#!/ usr/binenv python
# -*- coding : utf -8 -*-

import numpy as np
from Environment import LENGTH

class Agent:
	def __init__(self, eps=0.1, alpha=0.5):
		self.eps = eps 
		self.alpha = alpha
		self.verbose = False
		self.state_history = []

	def setV(self, V):
		self.V = V

	def set_symbol(self, sym):
		self.sym = sym

	def set_verbose(self, verbose):
		self.verbose = verbose

	def reset_history(self):
		self.state_history = []

	def take_action(self, env):
		r = np.random.rand()
		if r < self.eps:
			# random action
			if self.verbose:
				print "taking random action"
			possible_moves = []
			for i in xrange(LENGTH):
				for j in xrange(LENGTH):
					if env.is_empty(i, j):
						possible_moves.append((i,j))
			idx = np.random.choice(len(possible_moves))
			next_move = possible_moves[idx]
		else:
			# best move
			next_move = None
			best_value = -1
			for i in xrange(LENGTH):
				for j in xrange(LENGTH):
					if env.is_empty(i, j):
						# what is the state if we made this move?
						env.board[i,j] = self.sym
						state = env.get_state()
						env.board[i,j] = 0				# change it back
						if self.V[state] > best_value:
							best_value = self.V[state]
							next_move = (i,j)
		env.board[next_move[0], next_move[1]] = self.sym

	def update_state_history(self, state):
		self.state_history.append(state)

	def update(self, env):
		# backtrack over the states, so that
		# V(prev_state) = V(prev_state) + alpha * ( V(next_state) - V(prev_state) )		// update-rule
		# V(next_state) = reward, if it is the most current state
		reward = env.reward(self.sym)
		target = reward
		for prev in reversed(self.state_history):
			value = self.V[prev] + self.alpha * (target - self.V[prev])
			self.V[prev] = value
			target = value 
		self.reset_history()
