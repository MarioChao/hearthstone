from typing import TYPE_CHECKING

from target.query_target import TargetsType, QueryTarget
from effects.effect_functions import EffectFunction
from target.target_get import get_targets_input

if TYPE_CHECKING:
	from game_controller import GameController

# Class

class Spell:
	def __init__(self, description: str, spell_effect: EffectFunction, query_target: QueryTarget):
		self.description = description
		self.spell_effect = spell_effect
		self.query_target = query_target

	def input_targets(self, game: "GameController") -> TargetsType:
		# Get targets
		targets = get_targets_input(self.query_target, game)

		# Return targets
		return targets

	def can_cast_spell(self, targets: TargetsType):
		is_target_len_valid = self.query_target.check_count(len(targets))
		return is_target_len_valid

	def __str__(self):
		return self.description
