"""Base classes and registry for the Pydantic-based decoder architecture."""

import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, ClassVar, TypeVar

from pydantic import BaseModel, ConfigDict


class IBMessage(BaseModel):
    """
    Base class for all IB protocol messages with custom serialization.

    This provides common functionality for parsing IB's wire format
    and converting to/from the null-terminated field format.
    """

    model_config = ConfigDict(
        # Allow extra fields for forward compatibility
        extra='allow',
        # Validate on assignment for safety
        validate_assignment=True,
        # Use enum values directly
        use_enum_values=True,
        # Allow arbitrary types (for Contract, Order, etc.)
        arbitrary_types_allowed=True,
    )

    # Message ID for this message type (set by subclasses)
    MESSAGE_ID: ClassVar[int | None] = None

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'IBMessage':
        """
        Parse a message from IB wire format fields.

        Args:
            fields: List of string fields from IB protocol
            server_version: Server version for compatibility handling

        Returns:
            Parsed and validated message instance
        """
        # Subclasses should override this with their specific parsing logic
        raise NotImplementedError(
            f"{cls.__name__} must implement from_fields method"
        )

    def to_fields(self) -> list[str]:
        """
        Serialize the message to IB wire format fields.

        Returns:
            List of string fields for IB protocol
        """
        # Default implementation - subclasses can override
        fields = []
        if self.MESSAGE_ID is not None:
            fields.append(str(self.MESSAGE_ID))

        # Add other fields based on model
        for field_name in self.model_fields:
            field_value = getattr(self, field_name, None)
            if field_value is None:
                fields.append('')
            elif isinstance(field_value, bool):
                fields.append('1' if field_value else '0')
            elif isinstance(field_value, (int, float)):
                fields.append(str(field_value))
            else:
                fields.append(str(field_value))

        return fields

    def to_wire_format(self) -> str:
        """
        Convert to IB's null-terminated wire format.

        Returns:
            Null-terminated string ready for transmission
        """
        fields = self.to_fields()
        return '\0'.join(fields) + '\0'


T = TypeVar('T', bound=IBMessage)


class MessageHandler(ABC):
    """Abstract base class for message handlers."""

    @abstractmethod
    def handle(self, wrapper: Any, message: IBMessage) -> None:
        """
        Handle a parsed message.

        Args:
            wrapper: The IB wrapper instance
            message: The parsed message to handle
        """
        pass


class MessageRegistry:
    """
    Registry for message types and their handlers.

    This class manages the mapping between message IDs and their
    corresponding Pydantic models and handler functions.
    """

    def __init__(self):
        self._message_classes: dict[int, type[IBMessage]] = {}
        self._handlers: dict[type[IBMessage], Callable[[Any, IBMessage], None]] = {}
        self._logger = logging.getLogger(__name__)

    def register_message(self, msg_id: int) -> Callable[[type[T]], type[T]]:
        """
        Decorator to register a message class with its ID.

        Args:
            msg_id: The IB protocol message ID

        Returns:
            Decorator function

        Example:
            @registry.register_message(msg_id=1)
            class PriceSizeTickMessage(IBMessage):
                ...
        """
        def decorator(cls: type[T]) -> type[T]:
            cls.MESSAGE_ID = msg_id
            self._message_classes[msg_id] = cls
            self._logger.debug(f"Registered message class {cls.__name__} for ID {msg_id}")
            return cls
        return decorator

    def register_handler(
        self,
        message_cls: type[IBMessage]
    ) -> Callable[[Callable[[Any, IBMessage], None]], Callable[[Any, IBMessage], None]]:
        """
        Decorator to register a handler function for a message class.

        Args:
            message_cls: The message class to handle

        Returns:
            Decorator function

        Example:
            @registry.register_handler(PriceSizeTickMessage)
            def handle_price_size_tick(wrapper, msg: PriceSizeTickMessage):
                ...
        """
        def decorator(func: Callable[[Any, IBMessage], None]) -> Callable[[Any, IBMessage], None]:
            self._handlers[message_cls] = func
            self._logger.debug(f"Registered handler {func.__name__} for {message_cls.__name__}")
            return func
        return decorator

    def get_message_class(self, msg_id: int) -> type[IBMessage] | None:
        """
        Get the message class for a given message ID.

        Args:
            msg_id: The IB protocol message ID

        Returns:
            The message class or None if not registered
        """
        return self._message_classes.get(msg_id)

    def get_handler(self, message_cls: type[IBMessage]) -> Callable[[Any, IBMessage], None] | None:
        """
        Get the handler function for a message class.

        Args:
            message_cls: The message class

        Returns:
            The handler function or None if not registered
        """
        return self._handlers.get(message_cls)

    def list_registered_messages(self) -> dict[int, str]:
        """
        List all registered message types.

        Returns:
            Dictionary of message ID to class name
        """
        return {
            msg_id: cls.__name__
            for msg_id, cls in self._message_classes.items()
        }

    def list_registered_handlers(self) -> dict[str, str]:
        """
        List all registered handlers.

        Returns:
            Dictionary of message class name to handler function name
        """
        return {
            cls.__name__: func.__name__
            for cls, func in self._handlers.items()
        }


# Global registry instance
registry = MessageRegistry()
