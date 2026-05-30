#!/usr/bin/env python3
"""
CollateralOps Configuration - Environment-based constants.

All hardcoded values from engines should reference this file.
"""

import os
from decimal import Decimal

# Financial constants
CONSERVATISM_FACTOR = Decimal(os.getenv("COLLATERAL_CONSERVATISM", "0.85"))
ENGINEERING_RATE_USD = Decimal(os.getenv("COLLATERAL_ENG_RATE", "75"))

# LTV thresholds
LTV_HIGH = Decimal(os.getenv("COLLATERAL_LTV_HIGH", "0.35"))
LTV_MEDIUM = Decimal(os.getenv("COLLATERAL_LTV_MED", "0.20"))
LTV_LOW = Decimal(os.getenv("COLLATERAL_LTV_LOW", "0.12"))
LTV_MINIMAL = Decimal(os.getenv("COLLATERAL_LTV_MIN", "0.07"))

# Financeability score thresholds
FINANCEABILITY_LENDER_READY = int(os.getenv("COLLATERAL_FSCORE_LENDER", "65"))
FINANCEABILITY_BUYER_READY = int(os.getenv("COLLATERAL_FSCORE_BUYER", "50"))
FINANCEABILITY_PACKET_READY = int(os.getenv("COLLATERAL_FSCORE_PACKET", "50"))
FINANCEABILITY_FINANCEABLE = int(os.getenv("COLLATERAL_FSCORE_FIN", "60"))

# Valuation caps
MAX_REPLACEMENT_COST = Decimal(os.getenv("COLLATERAL_MAX_REPL", "5000000"))
MAX_AS_IS_VALUE = Decimal(os.getenv("COLLATERAL_MAX_ASIS", "2000000"))

# Database
COLLATERAL_DB_PATH = os.getenv("COLLATERAL_DB_PATH", "collateral_registry.db")

# Audit
AGENT_CLEANUP_SCAFFOLD = Decimal(os.getenv("COLLATERAL_CLEANUP_SCAFFOLD", "15"))
AGENT_CLEANUP_DUPLICATE = Decimal(os.getenv("COLLATERAL_CLEANUP_DUP", "10"))
AGENT_CLEANUP_RISKY = Decimal(os.getenv("COLLATERAL_CLEANUP_RISKY", "150"))
AGENT_CLEANUP_BUILD_FAIL = Decimal(os.getenv("COLLATERAL_CLEANUP_BUILD", "200"))
AGENT_CLEANUP_MISSING_TESTS = Decimal(os.getenv("COLLATERAL_CLEANUP_TESTS", "50"))
