#!/ usr/binenv python
# -*- coding : utf -8 -*-

class Human:
	def take_action(self, env):
		while True:
			yesNo = raw_input("take a new card? [y/n] ")
			if yesNo in "yn":
				if yesNo == "y":
					env.agent_action_take_new_card(True)
				else:
					env.agent_action_take_new_card(False)
				break

	def update_state_history(self, state):
		pass

	def update(self, env):
		pass