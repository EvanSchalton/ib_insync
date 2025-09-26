"""TickAttrib dataclass."""

from dataclasses import dataclass


@dataclass
class TickAttrib:
    canAutoExecute: bool = False
    pastLimit: bool = False
    preOpen: bool = False
