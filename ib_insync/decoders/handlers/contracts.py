"""Handler functions for contract-related messages."""

import logging
from typing import Any

from ib_insync.decoders.base import registry
from ib_insync.decoders.models.contracts import (
    BondContractDetailsMessage,
    CommissionReportMessage,
    ContractDetailsEndMessage,
    ContractDetailsMessage,
    DeltaNeutralValidationMessage,
    ScannerDataMessage,
    SecurityDefinitionOptionParameterEndMessage,
    SecurityDefinitionOptionParameterMessage,
)

logger = logging.getLogger(__name__)


@registry.register_handler(ContractDetailsMessage)
def handle_contract_details(wrapper: Any, msg: ContractDetailsMessage) -> None:
    """Handle contract details message."""
    wrapper.contractDetails(msg.req_id, msg.contract_details)


@registry.register_handler(BondContractDetailsMessage)
def handle_bond_contract_details(wrapper: Any, msg: BondContractDetailsMessage) -> None:
    """Handle bond contract details message."""
    wrapper.bondContractDetails(msg.req_id, msg.contract_details)


@registry.register_handler(ScannerDataMessage)
def handle_scanner_data(wrapper: Any, msg: ScannerDataMessage) -> None:
    """Handle scanner data message."""
    # Call the wrapper for each contract found
    for i, contract_details in enumerate(msg.contracts):
        wrapper.scannerData(
            msg.req_id,
            msg.ranks[i],
            contract_details,
            msg.distances[i],
            msg.benchmarks[i],
            msg.projections[i],
            msg.legs_strs[i]
        )

    # Call scanner data end
    wrapper.scannerDataEnd(msg.req_id)


@registry.register_handler(ContractDetailsEndMessage)
def handle_contract_details_end(wrapper: Any, msg: ContractDetailsEndMessage) -> None:
    """Handle contract details end message."""
    wrapper.contractDetailsEnd(msg.req_id)


@registry.register_handler(DeltaNeutralValidationMessage)
def handle_delta_neutral_validation(wrapper: Any, msg: DeltaNeutralValidationMessage) -> None:
    """Handle delta neutral validation message."""
    wrapper.deltaNeutralValidation(msg.req_id, msg.delta_neutral_contract)


@registry.register_handler(CommissionReportMessage)
def handle_commission_report(wrapper: Any, msg: CommissionReportMessage) -> None:
    """Handle commission report message."""
    wrapper.commissionReport(msg.commission_report)


@registry.register_handler(SecurityDefinitionOptionParameterMessage)
def handle_security_definition_option_parameter(
    wrapper: Any, msg: SecurityDefinitionOptionParameterMessage
) -> None:
    """Handle security definition option parameter message."""
    wrapper.securityDefinitionOptionParameter(
        msg.req_id,
        msg.exchange,
        msg.underlying_con_id,
        msg.trading_class,
        msg.multiplier,
        msg.expirations,
        msg.strikes
    )


@registry.register_handler(SecurityDefinitionOptionParameterEndMessage)
def handle_security_definition_option_parameter_end(
    wrapper: Any, msg: SecurityDefinitionOptionParameterEndMessage
) -> None:
    """Handle security definition option parameter end message."""
    wrapper.securityDefinitionOptionParameterEnd(msg.req_id)
