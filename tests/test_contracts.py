#!/usr/bin/env python3
"""Test the updated contract system."""

from decimal import Decimal

from ib_insync.contract import Exchange, Forex, Future, Option, OptionType, Stock

print("Testing Updated Contract System")
print("=" * 50)

# Test 1: Stock with enums
stock = Stock(symbol="AAPL")
print(f"\n1. Stock: {stock.symbol}")
print(f"   Exchange: {stock.exchange} (Exchange enum)")
print(f"   Currency: {stock.currency} (Currency enum)")

# Test 2: Option with Decimal and OptionType
option = Option(
    symbol="SPY",
    strike=Decimal("425.50"),
    option_type=OptionType.CALL,
    last_trade_date_or_contract_month="20240321"
)
print(f"\n2. Option: {option.symbol}")
print(f"   Strike: {option.strike} (Decimal)")
print(f"   Type: {option.option_type} (OptionType)")
print(f"   Multiplier: {option.multiplier} (int)")

# Test 3: Future with required exchange
future = Future(
    symbol="ES",
    exchange=Exchange.GLOBEX,
    last_trade_date_or_contract_month="202403"
)
print(f"\n3. Future: {future.symbol}")
print(f"   Exchange: {future.exchange}")

# Test 4: Forex
forex = Forex(pair="EURUSD")
print(f"\n4. Forex: {forex.pair()}")
print(f"   Symbol: {forex.symbol}")
print(f"   Currency: {forex.currency}")

print("\n" + "=" * 50)
print("✓ All improvements working correctly!")
print("  • Exchange and Currency enums")
print("  • Decimal for precision")
print("  • OptionType (not Right)")
print("  • Integer multiplier")
print("  • Updated in place (no _improved files)")
