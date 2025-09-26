"""Custom Pydantic validators for IB protocol data."""

from datetime import datetime
from typing import Any

from pydantic import field_validator

from ib_insync.util import UNSET_DOUBLE, UNSET_INTEGER, parseIBDatetime


class IBValidators:
    """Collection of reusable validators for IB data types."""

    @staticmethod
    def validate_ib_float(v: Any) -> float:
        """
        Validate and convert IB float values.

        Handles empty strings, UNSET_DOUBLE, and special values.
        """
        if v == '' or v is None:
            return 0.0
        if v == UNSET_DOUBLE:
            return UNSET_DOUBLE
        if isinstance(v, str):
            if v.lower() == 'infinite':
                return float('inf')
            return float(v)
        return float(v)

    @staticmethod
    def validate_ib_int(v: Any) -> int:
        """
        Validate and convert IB integer values.

        Handles empty strings, UNSET_INTEGER, and special values.
        """
        if v == '' or v is None:
            return 0
        if v == UNSET_INTEGER:
            return UNSET_INTEGER
        if isinstance(v, str):
            return int(v)
        return int(v)

    @staticmethod
    def validate_ib_bool(v: Any) -> bool:
        """
        Validate and convert IB boolean values.

        IB uses '1'/'0' for true/false.
        """
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v == '1' or v.lower() == 'true'
        if isinstance(v, (int, float)):
            return bool(v)
        return False

    @staticmethod
    def validate_ib_datetime(v: Any) -> datetime | None:
        """
        Validate and convert IB datetime values.

        Handles various IB datetime formats.
        """
        if v == '' or v is None:
            return None
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            try:
                return parseIBDatetime(v)
            except Exception:
                return None
        if isinstance(v, (int, float)):
            # Unix timestamp
            try:
                return datetime.fromtimestamp(v)
            except Exception:
                return None
        return None

    @staticmethod
    def validate_sec_type(v: str) -> str:
        """
        Validate security type.

        Args:
            v: Security type string

        Returns:
            Validated security type

        Raises:
            ValueError: If security type is invalid
        """
        valid_types = {
            'STK', 'OPT', 'FUT', 'CONTFUT', 'CASH', 'BOND', 'CFD',
            'FOP', 'WAR', 'IOPT', 'BAG', 'IND', 'CMDTY', 'CRYPTO',
            'NEWS', 'EVENT', 'FUND'
        }
        if v and v not in valid_types:
            raise ValueError(f'Invalid security type: {v}')
        return v

    @staticmethod
    def validate_order_type(v: str) -> str:
        """
        Validate order type.

        Args:
            v: Order type string

        Returns:
            Validated order type

        Raises:
            ValueError: If order type is invalid
        """
        valid_types = {
            'MKT', 'LMT', 'STP', 'STP LMT', 'REL', 'TRAIL', 'BOX TOP',
            'FIX PEGGED', 'ICEBERG', 'LIT', 'LMT + MKT', 'LOC', 'MIT',
            'MKT PRT', 'MOC', 'MTL', 'PASSV REL', 'PEG BENCH', 'PEG MID',
            'PEG MKT', 'PEG PRIM', 'PEG STK', 'REL + LMT', 'REL + MKT',
            'SNAP MID', 'SNAP MKT', 'SNAP PRIM', 'STP PRT', 'TRAIL LIMIT',
            'TRAIL LIT', 'TRAIL MIT', 'TRAIL REL + MKT', 'TRAIL STP',
            'VOL', 'VWAP', 'QUOTE', 'PPV', 'PDV', 'PIV', 'PSV', 'MIDPX'
        }
        if v and v not in valid_types:
            # Log warning but allow for forward compatibility
            pass
        return v

    @staticmethod
    def validate_order_action(v: str) -> str:
        """
        Validate order action.

        Args:
            v: Order action string

        Returns:
            Validated order action

        Raises:
            ValueError: If order action is invalid
        """
        valid_actions = {'BUY', 'SELL', 'SSHORT'}
        if v and v not in valid_actions:
            raise ValueError(f'Invalid order action: {v}')
        return v

    @staticmethod
    def validate_time_in_force(v: str) -> str:
        """
        Validate time in force.

        Args:
            v: Time in force string

        Returns:
            Validated time in force
        """
        valid_tifs = {'DAY', 'GTC', 'OPG', 'IOC', 'GTD', 'GTT', 'AUC', 'FOK', 'GTX', 'DTC'}
        if v and v not in valid_tifs:
            # Log warning but allow
            pass
        return v

    @staticmethod
    def validate_right(v: str) -> str:
        """
        Validate option right (PUT/CALL).

        Args:
            v: Option right string

        Returns:
            Validated option right
        """
        if not v:
            return v
        # Accept various formats
        v_upper = v.upper()
        if v_upper in ('P', 'PUT'):
            return 'P'
        elif v_upper in ('C', 'CALL'):
            return 'C'
        elif v == '':
            return ''
        else:
            raise ValueError(f'Invalid option right: {v}')


def ib_float_validator(field_name: str):
    """
    Create a Pydantic field validator for IB float fields.

    Args:
        field_name: Name of the field to validate

    Returns:
        Field validator function
    """
    @field_validator(field_name, mode='before')
    def validate(cls, v):
        return IBValidators.validate_ib_float(v)
    return validate


def ib_int_validator(field_name: str):
    """
    Create a Pydantic field validator for IB integer fields.

    Args:
        field_name: Name of the field to validate

    Returns:
        Field validator function
    """
    @field_validator(field_name, mode='before')
    def validate(cls, v):
        return IBValidators.validate_ib_int(v)
    return validate


def ib_bool_validator(field_name: str):
    """
    Create a Pydantic field validator for IB boolean fields.

    Args:
        field_name: Name of the field to validate

    Returns:
        Field validator function
    """
    @field_validator(field_name, mode='before')
    def validate(cls, v):
        return IBValidators.validate_ib_bool(v)
    return validate


def ib_datetime_validator(field_name: str):
    """
    Create a Pydantic field validator for IB datetime fields.

    Args:
        field_name: Name of the field to validate

    Returns:
        Field validator function
    """
    @field_validator(field_name, mode='before')
    def validate(cls, v):
        return IBValidators.validate_ib_datetime(v)
    return validate
