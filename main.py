"""Defines the program's starting logic"""

import game_controller
from aesthetics import horizontal_rule, input_to_continue
from game_loop import game_single_player, game_multiple_players_1v1

# Functions

def main_game():
	horizontal_rule(100)

	# Show cards
	game_controller.display_cards()

	# Game loop
	while True:
		horizontal_rule(100)

		# Show game modes
		print(
			"Game modes:\n"
			"1 - Single player (not available)\n"
			"2 - Multiple players 1v1"
		)

		# Select game mode
		while True:
			game_mode = input("Select a game mode (1 or 2): ")

			# Validate game mode
			if game_mode in ("1", "2"):
				break

		# Play game
		game = None
		if game_mode == "1":
			game = game_single_player()
		elif game_mode == "2":
			game = game_multiple_players_1v1()

		# Get game info
		winner = game.get_winner()
		game_logs = game.game_logs

		# End game
		horizontal_rule()
		print("Game ended!")
		if winner:
			print(f"<{winner}> won! Congratulations!")
		else:
			print(f"No one won!")

		# Wait until 'enter'
		input_to_continue()
		print("The game logs will follow next.")
		input_to_continue()

		# Print logs
		print("\n".join(game_logs))

		# Wait until 'enter'
		input_to_continue()

		# Continue game?
		while True:
			continue_game = input("Continue playing? (y/n): ")

			# Validate input
			if not continue_game in ("y", "n"):
				continue
			else:
				break
		if continue_game == "n":
			break

	print("Goodbye!")

if __name__ == "__main__":
	main_game()
