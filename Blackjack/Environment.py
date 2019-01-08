#!/ usr/binenv python
# -*- coding : utf -8 -*-

import numpy as np

card_values = {
	"2": 2,
	"3": 3,
	"4": 4,
	"5": 5,
	"6": 6,
	"7": 7,
	"8": 8,
	"9": 9,
	"10": 10,
	"J": 10,
	"Q": 10,
	"K": 10,
	"A": 11			# just needed for sorting, so 11 is ok -> A always at first place
}

class Environment:
	def __init__(self):
		self.agent_cards = []
		self.bank_cards = [self.random_card()]		# bank starts with one card open
		self.player_wants_next_card = True
		self.player_overbought = False

		print "bank has: " + self.bank_cards[0]		# print bank state

	def print_state(self):
		if self.game_over():
			if self.cards_sum(self.agent_cards) > 21:
				print "> bank wins. player overbought"
			elif self.cards_sum(self.bank_cards) > 21:
				print "> player wins. bank overbought"
			elif self.cards_sum(self.agent_cards) <= self.cards_sum(self.bank_cards):
				print "> bank wins"
			else:
				print "> player wins"
		else:
			print "player has: " + ", ".join(self.agent_cards) + " (" + str(self.cards_sum(self.agent_cards)) + ")"

	def cards_sum(self, cards):
		sum_of_cards = 0
		for card in cards:
			if card == "A":
				continue
			if card in "JQK":
				sum_of_cards += 10
			else:
				sum_of_cards += int(card)
		for i in range(cards.count("A")):
			if sum_of_cards + 11 > 21:
				sum_of_cards += 1
			else:
				sum_of_cards += 11
		return sum_of_cards

	def game_over(self):
		return self.cards_sum(self.agent_cards) > 21 or not self.player_wants_next_card

	def random_card(self):
		return np.random.choice(["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"])

	def bank_move(self):
		while self.cards_sum(self.bank_cards) < 17:
			self.bank_cards.append(self.random_card())
		print "bank has: " + ",".join(self.bank_cards) + " (" + str(self.cards_sum(self.bank_cards)) + ")"

	def agent_draw_card(self):
		self.agent_cards.append(self.random_card())
		if self.cards_sum(self.agent_cards) > 21:
			self.player_overbought = True

	def get_state(self):
		# order agent cards from high to low
		return sorted(self.agent_cards, key=lambda card: card_values[card], reverse=True)
