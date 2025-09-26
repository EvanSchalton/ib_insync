"""Message dispatcher for routing IB protocol messages to handlers."""

import logging
import time
from typing import Any

from pydantic import ValidationError

from ib_insync.decoders.base import IBMessage, MessageRegistry


class MessageDispatcher:
    """
    Dispatcher for routing IB protocol messages to appropriate handlers.

    This class is responsible for:
    - Parsing raw field lists into Pydantic message models
    - Validating message data
    - Routing messages to registered handlers
    - Error handling and logging
    - Performance monitoring
    """

    def __init__(
        self,
        wrapper: Any,
        registry: MessageRegistry | None = None,
        server_version: int = 0,
    ):
        """
        Initialize the message dispatcher.

        Args:
            wrapper: The IB wrapper instance
            registry: Message registry (uses global if not provided)
            server_version: Server version for compatibility
        """
        self.wrapper = wrapper
        self.server_version = server_version

        # Use provided registry or import global
        if registry is None:
            from ib_insync.decoders.base import registry as global_registry
            self.registry = global_registry
        else:
            self.registry = registry

        self.logger = logging.getLogger(__name__)

        # Statistics tracking
        self.stats = {
            'messages_processed': 0,
            'messages_failed': 0,
            'validation_errors': 0,
            'unknown_messages': 0,
            'processing_time': 0.0,
        }
        self.message_counts: dict[int, int] = {}

        # Middleware functions
        self.pre_processors = []
        self.post_processors = []

    def dispatch(self, fields: list[str]) -> IBMessage | None:
        """
        Dispatch a message from raw fields.

        Args:
            fields: List of string fields from IB protocol

        Returns:
            The parsed message object or None if processing failed
        """
        start_time = time.perf_counter()

        try:
            # Extract message ID
            if not fields or not fields[0]:
                self.logger.warning(f"Empty or invalid fields: {fields}")
                self.stats['messages_failed'] += 1
                return None

            try:
                msg_id = int(fields[0])
            except (ValueError, TypeError):
                self.logger.error(f"Invalid message ID: {fields[0]}")
                self.stats['messages_failed'] += 1
                return None

            # Update statistics
            self.stats['messages_processed'] += 1
            self.message_counts[msg_id] = self.message_counts.get(msg_id, 0) + 1

            # Run pre-processors
            for processor in self.pre_processors:
                fields = processor(fields)

            # Get message class
            message_cls = self.registry.get_message_class(msg_id)
            if not message_cls:
                if self.logger.isEnabledFor(logging.DEBUG):
                    self.logger.debug(f"Unknown message ID: {msg_id}, fields: {fields[:10]}")
                self.stats['unknown_messages'] += 1
                # Call legacy handler if available
                self._call_legacy_handler(msg_id, fields)
                return None

            # Parse fields into message object
            try:
                message = message_cls.from_fields(fields, self.server_version)
                if message is None:
                    # Message chose not to be created (e.g., empty price)
                    return None
            except Exception as e:
                self.logger.error(
                    f"Failed to parse {message_cls.__name__} from fields: {e}",
                    exc_info=True
                )
                self.stats['messages_failed'] += 1
                return None

            # Message is already validated during parsing in from_fields

            # Get and call handler
            handler = self.registry.get_handler(message_cls)
            if handler:
                try:
                    handler(self.wrapper, message)
                except Exception as e:
                    self.logger.error(
                        f"Handler error for {message_cls.__name__}: {e}",
                        exc_info=True
                    )
                    self.stats['messages_failed'] += 1
            else:
                # No handler registered, call wrapper method directly if available
                self._call_wrapper_method(message_cls.__name__, message)

            # Run post-processors
            for processor in self.post_processors:
                processor(message)

            return message

        finally:
            # Update processing time
            elapsed = time.perf_counter() - start_time
            self.stats['processing_time'] += elapsed

    def _call_legacy_handler(self, msg_id: int, fields: list[str]) -> None:
        """
        Call legacy decoder handler for backward compatibility.

        Args:
            msg_id: Message ID
            fields: Raw fields
        """
        # This would integrate with the existing decoder.py
        # For now, just log
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(f"Would call legacy handler for msg_id {msg_id}")

    def _call_wrapper_method(self, message_name: str, message: IBMessage) -> None:
        """
        Call wrapper method based on message name.

        Args:
            message_name: Name of the message class
            message: The message object
        """
        # Convert message class name to wrapper method name
        # e.g., PriceSizeTickMessage -> priceSizeTick
        method_name = message_name[0].lower() + message_name[1:]
        if method_name.endswith('Message'):
            method_name = method_name[:-7]

        method = getattr(self.wrapper, method_name, None)
        if method:
            try:
                # Convert message to appropriate parameters
                # This would need to be customized per message type
                self._call_wrapper_with_message(method, message)
            except Exception as e:
                self.logger.error(
                    f"Error calling wrapper method {method_name}: {e}",
                    exc_info=True
                )

    def _call_wrapper_with_message(self, method: callable, message: IBMessage) -> None:
        """
        Call wrapper method with message data.

        Args:
            method: Wrapper method to call
            message: Message object
        """
        # Default implementation - subclasses can override
        # This would need specific logic for each message type
        if hasattr(message, 'req_id'):
            # Many methods take req_id as first parameter
            method(message.req_id, message)
        else:
            method(message)

    def add_pre_processor(self, processor: callable) -> None:
        """
        Add a pre-processor function.

        Pre-processors are called before message parsing.

        Args:
            processor: Function that takes fields and returns modified fields
        """
        self.pre_processors.append(processor)

    def add_post_processor(self, processor: callable) -> None:
        """
        Add a post-processor function.

        Post-processors are called after successful message handling.

        Args:
            processor: Function that takes a message object
        """
        self.post_processors.append(processor)

    def get_statistics(self) -> dict[str, Any]:
        """
        Get dispatcher statistics.

        Returns:
            Dictionary of statistics
        """
        stats = self.stats.copy()
        stats['message_counts'] = self.message_counts.copy()
        if stats['messages_processed'] > 0:
            stats['avg_processing_time'] = (
                stats['processing_time'] / stats['messages_processed']
            )
            stats['error_rate'] = (
                stats['messages_failed'] / stats['messages_processed']
            )
        else:
            stats['avg_processing_time'] = 0
            stats['error_rate'] = 0
        return stats

    def reset_statistics(self) -> None:
        """Reset dispatcher statistics."""
        self.stats = {
            'messages_processed': 0,
            'messages_failed': 0,
            'validation_errors': 0,
            'unknown_messages': 0,
            'processing_time': 0.0,
        }
        self.message_counts.clear()


class AsyncMessageDispatcher(MessageDispatcher):
    """
    Asynchronous version of the message dispatcher.

    This can be used with asyncio for better performance
    in async environments.
    """

    async def dispatch_async(self, fields: list[str]) -> IBMessage | None:
        """
        Asynchronously dispatch a message.

        This allows for async handlers and better concurrency.

        Args:
            fields: List of string fields from IB protocol

        Returns:
            The parsed message object or None if processing failed
        """
        # For now, just call sync version
        # Could be enhanced with async handlers
        return self.dispatch(fields)
