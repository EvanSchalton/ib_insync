"""
Pydantic-based decoder architecture for IB protocol messages.

This package provides a modern, type-safe approach to handling
Interactive Brokers protocol messages using Pydantic for validation
and serialization.
"""

from ib_insync.decoders.base import IBMessage, MessageHandler, MessageRegistry, registry
from ib_insync.decoders.dispatcher import AsyncMessageDispatcher, MessageDispatcher
from ib_insync.decoders.handlers import (
    accounts as accounts_handlers,
)
from ib_insync.decoders.handlers import (
    contracts as contracts_handlers,
)
from ib_insync.decoders.handlers import (
    historical as historical_handlers,
)

# Import ALL handlers to register them
from ib_insync.decoders.handlers import (
    market_data as market_data_handlers,
)
from ib_insync.decoders.handlers import (
    misc as misc_handlers,
)
from ib_insync.decoders.handlers import (
    orders as orders_handlers,
)

# Import ALL models to register them with the registry
from ib_insync.decoders.models import (
    accounts,
    contracts,
    historical,
    market_data,
    misc,
    orders,
)
from ib_insync.decoders.parsers.field_parser import FieldIterator, FieldParser
from ib_insync.decoders.parsers.validators import IBValidators

# Create a global dispatcher instance for easy access
from ib_insync.wrapper import Wrapper


def create_dispatcher(wrapper: Wrapper, server_version: int = 0) -> MessageDispatcher:
    """
    Create a message dispatcher for the given wrapper.

    Args:
        wrapper: The IB wrapper instance
        server_version: Server version for compatibility

    Returns:
        Configured MessageDispatcher instance
    """
    return MessageDispatcher(wrapper, registry, server_version)

__all__ = [
    # Base classes
    'IBMessage',
    'MessageHandler',
    'MessageRegistry',
    'registry',
    # Dispatcher
    'MessageDispatcher',
    'AsyncMessageDispatcher',
    'create_dispatcher',
    # Parsers
    'FieldIterator',
    'FieldParser',
    'IBValidators',
]
