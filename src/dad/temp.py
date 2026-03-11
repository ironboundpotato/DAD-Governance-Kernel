"""
D.A.D. — Deterministic Autonomous Directives
Governance Kernel Package Initialization

This package provides the core modules for the D.A.D. governance layer.
It exposes the primary interfaces for delegation validation, constraint
evaluation, drift classification, deterministic state routing, and
structured logging.

Author: Kevin Gilbert
Role: Governance Architect
"""

from .kernel import DADKernel
from .types import (
    ActionRequest,
    Delegation,
    DriftReport,
    ConstraintViolation,
)

__all__ = [
    "DADKernel",
    "ActionRequest",
    "Delegation",
    "DriftReport",
    "ConstraintViolation",
]