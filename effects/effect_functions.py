"""Contains common effect functions for spells and character effects"""

import random
import typing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from cards.card_minion import MinionCard
	from character.character_effect_types import CharacterEffectType
	from target.query_target import TargetsType

# Types

type EffectFunction = typing.Callable[["TargetsType"], typing.Any]

# Functions

def get_commanders_set(targets: "TargetsType"):
	commanders = set()
	for target in targets:
		commanders.add(target.commander)
	return commanders

# Dummy effect

def create_dummy_effect():
	def dummy_effect(targets: "TargetsType"):
		pass
	return dummy_effect

# Combined effects

def create_combined_effects(effect_list: list[EffectFunction]):
	def combined_effects(targets: "TargetsType"):
		for effect in effect_list:
			effect(targets)
	return combined_effects

# Damage effects

def create_damage_effect(damage: int):
	def damage_effect(targets: "TargetsType"):
		for target in targets:
			target.receive_damage(damage)
	return damage_effect

def create_destroy_effect():
	def destroy_effect(targets: "TargetsType"):
		for target in targets:
			target.destroy()
	return destroy_effect

# Healing effects

def create_healing_effect(heal_by: int):
	def healing_effect(targets: "TargetsType"):
		for target in targets:
			target.restore_health(heal_by)
	return healing_effect

# Change stat effects

def create_change_max_health_effect(change_by: int):
	def change_max_health_effect(targets: "TargetsType"):
		for target in targets:
			target.change_max_health(change_by)
	return change_max_health_effect

def create_change_attack_effect(change_by: int):
	def change_attack_effect(targets: "TargetsType"):
		for target in targets:
			target.change_attack(change_by)
	return change_attack_effect

# Transform effects

def create_stat_edit_effect(morph_properties: typing.Dict[str, typing.Any]):
	def stat_edit_effect(targets: "TargetsType"):
		for target in targets:
			for property_name, property_value in morph_properties.items():
				setattr(target, property_name, property_value)
	return stat_edit_effect

def create_transform_effect(target_card: "MinionCard"):
	def transform_effect(targets: "TargetsType"):
		for target in targets:
			target.set_as_minion(target_card)
	return transform_effect

# Character special effects

def create_character_special_effect(add_effects: set["CharacterEffectType"], remove_effects: set["CharacterEffectType"]):
	def character_special_effect(targets: "TargetsType"):
		for target in targets:
			# Union update
			target.active_effect_types |= add_effects

			# Difference update
			target.active_effect_types -= remove_effects
	return character_special_effect

# Draw effects

def create_draw_card_effect(cards_count: int):
	def draw_card_effect(targets: "TargetsType"):
		if targets:
			target = targets[0]
			player = target.commander
			for _ in range(cards_count):
				player.draw_card(True)
	return draw_card_effect

# Discard effects

def create_discard_card_effect(cards_count: int):
	def discard_card_effect(targets: "TargetsType"):
		if targets:
			target = targets[0]
			player = target.commander

			# TODO: option for choosing cards to discard
			pass

			# Choose random cards
			discard_count = min(len(player.hand.cards), cards_count)
			selected_cards = random.sample(player.hand.cards, discard_count)

			# Discard cards
			for card in selected_cards:
				player.discard_card(card)
	return discard_card_effect
