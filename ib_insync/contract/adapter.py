"""Contract adapter for polymorphic contract creation."""

from typing import Annotated, Any

from pydantic import Field, TypeAdapter, ValidationError

from .base import Contract
from .specialized import (
    CFD,
    Bag,
    Bond,
    Commodity,
    ContFuture,
    Crypto,
    Forex,
    Future,
    FuturesOption,
    Index,
    MutualFund,
    Option,
    Stock,
    Warrant,
)

# Create discriminated union for specialized contract types
# Each specialized class has Literal[SecurityType.X] for security_type
SpecializedContractUnion = Annotated[
    Stock | Option | Future | ContFuture | Forex | Index | CFD | Bond | Commodity | FuturesOption | MutualFund | Warrant | Bag | Crypto,
    Field(discriminator='security_type')
]

class ContractAdapter:
    """
    Adapter for creating the correct contract type based on security_type.

    Uses Pydantic's native discriminated union support for efficient
    polymorphic contract creation.
    """

    # TypeAdapter for the discriminated union
    _type_adapter = TypeAdapter(SpecializedContractUnion)

    @classmethod
    def parse(cls, data: dict[str, Any]) -> Contract:
        """
        Parse a dictionary into the appropriate Contract subclass.

        Uses Pydantic's discriminated union to automatically select
        the correct contract type based on the security_type field.
        Falls back to base Contract for unknown types.

        Args:
            data: Dictionary with contract data

        Returns:
            Appropriate Contract subclass instance based on security_type
        """
        try:
            # Try to parse as a specialized contract using discriminated union
            # This is efficient - Pydantic uses the discriminator to pick the right type
            return cls._type_adapter.validate_python(data)
        except ValidationError:
            # If no specialized type matches (unknown security_type),
            # fall back to base Contract class
            return Contract.model_validate(data)

    @classmethod
    def parse_many(cls, data_list: list[dict[str, Any]]) -> list[Contract]:
        """
        Parse a list of dictionaries into Contract objects.

        Args:
            data_list: List of dictionaries with contract data

        Returns:
            List of appropriate Contract subclass instances
        """
        return [cls.parse(data) for data in data_list]



# Export the main components
__all__ = ['ContractAdapter', 'SpecializedContractUnion']
