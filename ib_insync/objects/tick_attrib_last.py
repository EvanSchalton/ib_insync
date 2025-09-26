"""TickAttribLast dataclass."""

from dataclasses import dataclass


@dataclass
class TickAttribLast:
    pastLimit: bool = False
    unreported: bool = False
