"""SoftDollarTier dataclass."""

from dataclasses import dataclass


@dataclass
class SoftDollarTier:
    name: str = ''
    val: str = ''
    displayName: str = ''

    def __bool__(self):
        return bool(self.name or self.val or self.displayName)
