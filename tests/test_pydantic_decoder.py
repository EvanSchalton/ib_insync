"""Tests for the Pydantic-based decoder architecture."""

from unittest.mock import MagicMock, Mock

import pytest
from ib_insync.decoders import (
    FieldIterator,
    MessageDispatcher,
    registry,
)
from ib_insync.decoders.models.market_data import (
    PriceSizeTickMessage,
    RealTimeBarMessage,
    TickByTickMessage,
    TickSizeMessage,
)


class TestFieldIterator:
    """Test the FieldIterator utility."""

    def test_basic_iteration(self):
        """Test basic field iteration."""
        fields = ['1', '2', '3', '4', '5']
        it = FieldIterator(fields)

        assert it.next() == '1'
        assert it.next() == '2'
        assert it.index == 2
        assert it.remaining() == 3
        assert it.has_more() is True

    def test_type_conversions(self):
        """Test type conversion methods."""
        fields = ['42', '3.14', '1', '', 'text']
        it = FieldIterator(fields)

        assert it.next_int() == 42
        assert it.next_float() == 3.14
        assert it.next_bool() is True
        assert it.next_int(99) == 99  # Empty field returns default
        assert it.next() == 'text'

    def test_peek_and_skip(self):
        """Test peeking and skipping."""
        fields = ['a', 'b', 'c', 'd']
        it = FieldIterator(fields)

        assert it.peek() == 'a'
        assert it.peek(1) == 'b'
        it.skip(2)
        assert it.next() == 'c'

    def test_consume_rest(self):
        """Test consuming remaining fields."""
        fields = ['1', '2', '3', '4', '5']
        it = FieldIterator(fields)
        it.skip(2)

        rest = it.consume_rest()
        assert rest == ['3', '4', '5']
        assert it.has_more() is False


class TestPriceSizeTickMessage:
    """Test PriceSizeTickMessage parsing."""

    def test_parse_valid_message(self):
        """Test parsing a valid price/size tick message."""
        fields = ['1', '1', '123', '1', '100.50', '1000']
        msg = PriceSizeTickMessage.from_fields(fields)

        assert msg.req_id == 123
        assert msg.tick_type == 1
        assert msg.price == 100.50
        assert msg.size == 1000.0

    def test_parse_empty_price(self):
        """Test that empty price returns None."""
        fields = ['1', '1', '123', '1', '', '1000']
        msg = PriceSizeTickMessage.from_fields(fields)
        assert msg is None

    def test_validation(self):
        """Test Pydantic validation."""
        # Valid message
        msg = PriceSizeTickMessage(
            req_id=123,
            tick_type=1,
            price=100.50,
            size=1000
        )
        assert msg.model_validate(msg.model_dump())

        # Test type coercion
        msg = PriceSizeTickMessage(
            req_id='123',  # String should be coerced to int
            tick_type='1',
            price='100.50',  # String should be coerced to float
            size='1000'
        )
        assert msg.req_id == 123
        assert msg.price == 100.50


class TestTickByTickMessage:
    """Test TickByTickMessage with different tick types."""

    def test_parse_last_tick(self):
        """Test parsing Last/AllLast tick."""
        fields = ['99', '456', '1', '1234567890', '100.25', '500', '3', 'NASDAQ', 'ODD_LOT']
        msg = TickByTickMessage.from_fields(fields)

        assert msg.req_id == 456
        assert msg.tick_type == 1
        assert msg.time == 1234567890
        assert msg.price == 100.25
        assert msg.size == 500.0
        assert msg.past_limit is True
        assert msg.unreported is True
        assert msg.exchange == 'NASDAQ'
        assert msg.special_conditions == 'ODD_LOT'

    def test_parse_bidask_tick(self):
        """Test parsing BidAsk tick."""
        fields = ['99', '456', '3', '1234567890', '100.10', '100.20', '1000', '2000', '1']
        msg = TickByTickMessage.from_fields(fields)

        assert msg.req_id == 456
        assert msg.tick_type == 3
        assert msg.bid_price == 100.10
        assert msg.ask_price == 100.20
        assert msg.bid_size == 1000.0
        assert msg.ask_size == 2000.0
        assert msg.bid_past_low is True
        assert msg.ask_past_high is False

    def test_parse_midpoint_tick(self):
        """Test parsing MidPoint tick."""
        fields = ['99', '456', '4', '1234567890', '100.15']
        msg = TickByTickMessage.from_fields(fields)

        assert msg.req_id == 456
        assert msg.tick_type == 4
        assert msg.mid_point == 100.15


class TestMessageDispatcher:
    """Test the MessageDispatcher."""

    def test_dispatch_valid_message(self):
        """Test dispatching a valid message."""
        wrapper = MagicMock()
        dispatcher = MessageDispatcher(wrapper)

        # Dispatch a TickSize message
        fields = ['2', '789', '5', '2500.5']
        msg = dispatcher.dispatch(fields)

        assert msg is not None
        assert isinstance(msg, TickSizeMessage)
        assert msg.req_id == 789
        assert msg.tick_type == 5
        assert msg.size == 2500.5

        # Check that handler was called
        wrapper.tickSize.assert_called_once_with(789, 5, 2500.5)

    def test_dispatch_unknown_message(self):
        """Test handling unknown message ID."""
        wrapper = MagicMock()
        dispatcher = MessageDispatcher(wrapper)

        # Unknown message ID
        fields = ['9999', 'data1', 'data2']
        msg = dispatcher.dispatch(fields)

        assert msg is None
        assert dispatcher.stats['unknown_messages'] == 1

    def test_dispatch_invalid_message(self):
        """Test handling invalid message data."""
        wrapper = MagicMock()
        dispatcher = MessageDispatcher(wrapper)

        # Invalid fields
        fields = []
        msg = dispatcher.dispatch(fields)

        assert msg is None
        assert dispatcher.stats['messages_failed'] == 1

    def test_statistics_tracking(self):
        """Test that statistics are tracked correctly."""
        wrapper = MagicMock()
        dispatcher = MessageDispatcher(wrapper)

        # Process several messages
        dispatcher.dispatch(['2', '1', '1', '100'])  # Valid
        dispatcher.dispatch(['2', '2', '2', '200'])  # Valid
        dispatcher.dispatch(['9999', 'unknown'])      # Unknown
        dispatcher.dispatch([])                       # Invalid

        stats = dispatcher.get_statistics()
        assert stats['messages_processed'] == 3  # Excludes empty fields
        assert stats['messages_failed'] == 1
        assert stats['unknown_messages'] == 1
        assert stats['message_counts'][2] == 2

    def test_middleware(self):
        """Test pre and post processors."""
        wrapper = MagicMock()
        dispatcher = MessageDispatcher(wrapper)

        pre_processor = Mock(side_effect=lambda fields: fields)
        post_processor = Mock()

        dispatcher.add_pre_processor(pre_processor)
        dispatcher.add_post_processor(post_processor)

        fields = ['2', '1', '1', '100']
        msg = dispatcher.dispatch(fields)

        pre_processor.assert_called_once_with(fields)
        post_processor.assert_called_once_with(msg)


class TestMessageRegistry:
    """Test the MessageRegistry."""

    def test_list_registered_messages(self):
        """Test listing registered messages."""
        # The registry should have our market data messages registered
        messages = registry.list_registered_messages()

        assert 1 in messages  # PriceSizeTickMessage
        assert messages[1] == 'PriceSizeTickMessage'
        assert 2 in messages  # TickSizeMessage
        assert 50 in messages  # RealTimeBarMessage

    def test_list_registered_handlers(self):
        """Test listing registered handlers."""
        handlers = registry.list_registered_handlers()

        assert 'PriceSizeTickMessage' in handlers
        assert handlers['PriceSizeTickMessage'] == 'handle_price_size_tick'


class TestRealTimeBarMessage:
    """Test RealTimeBarMessage parsing."""

    def test_parse_realtime_bar(self):
        """Test parsing a real-time bar message."""
        fields = ['50', '123', '1234567890', '100.1', '100.5', '99.9', '100.3', '10000', '100.2', '50']
        msg = RealTimeBarMessage.from_fields(fields)

        assert msg.req_id == 123
        assert msg.time == 1234567890
        assert msg.open == 100.1
        assert msg.high == 100.5
        assert msg.low == 99.9
        assert msg.close == 100.3
        assert msg.volume == 10000.0
        assert msg.wap == 100.2
        assert msg.count == 50


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
