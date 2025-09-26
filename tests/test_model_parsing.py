#!/usr/bin/env python3
"""Test the new model-based parsing approach."""

import sys

sys.path.insert(0, 'ib_insync')

from ib_insync.contract.base import ComboLeg, Contract, DeltaNeutralContract
from ib_insync.contract.enums import Currency, Exchange, SecurityType
from ib_insync.decoders.parsers.field_parser import FieldIterator


def test_contract_parsing():
    """Test Contract parsing with the new approach."""
    print("Testing Contract parsing...")

    # Sample field data for a contract (order matches _parser_fields)
    fields = [
        "12345",     # contract_id
        "AAPL",      # symbol
        "STK",       # security_type
        "",          # last_trade_date_or_contract_month
        "0.0",       # strike
        "",          # option_type
        "",          # multiplier
        "SMART",     # exchange
        "USD",       # currency
        "AAPL",      # local_symbol
        "NMS"        # trading_class
    ]

    iterator = FieldIterator(fields)
    contract = Contract.parse(iterator)

    print(f"✓ Parsed contract: {contract}")
    print(f"  Contract ID: {contract.contract_id}")
    print(f"  Symbol: {contract.symbol}")
    print(f"  Security Type: {contract.security_type}")
    print(f"  Exchange: {contract.exchange}")
    print(f"  Currency: {contract.currency}")

    assert contract.contract_id == 12345
    assert contract.symbol == "AAPL"
    assert contract.security_type == SecurityType.STOCK
    assert contract.exchange == Exchange.SMART
    assert contract.currency == Currency.USD


def test_combo_leg_parsing():
    """Test ComboLeg parsing."""
    print("\nTesting ComboLeg parsing...")

    # Sample field data for a combo leg
    fields = [
        "12345",  # contract_id
        "1",      # ratio
        "BUY",    # action
        "SMART",  # exchange
        "0",      # open_close
        "0",      # short_sale_slot
        "",       # designated_location
        "-1"      # exempt_code
    ]

    iterator = FieldIterator(fields)
    leg = ComboLeg.parse(iterator)

    print(f"✓ Parsed combo leg: {leg}")
    print(f"  Contract ID: {leg.contract_id}")
    print(f"  Ratio: {leg.ratio}")
    print(f"  Action: {leg.action}")

    assert leg.contract_id == 12345
    assert leg.ratio == 1
    assert leg.action.value == "BUY"


def test_multiple_combo_legs():
    """Test parsing multiple ComboLegs."""
    print("\nTesting multiple ComboLeg parsing...")

    # Sample field data for 2 combo legs
    fields = [
        # First leg
        "12345", "1", "BUY", "SMART", "0", "0", "", "-1",
        # Second leg
        "67890", "2", "SELL", "NASDAQ", "1", "0", "", "-1"
    ]

    iterator = FieldIterator(fields)
    legs = ComboLeg.parse_many(iterator, 2)

    print(f"✓ Parsed {len(legs)} combo legs")
    assert len(legs) == 2
    assert legs[0].contract_id == 12345
    assert legs[1].contract_id == 67890
    assert legs[0].action.value == "BUY"
    assert legs[1].action.value == "SELL"


def test_delta_neutral_contract():
    """Test DeltaNeutralContract parsing."""
    print("\nTesting DeltaNeutralContract parsing...")

    # Sample field data for delta neutral contract
    fields = [
        "12345",  # contract_id
        "0.5",    # delta
        "100.25"  # price
    ]

    iterator = FieldIterator(fields)
    dnc = DeltaNeutralContract.parse(iterator)

    print(f"✓ Parsed delta neutral contract: {dnc}")
    print(f"  Contract ID: {dnc.contract_id}")
    print(f"  Delta: {dnc.delta}")
    print(f"  Price: {dnc.price}")

    assert dnc.contract_id == 12345
    assert float(dnc.delta) == 0.5
    assert float(dnc.price) == 100.25


if __name__ == "__main__":
    print("Testing Model-Based Parsing")
    print("=" * 50)

    try:
        test_contract_parsing()
        test_combo_leg_parsing()
        test_multiple_combo_legs()
        test_delta_neutral_contract()

        print("\n" + "=" * 50)
        print("✓ All model-based parsing tests passed!")
        print("Benefits of this approach:")
        print("  • Configuration is centralized in the model class")
        print("  • Parsing logic is declarative and type-safe")
        print("  • Easy to maintain and extend")
        print("  • Eliminates standalone parsing functions")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise
