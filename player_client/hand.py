"""Handles a player's drawn cards"""

from cards.card_base import Card

class Hand:
	def __init__(self):
		self.cards = []

	def add_card(self, card: Card):
		self.cards.append(card)

	def remove_card(self, card: Card):
		self.cards.remove(card)

	def pop_card(self, card_index=-1):
		self.cards.pop(card_index)

	def get_display(self, is_detailed=False):
		result_str_list = []
		if is_detailed:
			# Full card detail
			for card_index in range(len(self.cards)):
				card = self.cards[card_index]
				result_str_list.append(f"\t{card_index:2}. {f"[{card}]":25}")
			result_str = "\n".join(result_str_list)
		else:
			# Card name + mana cost
			for card_index in range(len(self.cards)):
				card = self.cards[card_index]
				result_str_list.append(f"{f"[{card.name} (m: {card.mana_cost})]"}")
			result_str = "\t" + ",   ".join(result_str_list)

		return result_str
