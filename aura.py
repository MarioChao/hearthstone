"""Manages auras / ongoing effects during game"""

from character.character_class import Character
from character.character_effect_types import CharacterEffectType
from character.character_effects import CharacterAbility
from target.target_get import get_available_targets


# Aura class

class Aura:
	def __init__(self):
		self.aura_sources: list[tuple[Character, CharacterAbility]] = []

	def create_aura_source(self, source: Character, ability: CharacterAbility):
		if ability.effect_type != CharacterEffectType.aura:
			return

		self.aura_sources.append((source, ability))

		# Run apply effect on active targets
		targets = get_available_targets(ability.query_target, source.commander.game, source)
		ability.apply_effect_function(targets)

	def remove_aura_source(self, source: Character):
		new_aura_effects = []
		for effect in self.aura_sources:
			if effect[0] == source:
				# Run silence effect on remaining targets
				targets = get_available_targets(effect[1].query_target, source.commander.game, source)
				effect[1].silence_effect_function(targets)
				continue

			# Append remaining effect
			new_aura_effects.append(effect)

		self.aura_sources = new_aura_effects

	def apply_aura_effects(self, target: Character):
		for effect in self.aura_sources:
			try:
				effect[1].query_target.check_character_valid(effect[0], target)
			except Exception:
				continue

			if target.has_active_aura_effect(effect[1]):
				continue
			target.apply_aura_effect(effect[1])

			# Save logs
			target.commander.game.save_log(
				f"<{target.commander.name}>'s"
				f" character [{target.name}]"
				f" gained aura effect from [{effect[0].name}]."
			)

	def remove_aura_effects(self, target: Character):
		for effect in self.aura_sources:
			if not target.has_active_aura_effect(effect[1]):
				continue
			target.remove_aura_effect(effect[1])

			# Save logs
			target.commander.game.save_log(
				f"<{target.commander.name}>'s"
				f" character [{target.name}]"
				f" lost aura effect from [{effect[0].name}]."
			)