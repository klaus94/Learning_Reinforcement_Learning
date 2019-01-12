#!/ usr/binenv python
# -*- coding : utf -8 -*-

import numpy as np
from Environment import CARDS

class Agent:
	def __init__(self, eps=0.1, alpha=0.5):
		self.eps = eps 
		self.alpha = alpha
		self.state_history = []
		self.verbose = False

	def setV(self, V):
		self.V = V

	def set_verbose(self, verbose):
		self.verbose = verbose

	def reset_history(self):
		self.state_history = []

	def take_action(self, env):
		# decide if agent should do env.agent_action_take_new_card(True/False)

		r = np.random.rand()
		if r < self.eps:
			if self.verbose:
				print "random action"
			take_new_card = np.random.choice([True, False])
		else:
			# take-card
			value_taking_new_card = 0
			for next_card in CARDS:
				env.agent_cards.append(next_card)
				state = env.get_state()
				env.agent_cards.pop()
				value_taking_new_card += 1.0 / len(CARDS) * self.V[state]

			# take-no-more-card
			value_taking_no_card = self.V[env.get_state()]

			if self.verbose:
				print "new: " + str(value_taking_new_card) + " ; no more: " + str(value_taking_no_card)
			take_new_card = value_taking_new_card > value_taking_no_card

		env.agent_action_take_new_card(take_new_card)

	def update_state_history(self, state):
		self.state_history.append(state)

	def update(self, env):
		# backtrack over the states, so that
		# V(prev_state) = V(prev_state) + alpha * ( V(next_state) - V(prev_state) )		// update-rule
		# V(next_state) = reward, if it is the most current state
		reward = env.reward()
		target = reward
		for prev in reversed(self.state_history):
			value = self.V[prev] + self.alpha * (target - self.V[prev])
			self.V[prev] = value
			target = value 
		self.reset_history()
