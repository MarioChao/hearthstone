from enum import Enum
from typing import TYPE_CHECKING

from character.character_class import Character, CharacterType
from character.character_effect_types import CharacterEffectType

if TYPE_CHECKING:
	from player_client.player import Player

# Types

type TargetsType = list[Character]

# Enums

class TargetAlliance(Enum):
	none = "none",
	friendly = "friendly",
	enemy = "enemy",
	all = "all",

class TargetCharacterType(Enum):
	location = "location",
	minions = "minions",
	heroes = "heroes",
	any_character = "any character",

class TargetChooseMethod(Enum):
	user_input = "user input",
	random = "random",
	all = "all",

# Query target class

class QueryTarget:
	def __init__(
			self,
			alliance: TargetAlliance,
			targeted_character_type: TargetCharacterType,
			count_range: tuple[int, int],
			choose_method: TargetChooseMethod,
			exclude_self=False,
			only_self=False,
			respect_taunt=False,
			respect_stealth=True,
	):
		self.alliance = alliance
		self.targeted_character_type = targeted_character_type
		self.count_range = count_range
		self.choose_method = choose_method
		self.exclude_self = exclude_self
		self.only_self = only_self
		self.respect_taunt = respect_taunt
		self.respect_stealth = respect_stealth

	# Check character functions

	def __check_character_alliance(self, source: Character, target: Character):
		match self.alliance:
			case TargetAlliance.friendly:
				return source.commander == target.commander
			case TargetAlliance.enemy:
				return source.commander != target.commander
			case TargetAlliance.all:
				return True
		return False

	def __check_character_type(self, target: Character):
		match self.targeted_character_type:
			case TargetCharacterType.location:
				return True
			case TargetCharacterType.minions:
				return target.character_type == CharacterType.minion
			case TargetCharacterType.heroes:
				return target.character_type == CharacterType.hero
			case TargetCharacterType.any_character:
				is_hero = target.character_type == CharacterType.hero
				is_minion = target.character_type == CharacterType.minion
				return is_hero or is_minion
		return False

	def __check_character_exclude_self(self, source: Character, target: Character):
		if self.exclude_self and source == target:
			return False
		return True

	def __check_character_only_self(self, source: Character, target: Character):
		if self.only_self and source != target:
			return False
		return True

	def __check_character_taunt(self, target: Character):
		if not self.respect_taunt:
			return True
		if not target.commander.battlefield.has_taunt():
			return True
		return target.has_active_taunt()

	def __check_character_not_stealth(self, target: Character):
		if not self.respect_stealth:
			return True
		return not CharacterEffectType.stealth in target.active_effect_types

	def check_character_valid(self, source: Character, target: Character):
		if target.health <= 0:
			raise Exception("Target character is dead")
		if not self.__check_character_alliance(source, target):
			raise Exception("Character alliance doesn't match")
		if not self.__check_character_type(target):
			raise Exception("Character type incorrect")
		if not self.__check_character_exclude_self(source, target):
			raise Exception("Can't select self character")
		if not self.__check_character_only_self(source, target):
			raise Exception("Can only select self character")
		if not self.__check_character_taunt(target):
			raise Exception("Character with Taunt not selected")
		if source.commander != target.commander and not self.__check_character_not_stealth(target):
			raise Exception("Can't select a Stealth character")
		return True

	# Check alliance functions

	def __check_player_alliance(self, player1: "Player", player2: "Player"):
		match self.alliance:
			case TargetAlliance.friendly:
				return player1 == player2
			case TargetAlliance.enemy:
				return player1 != player2
			case TargetAlliance.all:
				return True
		return False

	def check_players_valid(self, player1: "Player", player2: "Player"):
		if not self.__check_player_alliance(player1, player2):
			raise Exception("Player alliance doesn't match")
		return True

	# Specific check functions

	def __check_targets_valid(self, new_targets: TargetsType):
		commanders = set()
		for target in new_targets:
			commanders.add(target.commander)

		# Check # of different enemy commanders, etc.
		match self.alliance:
			case TargetAlliance.enemy:
				pass
		return True

	def can_add_target(self, initial_targets: TargetsType, new_target: Character):
		new_targets = initial_targets + [new_target]
		if not self.__check_targets_valid(new_targets):
			return False
		return True

	# Check count

	def check_count(self, length):
		min_check = self.count_range[0] <= length or self.count_range[0] == -1
		max_check = length <= self.count_range[1] or self.count_range[1] == -1
		return min_check and max_check
