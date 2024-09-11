class Card:
	def __init__(self, name: str, mana_cost: int, description: str):
		self.name = name
		self.mana_cost = mana_cost
		self.description = description

	def play(self, *args, **kwargs):
		pass

	def __str__(self):
		return f"{self.name:>20} | Mana cost: {self.mana_cost:<2} | {self.description}"
