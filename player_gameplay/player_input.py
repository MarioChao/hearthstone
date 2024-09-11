from typing import TYPE_CHECKING

from character.character_class import CharacterType
from client.player import Player
from target.query_target import QueryTarget, TargetAlliance

if TYPE_CHECKING:
	from game_controller import GameController

# Functions

def input_card_choice(player: Player):
	# Input choice
	while True:
		try:
			card_choice = int(input("Enter card index (-1 to cancel): "))
			assert -1 <= card_choice < len(player.hand.cards)
			break
		except Exception:
			print(f"Enter a number between -1 and {len(player.hand.cards) - 1}.")

	# Return choice
	return card_choice

def input_battlefield_position(player: Player):
	# Input choice
	while True:
		try:
			position = int(input("Enter battlefield position (-1 to cancel): "))
			assert -1 <= position < len(player.battlefield.characters)
			break
		except Exception:
			print(f"Enter a number between -1 and {len(player.battlefield.characters) - 1}.")

	# Return choice
	return position

def input_empty_battlefield_position(player: Player):
	# Input choice
	while True:
		try:
			position = input_battlefield_position(player)
			if position == -1:
				break

			# Check empty character
			initial_character = player.battlefield.characters[position]
			assert initial_character.character_type == CharacterType.none
			break
		except Exception:
			print("Enter an empty battlefield position!")

	# Return choice
	return position

def input_minion_battlefield_position(player: Player):
	# Input choice
	while True:
		try:
			position = input_battlefield_position(player)
			if position == -1:
				break

			# Check minion
			initial_character = player.battlefield.characters[position]
			assert initial_character.character_type == CharacterType.minion
			break
		except Exception:
			print("Enter a minion position!")

	# Return choice
	return position

def input_character_type():
	while True:
		print("'m' for minions")
		print("'h' for hero")
		character_type_input = input("Enter character type (-1 to exit): ")
		if character_type_input in ("m", "h", "-1"):
			break
	return character_type_input

def input_player_index(game: "GameController"):
	# Input choice
	while True:
		try:
			position = int(input("Enter player index (-1 to cancel): "))
			assert -1 <= position < len(game.players)
			break
		except Exception:
			print(f"Enter a number between -1 and {len(game.players) - 1}.")

	# Return choice
	return position

def input_valid_player_index(query_target: QueryTarget, game: "GameController"):
	# Input validated choice
	while True:
		# Input player index
		game.display_alive_players(query_target.alliance != TargetAlliance.enemy)
		player_index = input_player_index(game)
		if player_index == -1:
			return -1

		# Validate player alive
		assert game.players[player_index].get_health() > 0

		# Validate player alliance
		player = game.players[player_index]
		try:
			query_target.check_players_valid(game.turn_get_player(), player)
			break
		except Exception as e:
			print(f"Player selection error: {e}")

	# Return index
	return player_index

def input_any_minion(query_target: QueryTarget, game: "GameController"):
	# Input valid player index
	player_index = input_valid_player_index(query_target, game)
	if player_index == -1:
		return

	# Input player minion
	player = game.players[player_index]
	player.display_battlefield()
	minion_index = input_minion_battlefield_position(player)
	if minion_index == -1:
		return

	# Return minion character
	return player.battlefield.characters[minion_index]

def input_hero(query_target: QueryTarget, game: "GameController"):
	# Input valid player index
	player_index = input_valid_player_index(query_target, game)
	if player_index == -1:
		return

	# Return hero
	player = game.players[player_index]
	return player.hero
