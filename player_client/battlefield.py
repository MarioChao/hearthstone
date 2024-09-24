from typing import TYPE_CHECKING

from character.character_class import Character, CharacterType

if TYPE_CHECKING:
	from cards.card_minion import MinionCard
	from player_client.player import Player

# Battlefield class

class Battlefield:
	def __init__(self, player: "Player"):
		self.commander = player
		self.characters = []
		for _ in range(7):
			self.characters.append(Character(player))

	def add_minion_at(self, minion: "MinionCard", position: int):
		# Validate position
		if not 0 <= position < len(self.characters):
			print("Not a battlefield position!")
			return

		# Validate no character
		if self.characters[position].character_type != CharacterType.none:
			print("Not an empty character!")
			return

		# Play minion card
		self.characters[position].set_as_minion(minion)

	def has_taunt(self):
		# Check if any character has "taunt" effect
		for character in self.characters:
			if character.has_active_taunt():
				return True
		return False

	# Display

	def get_display(self, is_detailed=False):
		# Get list of character names
		result_list = []
		for character in self.characters:
			character_name = character.get_display(is_detailed)
			result_list.append(f"[{character_name}]")

		# Format the list (newline for detailed view)
		if is_detailed:
			result_str = "\n".join(f"\t{i:2}: {result_list[i]}" for i in range(len(result_list)))
		else:
			result_str = ", ".join(f"\t{i:2}: {result_list[i]}" for i in range(len(result_list)))

		return result_str
