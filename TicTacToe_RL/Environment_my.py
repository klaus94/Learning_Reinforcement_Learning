#!/ usr/binenv python
# -*- coding : utf -8 -*-

class Environment(object):
	def __init__(self):
		self.board = "000000000"
		self.state = GameState.RUNNING

	def game_over(self):
		return self.state != GameState.RUNNING

	def get_state(self):
		return self.board, self.state

	# player... 1 or 2
	# move ...  0..8 left to right, top to bottom
	def player_move(self, player, move):
		if player != 1 and player != 2:
			raise Exception("[player_move] player was not 1 or 2")
		if move < 0 or move > 8:
			raise Exception("[player_move] move was not valid: " + str(move))

		if self.board[move] != "0":
			raise Exception("[player_move] move not valid. board has piece at this position already")

		self.board = self.change_char(self.board, move, str(player))
		self.check_end_of_game()

	def check_end_of_game(self):
		# check draw
		if "0" not in self.board:
			self.state = GameState.DRAW
			return

		# check horizontal win
		for r in range(3):
			row = self.board[3*r] + self.board[3*r+1] + self.board[3*r+2]
			if self.is_line_winning_line(row):
				return

		# check vertical win
		for c in range(3):
			column = self.board[c] + self.board[3+c] + self.board[6+c]
			if self.is_line_winning_line(column):
				return

		# check diagonal /
		diag1 = self.board[2] + self.board[4] + self.board[6]
		if self.is_line_winning_line(diag1):
			return

		# check dialgonal \
		diag2 = self.board[0] + self.board[4] + self.board[8]
		if self.is_line_winning_line(diag2):
			return

	def is_line_winning_line(self, line):
		if line == "111":
			self.state = GameState.PLAYER_1_WON
			return True
		if line == "222":
			self.state = GameState.PLAYER_2_WON
			return True
		return False


	def twoD_to_oneD(self, tuple):
		return 3 * tuple[1] + tuple[0]

	def change_char(self, s, p, r):
		return s[:p]+r+s[p+1:]

class GameState:
	RUNNING = 0
	PLAYER_1_WON = 1
	PLAYER_2_WON = 2
	DRAW = 3