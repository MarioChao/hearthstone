from typing import TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
	from cards.card_minion import MinionCard
	from client.player import Player

# Enum

class CharacterType(Enum):
	none = "none",
	minion = "minion",
	hero = "hero",

# Character class

class Character:
	def __init__(self, player: "Player"):
		self.character_type = CharacterType.none
		self.commander = player
		self.name = ""
		self.description = ""
		self.max_health = 0
		self.health = 0
		self.attack = 0
		self.defense = 0
		self.moves_left = 0
		self.effects = set()

	def set_as_minion(self, minion: "MinionCard"):
		self.character_type = CharacterType.minion
		self.name = minion.name
		self.description = minion.description
		self.max_health = minion.health
		self.health = minion.health
		self.attack = minion.attack
		self.defense = 0
		self.effects = minion.effects

	def set_as_hero(self, health: int):
		self.character_type = CharacterType.hero
		self.name = self.commander.name
		self.description = "A hero"
		self.max_health = health
		self.health = health
		self.attack = 0
		self.defense = 0

	def reset_moves(self):
		if self.character_type == CharacterType.minion:
			self.moves_left = 1
		else:
			self.moves_left = 0

	def get_attack(self):
		return self.attack

	# Health functions

	def change_max_health(self, change_by: int):
		self.max_health += change_by
		if change_by > 0:
			# Increment current health
			self.health += change_by
		else:
			# Clamp the current health
			self.health = min(self.max_health, self.health)

	def restore_health(self, restore_by: int):
		assert restore_by >= 0

		# Restore health, capping at maximum health
		self.health += restore_by
		self.health = min(self.max_health, self.health)

		# Save logs
		self.commander.game.save_log(
			f"<{self.commander.name}>'s"
			f" character [{self.name}]"
			f" restored to {self.health} health."
		)

	def receive_damage(self, damage: int):
		assert damage >= 0

		# Reduce health
		self.health -= damage

		# Save logs
		self.commander.game.save_log(
			f"<{self.commander.name}>'s"
			f" character [{self.name}]"
			f" received {damage} damage,"
			f" {self.health} health remaining."
		)

		# Death at non-positive health
		if self.health <= 0:
			self.on_destruction()

	def set_health(self, health: int):
		self.health = health

		if self.health <= 0:
			self.on_destruction()

	def destroy(self):
		self.set_health(0)

	# Destruction functions

	def on_destruction(self):
		assert self.health <= 0

		# Save logs
		self.commander.game.save_log(
			f"<{self.commander.name}>'s"
			f" character [{self.name}]"
			f" was destroyed."
		)

		self.character_type = CharacterType.none

		# TODO: Death effects

	# Display functions

	def get_display(self, is_detailed=False):
		result_str = ""
		if self.character_type != CharacterType.none:
			result_str = (
				f"{self.name:>20}"
				f" | Attack: {self.attack:<4} | Health: {self.health:<4} | Defense: {self.defense:<4}"
			)
			if is_detailed:
				result_str += f" | {self.description}"
		return result_str
