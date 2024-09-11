import random

from aesthetics import horizontal_rule
from cards.card_minion import MinionCard
from cards.card_spell import SpellCard
from cards.card_storage import minion_cards, spell_cards
from character.character_class import Character
from client.player import Player

# Functions

def display_cards():
	print(f"{" Implemented cards ":-^50}")

	print(f"Minion cards ({len(minion_cards)}):")
	for card_name, card in minion_cards.items():
		print(f"\t{f"[{card_name}]":20} {card}")

	print(f"Spell cards ({len(spell_cards)}):")
	for card_name, card in spell_cards.items():
		print(f"\t{f"[{card_name}]":20} {card}")

def attacker_can_attack(attacker: Character):
	return attacker.moves_left > 0 and attacker.health > 0

def reset_minion_moves(player: Player):
	for character in player.battlefield.characters:
		character.reset_moves()

# Game instance class

class GameController:
	def __init__(self, players: list[Player]):
		self.players = players
		self.round_number = 0
		self.player_turn = 0
		self.game_logs: list[str] = []

	# General functions

	def shuffle_players(self):
		random.shuffle(self.players)

	def display_battlefields(self, is_detailed: bool):
		for player_index in range(len(self.players)):
			player = self.players[player_index]
			print(f"{player_index:2}. Battlefield for <{player.name}>:")
			player.display_battlefield(is_detailed)

	def display_players(self):
		for player_index in range(len(self.players)):
			player = self.players[player_index]
			print(f"{player_index:2}. <{player.name}>:")

	def display_alive_players(self, include_turn_player=True):
		for player_index in range(len(self.players)):
			player = self.players[player_index]
			if player.get_health() > 0 and (include_turn_player or player != self.turn_get_player()):
				print(f"{player_index:2}. <{player.name}>:")

	def display_heroes(self):
		for player_index in range(len(self.players)):
			player = self.players[player_index]
			turn_prefix = (">>>" if player == self.turn_get_player()
						   else "  -" if player.get_health() > 0
						   else "   ")
			print(f"{turn_prefix:2}\tHero:\t{player}")

	def get_player_by_index(self, index: int) -> Player | None:
		if not 0 <= index < len(self.players):
			return
		return self.players[index]

	# Start functions

	def start_game(self):
		self.save_log("Starting new game.")

		# Set game for each player
		for player in self.players:
			player.set_game(self)

		# Shuffle players
		self.shuffle_players()

		# Shuffle player cards
		for player in self.players:
			player.deck.shuffle_cards()

		# Draw 3 cards for first player
		for _ in range(3):
			self.players[0].draw_card()

		# Draw 4 cards for other players
		for i in range(1, len(self.players)):
			for _ in range(4):
				self.players[i].draw_card()

		# Start round 1
		self.round_number = 0
		self.__next_round()

	# Turn / round functions

	def start_turn(self):
		player = self.turn_get_player()
		self.__reset_mana(player)

	def turn_get_player(self):
		return self.players[self.player_turn]

	# Turn display

	def turn_display_round(self):
		horizontal_rule(75)
		print(f"{f"Round {self.round_number}":-^75}")
		horizontal_rule(75)

	def turn_display_player(self):
		player = self.turn_get_player()
		print(f"{f"{player.name}'s turn":^30}")

	def turn_display_hand(self, is_detailed: bool):
		player = self.turn_get_player()
		print("Hand:")
		player.display_hand(is_detailed)

	def turn_display_hero(self):
		player = self.turn_get_player()
		print(f"Hero:\t{player}")

	# Turn draw

	def turn_draw_card(self):
		player = self.turn_get_player()
		card = player.draw_card(True)
		return card

	# Turn play

	def turn_play_minion_card_at(self, card_index: int, position: int):
		player = self.turn_get_player()

		# Validate card index
		if not 0 <= card_index < len(player.hand.cards):
			print("Not a Hand card!")
			return

		# Get card
		card = player.hand.cards[card_index]

		# Validate card type
		if not isinstance(card, MinionCard):
			print("Not a Minion card!")
			return

		# Check card playable
		if not player.can_play_card(card):
			print("Can't play card!")
			return

		# Play card
		success = player.play_minion_card(card, position)

		return success

	def turn_play_spell_card(self, card_index: int):
		player = self.turn_get_player()

		# Validate card index
		if not 0 <= card_index < len(player.hand.cards):
			return

		# Get card
		card = player.hand.cards[card_index]

		# Validate card type
		if not isinstance(card, SpellCard):
			return

		# Play card
		success = player.play_spell_card(card)

		return success

	# Turn attack

	def attack(self, attacker: Character, target: Character):
		player = self.turn_get_player()

		# Validate commander
		if attacker.commander != player:
			return

		# Check if the attacker can attack
		if not attacker_can_attack(attacker):
			return

		# Save logs
		self.save_log(
			f"<{attacker.commander.name}>'s"
			f" character [{attacker.name}]"
			f" attacked <{target.commander.name}>'s"
			f" character [{target.name}]."
		)

		# Attack
		target.receive_damage(attacker.get_attack())
		attacker.receive_damage(target.get_attack())

		# Reduce moves
		attacker.moves_left -= 1

	# End turn

	def end_turn(self):
		# Reset minion moves
		player = self.turn_get_player()
		reset_minion_moves(player)

		# Save logs
		self.save_log(f"Ended turn for <{player.name}>.")

		# Get next player
		is_looped = False
		for i in range(len(self.players)):
			# Increment player turn
			self.player_turn += 1

			# Check looped
			if self.player_turn >= len(self.players):
				self.player_turn = 0
				is_looped = True

			# Check alive
			if self.players[self.player_turn].get_health() > 0:
				break

		# New round if looped
		if is_looped:
			self.__next_round()

	def __next_round(self):
		# Increment round number
		self.round_number += 1

	# Reset functions

	def __reset_mana(self, player: Player):
		if player.get_health() >= 0:
			player.set_max_mana_crystal(min(10, self.round_number))
			player.reset_mana()

	# Concede

	def concede(self):
		player = self.turn_get_player()
		player.concede()

	# Game end functions

	def is_game_ended(self):
		# Count alive players
		alive_count = 0
		for player in self.players:
			if player.get_health() > 0:
				alive_count += 1

		# Game ends when there's one or no player alive
		return alive_count <= 1

	def get_winner(self):
		# Validate game ended
		if not self.is_game_ended():
			return False

		# Return winner
		for player in self.players:
			if player.get_health() > 0:
				return player.name
		return None

	# Log functions

	def save_log(self, log: str):
		self.game_logs.append(log)
