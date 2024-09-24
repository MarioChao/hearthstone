"""Handles a player's card deck"""

import random
from copy import deepcopy

from cards.card_base import Card

class Deck:
	def __init__(self, cards: list[Card]):
		self.cards = deepcopy(cards)

	def shuffle_cards(self):
		random.shuffle(self.cards)

	def draw_card(self):
		if self.cards:
			return self.cards.pop(0)
		else:
			return None

	def remove_top_card(self):
		if self.cards:
			return self.cards.pop(0)
