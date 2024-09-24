"""Defines all cards (minion, spell)"""

from cards.card_minion import MinionCard
from cards.card_spell import SpellCard
from character.character_effect_examples import create_taunt_ability, create_charge_ability, create_stealth_ability
from character.character_effects import CharacterAbility
from character.character_effect_types import CharacterEffectType
from effects.effect_functions import create_damage_effect, create_stat_edit_effect, create_draw_card_effect, \
	create_healing_effect, create_destroy_effect, create_discard_card_effect, create_dummy_effect, \
	create_combined_effects, create_change_attack_effect, create_change_max_health_effect, create_transform_effect
from target.query_target import QueryTarget, TargetAlliance, TargetCharacterType, TargetChooseMethod
from spells.spell_module import Spell

# Variables

minion_cards = {
	"Chillwind Yeti": MinionCard(
		"Chillwind Yeti", 4,
		"A classic yeti minion with solid stats.",
		4, 5,
		[]
	),
	"Bloodfen Raptor": MinionCard(
		"Bloodfen Raptor", 2,
		"A powerful ogre minion with high attack and health.",
		3, 2,
		[]
	),
	"Boulderfist Ogre": MinionCard(
		"Boulderfist Ogre", 6,
		"A simple raptor minion with good stats for its cost.",
		6, 7,
		[]
	),
	"Sheep": MinionCard(
		"Sheep", 1,
		"",
		1, 1,
		[]
	),
	# Core set is 7/7, while Classic is 6/6
	"Stormwind Champion": MinionCard(
		"Stormwind Champion", 7,
		"Your other minions have +1/+1.",
		7, 7,
		[
			CharacterAbility(
				CharacterEffectType.aura,
				create_combined_effects([
					create_change_attack_effect(1),
					create_change_max_health_effect(1)
				]),
				create_combined_effects([
					create_change_attack_effect(-1),
					create_change_max_health_effect(-1)
				]),
				QueryTarget(
					TargetAlliance.friendly, TargetCharacterType.minions,
					(-1, -1), TargetChooseMethod.all,
					exclude_self=True
				)
			),
		]
	),
	"Booty Bay Bodyguard": MinionCard(
		"Booty Bay Bodyguard", 5,
		"Taunt",
		6, 6,
		[
			create_taunt_ability()
		]
	),
	"Wolfrider": MinionCard(
		"Wolfrider", 3,
		"Charge",
		3, 1,
		[
			create_charge_ability()
		]
	),
	"Spymistress": MinionCard(
		"Spymistress", 1,
		"Stealth",
		3, 1,
		[
			create_stealth_ability()
		]
	),
}

upcoming_minion_cards = {
}

spell_cards = {
	"Fireball": SpellCard(
		"Fireball", 4,
		"Deal 6 damage.",
		[
			Spell(
				"Deal 6 damage.",
				create_damage_effect(6),
				QueryTarget(
					TargetAlliance.all, TargetCharacterType.any_character,
					(1, 1), TargetChooseMethod.user_input
				)
			)
		]
	),
	"Polymorph": SpellCard(
		"Polymorph", 4,
		"Transform a minion into a 1/1 Sheep.",
		[
			Spell(
				"Transform a minion into a 1/1 Sheep.",
				create_transform_effect(minion_cards["Sheep"]),
				QueryTarget(
					TargetAlliance.all, TargetCharacterType.minions,
					(1, 1), TargetChooseMethod.user_input
				)
			)
		]
	),
	"Flamestrike": SpellCard(
		"Flamestrike", 7,
		"Deal 5 damage to all enemy minions.",
		[
			Spell(
				"Deal 5 damage to all enemy minions.",
				create_damage_effect(5),
				QueryTarget(
					TargetAlliance.enemy, TargetCharacterType.minions,
					(-1, -1), TargetChooseMethod.all,
					respect_stealth=False
				),
			)
		]
	),
	"Arcane Intellect": SpellCard(
		"Arcane Intellect", 3,
		"Draw 2 cards.",
		[
			Spell(
				"Draw 2 cards.",
				create_draw_card_effect(2),
				QueryTarget(
					TargetAlliance.friendly, TargetCharacterType.heroes,
					(-1, -1), TargetChooseMethod.all
				)
			)
		]
	),
	"Holy Nova": SpellCard(
		"Holy Nova", 3,
		"Deal 2 damage to all enemy minions. Restore 2 Health to all friendly characters.",
		[
			Spell(
				"Deal 2 damage to all enemy minions.",
				create_damage_effect(2),
				QueryTarget(
					TargetAlliance.enemy, TargetCharacterType.minions,
					(-1, -1), TargetChooseMethod.all,
					respect_stealth=False
				)
			),
			Spell(
				"Restore 2 Health to all friendly characters.",
				create_healing_effect(2),
				QueryTarget(
					TargetAlliance.friendly, TargetCharacterType.any_character,
					(-1, -1), TargetChooseMethod.all
				)
			)
		]
	),
	"Cataclysm": SpellCard(
		"Cataclysm", 5,
		"Destroy all minions. Discard 2 cards.",
		[
			Spell(
				"Destroy all minions.",
				create_destroy_effect(),
				QueryTarget(
					TargetAlliance.all, TargetCharacterType.minions,
					(-1, -1), TargetChooseMethod.all,
					respect_stealth=False
				)
			),
			Spell(
				"Discard 2 cards.",
				create_discard_card_effect(2),
				QueryTarget(
					TargetAlliance.friendly, TargetCharacterType.heroes,
					(-1, -1), TargetChooseMethod.all
				)
			)
		]
	),
	"Deadly Shot": SpellCard(
		"Deadly Shot", 3,
		"Destroy a random enemy minion.",
		[
			Spell(
				"Destroy a random enemy minion.",
				create_destroy_effect(),
				QueryTarget(
					TargetAlliance.enemy, TargetCharacterType.minions,
					(1, 1), TargetChooseMethod.random,
					respect_stealth=False
				)
			)
		]
	),
}
