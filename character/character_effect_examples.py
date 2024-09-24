"""Contains common character effects (e.g. taunt, charge)"""

from character.character_effects import CharacterAbility
from character.character_effect_types import CharacterEffectType
from effects.effect_functions import create_dummy_effect, create_character_special_effect, create_combined_effects, \
	create_stat_edit_effect
from target.query_target import QueryTarget, TargetAlliance, TargetCharacterType, TargetChooseMethod


# Example special effects

def create_taunt_ability():
	return CharacterAbility(
		CharacterEffectType.taunt,
		create_character_special_effect({CharacterEffectType.taunt}, set()),
		create_character_special_effect(set(), {CharacterEffectType.taunt}),
		QueryTarget(
			TargetAlliance.friendly, TargetCharacterType.minions,
			(1, 1), TargetChooseMethod.all,
			only_self=True
		)
	)

def create_charge_ability():
	return CharacterAbility(
		CharacterEffectType.charge,
		create_combined_effects([
			create_character_special_effect({CharacterEffectType.charge}, set()),
			create_stat_edit_effect({"moves_left": 1})
		]),
		create_character_special_effect(set(), {CharacterEffectType.charge}),
		QueryTarget(
			TargetAlliance.friendly, TargetCharacterType.minions,
			(1, 1), TargetChooseMethod.all,
			only_self=True
		)
	)

def create_stealth_ability():
	return CharacterAbility(
		CharacterEffectType.stealth,
		create_character_special_effect({CharacterEffectType.stealth}, set()),
		create_character_special_effect(set(), {CharacterEffectType.stealth}),
		QueryTarget(
			TargetAlliance.friendly, TargetCharacterType.minions,
			(1, 1), TargetChooseMethod.all,
			only_self=True
		)
	)
