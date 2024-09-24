from typing import TYPE_CHECKING

from character.character_effect_types import CharacterEffectType
from effects.effect_functions import EffectFunction
from target.query_target import QueryTarget
from target.target_get import get_available_targets

if TYPE_CHECKING:
	from character.character_class import Character
	from game_controller import GameController

# Special effect class

class CharacterAbility:
	def __init__(
			self,
			effect_type: CharacterEffectType,
			apply_effect: EffectFunction,
			silence_effect: EffectFunction,
			query_target: "QueryTarget",
	):
		self.effect_type = effect_type
		self.apply_effect_function = apply_effect
		self.silence_effect_function = silence_effect
		self.query_target = query_target
		self.is_enabled = False
		self.is_silenced = False

	def set_enabled(self, enabled):
		self.is_enabled = enabled

	def apply(self, character: "Character", game: "GameController"):
		if self.is_enabled:
			return

		# Aura effects
		if self.effect_type == CharacterEffectType.aura:
			game.aura.create_aura_source(character, self)
			self.is_enabled = True

		# Regular effects
		else:
			targets = get_available_targets(self.query_target, game, character)
			self.apply_effect_function(targets)
			self.is_enabled = True

		# Save logs
		game.save_log(
			f"<{character.commander.name}>'s"
			f" character [{character.name}]"
			f" activated effect {self.effect_type}"
		)

	def silence(self, character: "Character", game: "GameController"):
		if not self.is_enabled:
			return

		if self.is_silenced:
			return

		# Aura effects
		if self.effect_type == CharacterEffectType.aura:
			game.aura.remove_aura_source(character)
			self.is_silenced = True

		# Regular effects
		else:
			targets = get_available_targets(self.query_target, game, character)
			self.silence_effect_function(targets)
			self.is_silenced = True

		# Save logs
		game.save_log(
			f"<{character.commander.name}>'s"
			f" character [{character.name}]"
			f" silenced effect {self.effect_type}"
		)
