#!/ usr/binenv python
# -*- coding : utf -8 -*-

import numpy as np

CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

card_sort_order = {
	"2": 0,
	"3": 1,
	"4": 2,
	"5": 3,
	"6": 4,
	"7": 5,
	"8": 6,
	"9": 7,
	"10": 8,
	"J": 9,
	"Q": 10,
	"K": 11,
	"A": 12
}

class Environment:
	def __init__(self, verbose=False):
		self.verbose = verbose
		self.agent_cards = []
		self.bank_cards = [self.random_card()]		# bank starts with one card open
		self.winner = None 							# bank/agent
		self.player_wants_next_card = True
		self.player_overbought = False

		if self.verbose:
			print "bank has: " + self.bank_cards[0]		# print bank state

	def agent_action_take_new_card(self, take_new_card):
		if take_new_card:
			if self.verbose:
				print "player takes a card"
			self.agent_draw_card()
		else:
			if self.verbose:
				print "player stops drawing cards"
			self.agent_no_more_card()

	def agent_draw_card(self):
		self.agent_cards.append(self.random_card())
		if self.cards_sum(self.agent_cards) > 21:
			self.player_overbought = True
			self.winner = "bank"

	def agent_no_more_card(self):
		self.player_wants_next_card = False
		self.bank_move()
		bank_sum = self.cards_sum(self.bank_cards)
		if bank_sum > 21:
			self.winner = "agent"
		elif self.cards_sum(self.agent_cards) <= bank_sum:
			self.winner = "bank"
		else:
			self.winner = "agent"

	def print_state(self):
		if not self.verbose:
			return
		if self.game_over():
			print self.winner + " wins"
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

	def game_over(self, force_recalculate=False):
		if force_recalculate:
			return self.cards_sum(self.agent_cards) > 21 or not self.player_wants_next_card
		return self.player_overbought or not self.player_wants_next_card

	def bank_move(self):
		while self.cards_sum(self.bank_cards) < 17:
			self.bank_cards.append(self.random_card())
		if self.verbose:
			print "bank has: " + ",".join(self.bank_cards) + " (" + str(self.cards_sum(self.bank_cards)) + ")"

	def reward(self):
		if self.winner == "agent":
			return 1
		else:
			return 0


	def random_card(self):
		return np.random.choice(CARDS)

	def get_state(self):
		# return tuple: 
		# ( agent_sum, amount_agent_aces, bank_card )
		return (self.cards_sum(self.agent_cards), self.agent_cards.count("A"), self.bank_cards[0])