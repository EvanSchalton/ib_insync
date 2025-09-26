#!/usr/bin/env python3
"""Test the new model-based parsing approach directly."""

# Import just what we need to test the concept
from decimal import Decimal
from typing import ClassVar

from ib_insync.parseable_model import ParseableModel
from ib_insync.decoders.parsers.field_parser import FieldIterator


# Create a simple test model to demonstrate the concept
class TestContract(ParseableModel):
    """Simple test contract model."""

    _parser_fields: ClassVar[tuple[str, ...]] = (
        'contract_id',
        'symbol',
        'security_type',
        'strike',
        'exchange',
        'currency',
    )

    contract_id: int = 0
    symbol: str | None = None
    security_type: str | None = None
    strike: Decimal = Decimal("0")
    exchange: str | None = None
    currency: str | None = None


def test_simple_parsing():
    """Test the simplified parsing approach."""
    print("Testing Simple Parsing Approach")
    print("=" * 50)

    # Sample field data
    fields = [
        "12345",     # contract_id
        "AAPL",      # symbol
        "STK",       # security_type
        "150.50",    # strike
        "SMART",     # exchange
        "USD",       # currency
    ]

    iterator = FieldIterator(fields)
    contract = TestContract.parse(iterator)

    print(f"✓ Parsed contract: {contract}")
    print(f"  Contract ID: {contract.contract_id} (type: {type(contract.contract_id)})")
    print(f"  Symbol: {contract.symbol} (type: {type(contract.symbol)})")
    print(f"  Security Type: {contract.security_type} (type: {type(contract.security_type)})")
    print(f"  Strike: {contract.strike} (type: {type(contract.strike)})")
    print(f"  Exchange: {contract.exchange} (type: {type(contract.exchange)})")
    print(f"  Currency: {contract.currency} (type: {type(contract.currency)})")

    # Verify types were properly converted by Pydantic
    assert contract.contract_id == 12345
    assert isinstance(contract.contract_id, int)
    assert contract.symbol == "AAPL"
    assert isinstance(contract.symbol, str)
    assert contract.strike == Decimal("150.50")
    assert isinstance(contract.strike, Decimal)

    print("\n" + "=" * 50)
    print("✅ SUCCESS: Simplified parsing approach works!")
    print("\nKey benefits:")
    print("  • Simple tuple of field names (no type annotations needed)")
    print("  • Pydantic handles all type conversion automatically")
    print("  • Configuration is centralized in the model class")
    print("  • Parsing logic is declarative and maintainable")
    print("  • No more standalone parsing functions")
    print("\nExample usage:")
    print("  class MyModel(ParseableModel):")
    print("      _parser_fields = ('field1', 'field2', 'field3')")
    print("      field1: int")
    print("      field2: str")
    print("      field3: Decimal")
    print("")
    print("  # Parse from IB field data")
    print("  model = MyModel.parse(field_iterator)")


if __name__ == "__main__":
    test_simple_parsing()
