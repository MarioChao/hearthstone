import random
import typing

from character.character_class import CharacterType
from target.query_target import TargetsType

# Type

type SpellEffect = typing.Callable[[TargetsType], typing.Any]

# Functions

def get_commanders_set(targets: TargetsType):
	commanders = set()
	for target in targets:
		commanders.add(target.commander)
	return commanders

# Damage effects

def create_damage_effect(damage: int):
	def damage_effect(targets: TargetsType):
		for target in targets:
			target.receive_damage(damage)
	return damage_effect

def create_destroy_effect():
	def destroy_effect(targets: TargetsType):
		for target in targets:
			target.destroy()
	return destroy_effect

# Healing effects

def create_healing_effect(heal_by: int):
	def healing_effect(targets: TargetsType):
		for target in targets:
			target.restore_health(heal_by)
	return healing_effect

# Morph effects

def create_morph_effect(morph_properties: typing.Dict[str, typing.Any]):
	def morph_effect(targets: TargetsType):
		for target in targets:
			for property_name, property_value in morph_properties.items():
				setattr(target, property_name, property_value)
	return morph_effect

# Draw effects

def create_draw_card_effect(cards_count: int):
	def draw_card_effect(targets: TargetsType):
		if targets:
			target = targets[0]
			player = target.commander
			for _ in range(cards_count):
				player.draw_card(True)
	return draw_card_effect

# Discard effects

def create_discard_card_effect(cards_count: int):
	def discard_card_effect(targets: TargetsType):
		if targets:
			target = targets[0]
			player = target.commander

			# Choose random cards
			discard_count = min(len(player.hand.cards), cards_count)
			selected_cards = random.sample(player.hand.cards, discard_count)

			# Discard cards
			for card in selected_cards:
				player.discard_card(card)
	return discard_card_effect
