"""User type placing the order (Rule 80A) for regulatory compliance."""

from enum import Enum


class UserType(str, Enum):
    """User type placing the order (Rule 80A) for regulatory compliance."""

    INDIVIDUAL = "I"  # Individual customer account
    AGENCY = "A"  # Agency executing for a customer
    AGENT_OTHER_MEMBER = "W"  # Agent executing for another member
    INDIVIDUAL_PTIA = "J"  # Individual Prop Trading Interest Account
    AGENCY_PTIA = "U"  # Agency Prop Trading Interest Account
    AGENT_OTHER_MEMBER_PTIA = "M"  # Agent for other member PTIA
    INDIVIDUAL_PT = "K"  # Individual Proprietary Trading
    AGENCY_PT = "Y"  # Agency Proprietary Trading
    AGENT_OTHER_MEMBER_PT = "N"  # Agent for other member Proprietary Trading
