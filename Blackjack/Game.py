#!/ usr/binenv python
# -*- coding : utf -8 -*-

import numpy as np
from Agent import *
from Human import *
from Environment import *

# state is tuple (sum(int), amount_of_aces(int), card_of_bank(string)) => 32*9*13 = 3744 states
def get_state_tuples(env):
	results = []
	for num in range(32):
		for aces in range(9):
			for bank_card in CARDS:
				results.append((num, aces, bank_card))
	return results

def initialV(state_tuples):
	V = {}
	for state_tuple in state_tuples:
		if state_tuple[0] > 21:
			V[state_tuple] = 0
		else:
			V[state_tuple] = np.random.rand()
	return V

def play_game(agent, env):
	while not env.game_over():
		env.print_state()
		agent.take_action(env)
		agent.update_state_history(env.get_state())
	env.print_state()
	agent.update(env)

if __name__ == '__main__':
	state_tuples = get_state_tuples(Environment())
	V = initialV(state_tuples)
	agent = Agent()
	agent.setV(V)

	# train
	T = 40000
	for t in xrange(T):
		if t % 200 == 0:
			print t 
		play_game(agent, Environment())

	print ""
	print agent.V
	print ""

	agent.set_verbose(True)

	for i in range(10):
		play_game(agent, Environment(True))
		print ""

	# agent = Human()
	# play_game(agent, Environment())
