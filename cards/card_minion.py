from typing import TYPE_CHECKING

from cards.card_base import Card

if TYPE_CHECKING:
	from character.character_effects import CharacterAbility

# Minion card class

class MinionCard(Card):
	def __init__(
			self,
			name: str,
			mana_cost: int,
			description: str,
			attack: int,
			health: int,
			card_effects: list["CharacterAbility"],
	):
		super().__init__(name, mana_cost, description)
		self.attack = attack
		self.health = health
		self.card_effects = card_effects

	def play(self):
		pass

	def __str__(self):
		return (
			f"{self.name:>20} | Mana cost: {self.mana_cost:<2d}"
			f" | Attack: {self.attack:<2d} | Health: {self.health:<2d}"
			f" | {self.description}"
		)
