import random
from typing import TYPE_CHECKING

from target.query_target import QueryTarget, TargetsType, TargetCharacterType, TargetChooseMethod
from player_gameplay.player_input import input_character_type, input_any_minion, input_hero

if TYPE_CHECKING:
	from game_controller import GameController

# Functions

# Get all selectable targets
def get_available_targets(query_target: QueryTarget, game: "GameController") -> TargetsType:
	# Find all targets in the game
	raw_targets = []
	for player in game.players:
		raw_targets.append(player.hero)
		for character in player.battlefield.characters:
			raw_targets.append(character)

	# Filter valid targets
	available_targets = []
	player = game.turn_get_player()
	for target in raw_targets:
		# Check validity
		try:
			query_target.check_character_valid(player, target)
		except Exception:
			continue

		# Append
		available_targets.append(target)

	# Return filtered targets
	return available_targets

# For user input
def get_targets_user_input(query_target: QueryTarget, game: "GameController") -> TargetsType:
	targets = []

	# Input targets
	first_run = True
	while True:
		target_type = query_target.targeted_character_type

		# Continue input
		if not first_run:
			if not query_target.check_count(len(targets)):
				while True:
					continue_input = input("Continue selecting targets (y/n)?: ")
					if continue_input in ("y", "n"):
						break
				if continue_input == "n":
					break
			else:
				break
		first_run = False

		# Input target character type
		if query_target.targeted_character_type == TargetCharacterType.any_character:
			# Input character type
			character_type_input = input_character_type()

			# Check exit
			if character_type_input == "-1":
				break

			# Set target character type
			match character_type_input:
				case "m":
					target_type = TargetCharacterType.minions
				case "h":
					target_type = TargetCharacterType.heroes

		# Input target character
		target_character = None
		match target_type:
			case TargetCharacterType.minions:
				target_character = input_any_minion(query_target, game)
			case TargetCharacterType.heroes:
				target_character = input_hero(query_target, game)

		# Check cancellation
		if not target_character:
			continue

		# Validate target
		try:
			query_target.check_character_valid(game.turn_get_player(), target_character)
		except Exception as e:
			print(f"Error: {e}")
			continue

		# Validate the addition of target
		if not query_target.can_add_target(targets, target_character):
			print("Target can't be added to the selection!")
			continue

		# Add target
		targets.append(target_character)

	# Return targets
	return targets

def get_targets_random(query_target: QueryTarget, game: "GameController") -> TargetsType:
	available_targets = get_available_targets(query_target, game)

	# Choose a random number of targets
	sample_size = min(len(available_targets), query_target.count_range[1])
	targets = random.sample(available_targets, sample_size)

	# Return targets
	return targets

def get_targets_all(query_target: QueryTarget, game: "GameController") -> TargetsType:
	targets = get_available_targets(query_target, game)
	return targets

def get_targets_input(query_target: QueryTarget, game: "GameController") -> TargetsType:
	targets = []
	match query_target.choose_method:
		case TargetChooseMethod.user_input:
			targets = get_targets_user_input(query_target, game)
		case TargetChooseMethod.random:
			targets = get_targets_random(query_target, game)
		case TargetChooseMethod.all:
			targets = get_targets_all(query_target, game)

	return targets
