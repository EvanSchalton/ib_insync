"""Base class for parseable models."""

from abc import ABC
from typing import Any, ClassVar

from pydantic import BaseModel


class ParseableModel(BaseModel, ABC):
    """
    Base class for IB API models with automatic parsing and hashing.

    Features:
    - Automatic parsing from _parser_fields tuple
    - Automatic hashing based on _parser_fields
    - Support for parsing multiple instances

    Note: Pydantic handles all type conversions (enum, Decimal, int, etc.) automatically.
    No custom validators needed for standard type conversions.
    """

    _parser_fields: ClassVar[tuple[str, ...]] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not cls._parser_fields:
            raise NotImplementedError(
                f"{cls.__name__} must define _parser_fields")

    @classmethod
    def parse(cls, field_iterator):
        """
        Parse an instance from a FieldIterator.

        Args:
            field_iterator: FieldIterator positioned at the start of this model's data

        Returns:
            Instance of this model
        """
        data: dict[str, Any] = {}
        for field_name in cls._parser_fields:
            value = field_iterator.next()
            data[field_name] = value

        return cls.model_validate(data)

    @classmethod
    def parse_many(cls, field_iterator, count: int):
        """
        Parse multiple instances from a FieldIterator.

        Args:
            field_iterator: FieldIterator positioned at the start
            count: Number of instances to parse

        Returns:
            List of model instances
        """
        return [cls.parse(field_iterator) for _ in range(count)]

    def __hash__(self) -> int:
        """
        Hash based on parser fields for consistent object identity.

        This enables using these models as dictionary keys and in sets.
        """
        values = tuple(getattr(self, field) for field in self._parser_fields)
        return hash(values)

    def __eq__(self, other) -> bool:
        """Equality based on parser fields."""
        if not isinstance(other, self.__class__):
            return False
        return hash(self) == hash(other)