"""Defines the enum type for character effects"""

from enum import Enum

# Enums

class CharacterEffectType(Enum):
	aura = "aura / ongoing",
	taunt = "taunt",
	charge = "charge",
	stealth = "stealth",
	silence = "silence",
	invisible = "invisible",
	death_rattle = "death rattle",
