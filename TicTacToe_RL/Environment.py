import numpy as np

LENGTH = 3

class Environment:
	def __init__(self):
		self.board = np.zeros((LENGTH, LENGTH))
		self.x = -1
		self.o = 1
		self.winner = None
		self.ended = False
		self.num_states = 3**(LENGTH*LENGTH)

	def is_empty(self, i, j):
		return self.board[i,j] == 0

	def reward(self, sym):
		if not self.game_over():
			return 0
		return 1 if self.winner == sym else 0

	# convert board to number
	def get_state(self):
		k = 0
		h = 0
		for i in xrange(LENGTH):
			for j in xrange(LENGTH):
				if self.board[i,j] == 0:
					v = 0
				elif self.board[i,j] == self.x:
					v = 1
				elif self.board[i,j] == self.o:
					v = 2
				h += (3**k) * v 
				k += 1
		return h

	# force_recalculate True shortens the calc-effort, if the game already ended
	# force_recalculate False might be needed for testing future steps (agent-planning)
	def game_over(self, force_recalculate=False):
		if not force_recalculate and self.ended:
			return self.ended

		# check rows
		for i in xrange(LENGTH):
			for player in (self.x, self.o):
				if self.board[i].sum() == player*LENGTH:
					self.winner = player
					self.ended = True
					return True

		# check columns
		for j in xrange(LENGTH):
			for player in (self.x, self.o):
				if self.board[:,j].sum() == player*LENGTH:
					self.winner = player
					self.ended = True
					return True

		# check diagonal \
		for player in (self.x, self.o):
			if self.board.trace() == player*LENGTH:
				self.winner = player
				self.ended = True
				return True

		# check diagonal /
		for player in (self.x, self.o):
			if np.fliplr(self.board).trace() == player*LENGTH:
				self.winner = player
				self.ended = True
				return True

		# check draw
		if np.all((self.board == 0) == False):
			self.winner = None
			self.ended = True
			return True

		# game is running
		self.winner = None
		self.ended = False
		return False

	def draw_board(self):
		for i in xrange(LENGTH):
			print 13*"-"
			for j in xrange(LENGTH):
				print " ",
				if self.board[i,j] == self.x:
					print "x",
				elif self.board[i,j] == self.o:
					print "o",
				else:
					print " ",
			print ""
		print 13*"-"
