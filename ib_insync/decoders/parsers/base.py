"""Base classes for parseable models."""

from decimal import Decimal
from typing import Any, ClassVar

from ...parseable_model import ParseableModel


class VersionedParseableModel(ParseableModel):
    """
    Base class for models that have version-dependent parsing.

    Subclasses can define _version_fields mapping server versions to additional field tuples.
    """

    _version_fields: ClassVar[dict[int, tuple[str, ...]]] = {}

    @classmethod
    def parse(cls, field_iterator, server_version: int = 0):
        """
        Parse with version-specific field handling.

        Args:
            field_iterator: FieldIterator positioned at the start of this model's data
            server_version: Server version for compatibility

        Returns:
            Instance of this model
        """
        data: dict[str, Any] = {}

        # Parse base fields
        for field_name in cls._parser_fields:
            value = field_iterator.next()
            data[field_name] = value

        # Parse version-specific fields
        for version, version_fields in cls._version_fields.items():
            if server_version >= version:
                for field_name in version_fields:
                    value = field_iterator.next()
                    data[field_name] = value

        return cls.model_validate(data)
