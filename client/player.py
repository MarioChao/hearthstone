from typing import TYPE_CHECKING

from cards.card_base import Card
from cards.card_minion import MinionCard
from cards.card_spell import SpellCard
from client.battlefield import Battlefield
from character.character_class import Character
from client.deck import Deck
from client.hand import Hand

if TYPE_CHECKING:
	from game_controller import GameController

# Player class

class Player:
	def __init__(self, name: str, deck: Deck):
		self.name = name
		self.max_mana_crystal = 0
		self.mana_crystal = 0
		self.deck = deck
		self.hand = Hand()
		self.battlefield = Battlefield(self)

		self.max_hand = 10
		self.fatigue = 0

		self.hero = Character(self)
		self.hero.set_as_hero(30)

		self.game: "GameController" = None

	# Set up functions

	def set_game(self, game: "GameController"):
		self.game = game

	# Mana functions

	def set_max_mana_crystal(self, max_mana_crystal):
		self.max_mana_crystal = max_mana_crystal

	def reset_mana(self):
		self.mana_crystal = self.max_mana_crystal

	# Deck functions

	def draw_card(self, print_result=False):
		# Check for fatigue
		if not self.deck.cards:
			# Save logs
			self.game.save_log(
				f"<{self.name}>"
				f" is experiencing fatigue."
			)

			# Calculate fatigue
			self.fatigue += 1

			# Receive fatigue
			self.hero.receive_damage(self.fatigue)
			print("{Fatigue}")
			print(f"Out of cards!")
			print(f"\t<{self.name}> take {self.fatigue} damage.")
			return

		# Overdraw
		if len(self.hand.cards) >= self.max_hand:
			card = self.deck.remove_top_card()
			print(f"{{Overdrawn}} Card: {card}")

			# Save logs
			self.game.save_log(
				f"<{self.name}>"
				f" overdrew card [{card.name}]."
			)
			return

		# Draw card
		card = self.deck.draw_card()
		self.hand.add_card(card)

		# Save logs
		self.game.save_log(
			f"<{self.name}>"
			f" drew the card [{card.name}]."
		)

		# Optionally prints result
		if print_result:
			print(f"Drawn card: {card}")
		return card

	# Hand functions

	def discard_card(self, card: Card):
		# Save logs
		self.game.save_log(
			f"<{self.name}>"
			f" discarded [{card.name}]."
		)

		# Remove card
		self.remove_card(card)
		print(f"Discarded card: [{card.name}]")

		# TODO: Discard effect

	def remove_card(self, card: Card):
		# Remove a card object from player's hand
		if card in self.hand.cards:
			self.hand.remove_card(card)

	def __play_and_remove_card(self, card: Card):
		# Decrease mana crystal
		self.mana_crystal -= card.mana_cost

		# Remove card from hand
		self.remove_card(card)

	def can_play_card(self, card: Card):
		in_hand = card in self.hand.cards
		has_enough_mana = card.mana_cost <= self.mana_crystal
		return in_hand and has_enough_mana

	def play_minion_card(self, card: MinionCard, position: int):
		# Check card playable
		if not self.can_play_card(card):
			return

		# Save logs
		self.game.save_log(
			f"<{self.name}>"
			f" played [{card.name}] minion"
			f" at battlefield position {position}."
		)

		# Play card
		self.battlefield.add_minion_at(card, position)
		self.__play_and_remove_card(card)
		card.play()

		# Save logs
		self.game.save_log(f"[{card.name}] minion finish played.")

		# Return success
		return True

	def play_spell_card(self, card: SpellCard):
		# Check card playable
		if not self.can_play_card(card):
			return

		# Get targets list
		targets_list = card.get_targets_list(self.game)
		if not targets_list:
			return

		# Spell card confirmation
		while True:
			spell_card_confirmation_input = input("Do you want to play the spell card? (y/n): ")
			if spell_card_confirmation_input in ("y", "n"):
				break
		if spell_card_confirmation_input == "n":
			return False

		# Save logs
		self.game.save_log(
			f"<{self.name}>"
			f" played [{card.name}] spell."
		)

		# Play card
		print()
		self.__play_and_remove_card(card)
		card.play(targets_list)

		# Save logs
		self.game.save_log(f"[{card.name}] spell finish played.")

		# Return success
		return True

	# Hero functions

	def get_health(self):
		return self.hero.health

	def set_health(self, health: int):
		self.hero.health = health

	def concede(self):
		# Save logs
		self.game.save_log(
			f"<{self.name}>"
			f" conceded."
		)

		self.set_health(0)

	# Display functions

	def display_hand(self, is_detailed=False):
		print(self.hand.get_display(is_detailed))

	def display_battlefield(self, is_detailed=False):
		print(self.battlefield.get_display(is_detailed))

	def __str__(self):
		return (
			f"{self.name}"
			f" - {self.get_health():02} health"
			f" - {self.mana_crystal}/{self.max_mana_crystal} mana crystals"
		)
