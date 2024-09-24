"""Contains the character class which represents heroes and minions on the battlefield"""

import typing
from copy import deepcopy
from typing import TYPE_CHECKING
from enum import Enum

from character.character_effect_types import CharacterEffectType

if TYPE_CHECKING:
	from cards.card_minion import MinionCard
	from character.character_effects import CharacterAbility
	from player_client.player import Player

# Enums

class CharacterType(Enum):
	none = "none",
	minion = "minion",
	hero = "hero",

# Types

EffectState = typing.TypedDict("EffectState", {"effect": "CharacterAbility", "state": bool})

# Character class

class Character:
	def __init__(self, player: "Player"):
		self.character_type = CharacterType.none
		self.commander = player
		self.name = ""
		self.description = ""
		self.max_health = 0
		self.health = 0
		self.attack = 0
		self.defense = 0
		self.moves_left = 0
		self.source_card = None
		self.effect_states: list[EffectState] = list()
		self.active_effect_types: set["CharacterEffectType"] = set()
		self.active_aura_effects: set["CharacterAbility"] = set()

	def set_as_minion(self, minion: "MinionCard"):
		self.character_type = CharacterType.minion
		self.name = minion.name
		self.description = minion.description
		self.max_health = minion.health
		self.health = minion.health
		self.attack = minion.attack
		self.defense = 0
		self.moves_left = 0
		self.source_card = minion

		self.clear_effect_states()
		self.add_multiple_effects(deepcopy(minion.card_effects))

	def set_as_hero(self, health: int):
		self.character_type = CharacterType.hero
		self.name = self.commander.name
		self.description = "A hero"
		self.max_health = health
		self.health = health
		self.attack = 0
		self.defense = 0

	# Access functions

	def get_attack(self):
		return self.attack

	# Turn functions

	def reset_moves(self):
		if self.character_type == CharacterType.minion:
			self.moves_left = 1
		else:
			self.moves_left = 0

	# Attack stat functions

	def change_attack(self, change_by: int):
		self.attack += change_by

	# Health functions

	def change_max_health(self, change_by: int):
		self.max_health += change_by
		if change_by > 0:
			# Increment current health by same amount
			self.health += change_by
		else:
			# Clamp the current health
			self.health = min(self.max_health, self.health)

	def restore_health(self, restore_by: int):
		assert restore_by >= 0

		# Restore health, capping at maximum health
		self.health += restore_by
		self.health = min(self.max_health, self.health)

		# Save logs
		self.commander.game.save_log(
			f"<{self.commander.name}>'s"
			f" character [{self.name}]"
			f" restored to {self.health} health."
		)

	def receive_damage(self, damage: int):
		assert damage >= 0

		# Reduce health
		self.health -= damage

		# Save logs
		self.commander.game.save_log(
			f"<{self.commander.name}>'s"
			f" character [{self.name}]"
			f" received {damage} damage,"
			f" {self.health} health remaining."
		)

	def set_health(self, health: int):
		self.health = health

	def destroy(self):
		self.set_health(0)

	# Effect functions

	def clear_effect_states(self):
		self.remove_all_effects()
		self.active_effect_types.clear()
		self.effect_states.clear()

	def add_multiple_effects(self, effects: list["CharacterAbility"]):
		for effect in effects:
			self.add_effect(effect, False)
		self.apply_effects()

	def add_effect(self, effect: "CharacterAbility", refresh=True):
		# Append enabled effect
		self.effect_states.append({"effect": effect, "state": True})

		if refresh:
			self.apply_effects()

	def remove_all_effects(self):
		for effect_state in self.effect_states:
			if not effect_state["state"]:
				continue

			# Disable the effect
			effect_state["state"] = False

		self.apply_effects()

	def remove_effect(self, effect: "CharacterAbility"):
		for effect_state in self.effect_states:
			if effect_state["effect"] != effect:
				continue
			if not effect_state["state"]:
				continue

			# Disable the effect
			effect_state["state"] = False

		self.apply_effects()

	def apply_effects(self):
		# Own effects
		for effect_state in self.effect_states:
			effect = effect_state["effect"]
			if effect_state["state"]:
				effect.apply(self, self.commander.game)
			else:
				effect.silence(self, self.commander.game)

		# Aura effects
		self.commander.game.aura.apply_aura_effects(self)

	def has_active_taunt(self):
		if self.character_type == CharacterType.none:
			return False
		if CharacterEffectType.stealth in self.active_effect_types:
			return False
		return CharacterEffectType.taunt in self.active_effect_types

	# Aura effect

	def has_active_aura_effect(self, aura_effect: "CharacterAbility"):
		return aura_effect in self.active_aura_effects

	def apply_aura_effect(self, aura_effect: "CharacterAbility"):
		if aura_effect in self.active_aura_effects:
			return

		self.active_aura_effects |= {aura_effect}
		aura_effect.apply_effect_function([self])

	def remove_aura_effect(self, aura_effect: "CharacterAbility"):
		if not aura_effect in self.active_aura_effects:
			return

		self.active_aura_effects -= {aura_effect}
		aura_effect.silence_effect_function([self])

	# Event functions

	def on_attack(self):
		# Remove stealth
		if CharacterEffectType.stealth in self.active_effect_types:
			self.active_effect_types -= {CharacterEffectType.stealth}
			self.commander.game.save_log(
				f"<{self.commander.name}>'s"
				f" character [{self.name}]"
				f" lost stealth."
			)

	def on_destruction(self):
		assert self.health <= 0

		if self.character_type == CharacterType.none:
			return

		# Print character death
		print(f"(DEATH) <{self.commander.name}>'s [{self.name}] was destroyed!")

		# Save logs
		self.commander.game.save_log(
			f"<{self.commander.name}>'s"
			f" character [{self.name}]"
			f" was destroyed."
		)

		# Remove active effects

		self.clear_effect_states()

		self.character_type = CharacterType.none

		# TODO: Death effects
		pass

	# Display functions

	def get_state_display(self):
		result_str = ""
		if self.moves_left <= 0:
			result_str += "-Zzz- "
		if CharacterEffectType.stealth in self.active_effect_types:
			result_str += "-STEALTH- "
		elif self.has_active_taunt():
			result_str += "-TAUNT- "
		return result_str

	def get_display(self, is_detailed=False):
		result_str = ""
		if self.character_type != CharacterType.none:
			result_str = self.get_state_display()
			result_str += (
				f"{self.name}"
				f" | Attack: {self.attack:<4} | Health: {self.health:<4}"
			)
			if self.defense > 0:
				result_str += f" | Defense: {self.defense:<4}"
			if is_detailed:
				result_str += f" | {self.description}"
		return result_str
