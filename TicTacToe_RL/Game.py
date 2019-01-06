#!/ usr/binenv python
# -*- coding : utf -8 -*-

import numpy as np
from Agent import *
from Environment import * 
from Human import *


def get_state_hash_and_winner(env, i=0, j=0):
	results = []
	for v in (0, env.x, env.o):
		env.board[i,j] = v 
		if j == 2:
			if i == 2:
				state =  env.get_state()
				ended = env.game_over(force_recalculate=True)
				winner = env.winner
				results.append((state, winner, ended))
			else:
				results += get_state_hash_and_winner(env, i+1, 0)
		else:
			results += get_state_hash_and_winner(env, i, j+1)
	return results

def initialVx(env, state_winner_triples):
	# initializes state-values:
	# if x wins: V(s) = 1
	# if x loses or draw: V(s) = 0
	# else: V(s) = 0.5
	V = np.zeros(env.num_states)
	for state, winner, ended in state_winner_triples:
		if ended:
			if winner == env.x:
				v = 1
			else:
				v = 0
		else:
			v = 0.5
		V[state] = v 
	return V

def initialVo(env, state_winner_triples):
	# initializes state-values:
	# if o wins: V(s) = 1
	# if o loses or draw: V(s) = 0
	# else: V(s) = 0.5
	V = np.zeros(env.num_states)
	for state, winner, ended in state_winner_triples:
		if ended:
			if winner == env.o:
				v = 1
			else:
				v = 0
		else:
			v = 0.5
		V[state] = v 
	return V

def play_game(agent1, agent2, env, draw=False):
	currentPlayer = None

	while not env.game_over():

		# switch players
		if (currentPlayer == agent1):
			currentPlayer = agent2
		else:
			currentPlayer = agent1

		if draw:
			if draw == 1 and currentPlayer == agent1:
				env.draw_board()
			elif draw == 2 and currentPlayer == agent2:
				env.draw_board()

		# agent action
		currentPlayer.take_action(env)

		# get environment state
		state = env.get_state()
		agent1.update_state_history(state)
		agent2.update_state_history(state)
	
	if draw:
		env.draw_board()

	# update value-function
	agent1.update(env)
	agent2.update(env)

if __name__ == '__main__':
	# init
	env = Environment()
	agent1 = Agent()
	agent2 = Agent()
	state_winner_triples = get_state_hash_and_winner(env)
	print state_winner_triples
	Vx = initialVx(env, state_winner_triples)
	agent1.setV(Vx)
	agent1.set_symbol(env.x)
	Vo = initialVo(env, state_winner_triples)
	agent2.setV(Vo)
	agent2.set_symbol(env.o)

	# train
	T = 10000
	for t in xrange(T):
		if t % 200 == 0:
			print t 
		play_game(agent1, agent2, Environment())

	# play against human
	human = Human()
	human.set_symbol(env.o)
	while True:
		agent1.set_verbose(True)
		play_game(agent1, human, Environment(), draw=2)
		answer = raw_input("Play again? [Y/n]: ")
		if answer and answer.lower()[0] == 'n':
			break