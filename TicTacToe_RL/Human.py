class Human:
	def __init__(self):
		pass

	def set_symbol(self, sym):
		self.sym = sym

	def take_action(self, env):
		while True:
			move = raw_input("Enter coordinates 'i,j' i and j must be between 0 and 2: ")
			i, j = move.split(',')
			i = int(i)
			j = int(j)
			if env.is_empty(i, j):
				env.board[i, j] = self.sym 
				break

	def update(self, env):
		pass

	def update_state_history(self, s):
		pass