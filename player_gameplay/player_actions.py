"""Handles action inputs during a player's turn"""

from aesthetics import horizontal_rule
from cards.card_minion import MinionCard
from cards.card_spell import SpellCard
from game_controller import GameController
from player_gameplay.player_input import input_card_choice, input_empty_battlefield_position, input_minion_battlefield_position
from target.target_get import get_targets_input
from target.query_target import QueryTarget, TargetAlliance, TargetCharacterType, TargetChooseMethod

# Variables

action_list = [
	"h",
	"field", "fd",
	"hand", "hd",
	"play",
	"attack", "atk",
	"hero power",
	"e", "end", "concede",
]

attack_query_target = QueryTarget(
	TargetAlliance.enemy, TargetCharacterType.any_character,
	(1, 1), TargetChooseMethod.user_input,
	respect_taunt=True,
	respect_stealth=True
)

# Functions

def input_action():
	action = input("Enter action ('h' for help): ")
	return action

def process_action(action: str, game: GameController):
	match action:
		case "h":
			horizontal_rule()
			print("Actions:")
			print(f"\t{action_list}")
			return True
		case "field never":
			game.display_battlefields(False)
			return True
		case "field" | "fd":
			game.display_battlefields(True)
			return True
		case "hand never" :
			game.turn_display_hand(False)
			return True
		case "hand" | "hd":
			game.turn_display_hand(True)
			return True
		case "play":
			# Get player
			player = game.turn_get_player()

			# Display hand
			game.turn_display_hand(True)

			# Select card to play
			card_choice = input_card_choice(player)

			# Check cancellation
			if card_choice == -1:
				return

			# Get card
			card = player.hand.cards[card_choice]

			# Check if card can be played
			if not player.can_play_card(card):
				print("Can't play card!")
				return True

			# Play card
			if isinstance(card, MinionCard):
				# Display player battlefield
				player.display_battlefield(True)

				# Input position to play minion
				position = input_empty_battlefield_position(player)

				# Check cancellation
				if position == -1:
					return

				# Play card
				success = game.turn_play_minion_card_at(card_choice, position)

				# Print success
				if success:
					print(f"Played [{card.name}] minion at battlefield position {position}.")

			elif isinstance(card, SpellCard):
				# Play card
				success = game.turn_play_spell_card(card_choice)

				# Print success
				if success:
					print(f"Played [{card.name}] spell.")

			return True
		case "attack" | "atk":
			# Get player
			player = game.turn_get_player()

			# Display player battlefield
			player.display_battlefield(True)

			# Input player's minion to attack
			minion_position = input_minion_battlefield_position(player)

			# Check cancellation
			if minion_position == -1:
				return

			# Check if minion can attack
			minion = player.battlefield.characters[minion_position]
			if minion.moves_left <= 0:
				print(f"Minion has no moves remaining!")
				return True

			# Input target to attack
			game.display_heroes()
			print("Enter attack target!")
			targets = get_targets_input(attack_query_target, game)
			if not targets:
				print("Target is empty.")
				return True

			# Attack
			target = targets[0]
			game.attack(minion, target)

			# Print message
			print(f"[{minion.name}] attacks {target.commander.name}'s [{target.name}].")

			return True
		case "hero power":
			print("Not implemented")
			return
		case "e" | "end":
			pass
		case "concede":
			# Kill player
			game.concede()
			pass

	return
