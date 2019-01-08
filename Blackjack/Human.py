#!/ usr/binenv python
# -*- coding : utf -8 -*-

class Human:
	def take_action(self, env):
		while True:
			yesNo = raw_input("take a new card? [y/n] ")
			if yesNo in "yn":
				if yesNo == "y":
					env.agent_draw_card()
				else:
					env.player_wants_next_card = False
				break
