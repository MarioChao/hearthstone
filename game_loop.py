"""Defines the gameplay loop"""

from copy import deepcopy

import game_controller
from player_gameplay import player_actions
from aesthetics import horizontal_rule, input_to_continue
from cards.card_storage import spell_cards, minion_cards
from player_client.deck import Deck
from player_client.player import Player

# Variables

default_deck_cards = list(minion_cards.values()) + list(spell_cards.values())
default_deck_cards *= 2

# Helper functions

def create_player(deck: Deck, name_prompt="Player name: "):
	player_name = input(name_prompt)
	player = Player(player_name, deepcopy(deck))
	return player

# Local functions

def general_game_loop(game_players: list[Player]):
	# Create new game instance
	game = game_controller.GameController(game_players)

	# Start game
	game.start_game()

	# Round variables
	previous_round = 0

	# Game loop phase
	while not game.is_game_ended():
		print()

		# Display round if new
		if previous_round != game.round_number:
			# Update & display round
			previous_round = game.round_number
			game.turn_display_round()

			# Save logs
			game.save_log(f"New round: round {game.round_number}.")

		# Horizontal rule
		horizontal_rule(50)

		# Start turn
		game.start_turn()

		# Display player
		game.turn_display_player()

		# Draw a card for the player
		game.turn_draw_card()

		# Input player actions
		while True:
			# Game ended check
			if game.is_game_ended():
				break

			# Aesthetics
			horizontal_rule()
			horizontal_rule()

			# Show the battlefield
			game.display_battlefields(False)

			# Show the heroes
			print()
			game.display_heroes()

			horizontal_rule(10)

			# Input action
			while True:
				action = player_actions.input_action()
				if action in player_actions.action_list:
					break

			# Process action
			action_result = player_actions.process_action(action, game)

			# Resolve death
			game.resolve_deaths()

			# Break actions
			if action in ("e", "end", "concede"):
				break

			# Wait for 'enter'
			if action_result:
				input_to_continue()

		# End turn
		game.end_turn()

	# End game
	game.end_game()

	# Return game
	return game

def game_single_player():
	# Create players
	player_1 = create_player(Deck(default_deck_cards))
	player_bot = Player("npc", Deck(default_deck_cards))
	game_players = [player_1, player_bot]

	# ...
	return general_game_loop(game_players)

def game_multiple_players_1v1():
	# Start message
	horizontal_rule()
	print("Welcome to Multiple Players 1v1!")
	print()
	print("First, tell us the number of players! (>= 2)")
	print("# of players:")

	# Input player count
	while True:
		try:
			player_count = int(input("> "))
			assert player_count >= 2
			break
		except Exception:
			print("Enter a number >= 2.")

	# Player names message
	print()
	print("Now, enter the names for each player.")

	# Create players
	game_players = []
	for i in range(player_count):
		player_object = create_player(Deck(default_deck_cards), f"Player {i + 1} name: ")
		game_players.append(player_object)

	# Start game message
	print()
	print("Alright!")
	print(f"By continuing on, you will start the Hearthstone game for {player_count} players!")
	input_to_continue()

	# Game loop
	return general_game_loop(game_players)