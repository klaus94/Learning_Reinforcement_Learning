#!/ usr/binenv python
# -*- coding : utf -8 -*-

import numpy as np
from Agent import *
from Human import *
from Environment import *

def play_game(agent, env):
	while not env.game_over():
		env.print_state()
		agent.take_action(env)
	if not env.player_overbought:
		env.bank_move()
	env.print_state()

if __name__ == '__main__':
	# agent = Agent()
	agent = Human()
	play_game(agent, Environment())
