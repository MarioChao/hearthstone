import game_controller
from aesthetics import horizontal_rule, input_to_continue
from game_loop import game_single_player, game_multiple_players_1v1

'''
TODO (v1):
- Player actions:
	[x] play
	[x] attack
- Cards:
	[x] Chillwind Yeti
	[x] Bloodfen Raptor
	[x] Boulderfist Ogre
	[x] Fireball
	[x] Polymorph
- [x] Starter cards (3, 4, ...)
- [x] Turn based (multiple players)
- [x] Health point tracking
- [x] Fatigue damage (empty deck)
- [x] Overdraw
- [x] Victory conditions (only one player alive)
- [x] Max 7 minions on a player's battlefield
- [x] Max 10 mana crystals
- [x] Hand logs
'''

'''
TODO (v2):
- Player actions:
	[ ] hero power
- Cards:
	[x] Flamestrike
	[x] Arcane Intellect
	[x] Holy Nova
	[x] Cataclysm
	[x] Deadly Shot
	[ ] Stormwind Champion
	[ ] Booty Bay Bodyguard
	[ ] Wolfrider
	[ ] Spymistress
- [ ] Card / character effects
'''

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
