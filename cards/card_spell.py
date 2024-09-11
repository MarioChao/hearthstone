from typing import TYPE_CHECKING

from cards.card_base import Card
from target.query_target import TargetsType, TargetChooseMethod

if TYPE_CHECKING:
	from game_controller import GameController
	from spells.spell_module import Spell

# Spell card class

class SpellCard(Card):
	def __init__(
			self,
			name: str,
			mana_cost: int,
			description: str,
			spells: list["Spell"],
	):
		super().__init__(name, mana_cost, description)
		self.spells = spells

	def get_targets_list(self, game: "GameController"):
		# Go through & get each spell's targets
		targets_list = []
		for spell in self.spells:
			while True:
				print()
				print(f"Current spell: *** {spell} ***")
				targets = spell.input_targets(game)

				# Break directly is targets are random
				if spell.query_target.choose_method == TargetChooseMethod.random:
					break

				# Targets confirmation
				print(f"{" Target Decision ":-^30}")
				print(f"Targets: {", ".join(target.name for target in targets)}")
				print()
				while True:
					targets_confirmation_input = input("Do you want to use the selected targets? (y/n): ")
					if targets_confirmation_input in ("y", "n"):
						break
				if targets_confirmation_input == "y":
					break

				# Quit spell selection
				while True:
					spell_card_confirmation_input = input("Continue 'y' or quit 'n' spell selection? (y/n): ")
					if spell_card_confirmation_input in ("y", "n"):
						break
				if spell_card_confirmation_input == "n":
					return []
			if spell.can_cast_spell(targets):
				targets_list.append(targets)
			else:
				print("Not correct number of targets selected!")
				return []

		# Return targets for each spell
		return targets_list

	def play(self, targets_list: list[TargetsType]):
		# Play spells
		for spell, targets in zip(self.spells, targets_list):
			spell.spell_effect(targets)
