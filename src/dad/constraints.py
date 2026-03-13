"""
D.A.D. Governance Kernel v0.1
Constraint System
Author: Kevin Gilbert
"""

from abc import ABC, abstractmethod


class Constraint(ABC):
    """Base interface for all constraints."""

    @abstractmethod
    def applies_to(self, authority_id: str, plugin_id: str, action: str) -> bool:
        """Returns True if this constraint applies to the request."""
        pass

    @abstractmethod
    def check(self, authority_id: str, plugin_id: str, action: str, context: dict) -> bool:
        """Returns True if constraint passes. False blocks execution."""
        pass


class MaintenanceModeConstraint(Constraint):
    """Blocks all actions when system is in maintenance mode."""

    def applies_to(self, authority_id: str, plugin_id: str, action: str) -> bool:
        return True  # Applies to all requests

    def check(self, authority_id: str, plugin_id: str, action: str, context: dict) -> bool:
        return context.get("system_mode", "normal") != "maintenance"


class MaxFileSizeConstraint(Constraint):
    """Blocks file write actions exceeding max file size."""

    def applies_to(self, authority_id: str, plugin_id: str, action: str) -> bool:
        return action == "write_file"

    def check(self, authority_id: str, plugin_id: str, action: str, context: dict) -> bool:
        file_size = context.get("file_size", 0)
        max_size = context.get("max_file_size", 1024)
        return file_size <= max_size


class AuthorityWriteRestriction(Constraint):
    """Restricts write_file to admin authority only."""

    def applies_to(self, authority_id: str, plugin_id: str, action: str) -> bool:
        return action == "write_file"

    def check(self, authority_id: str, plugin_id: str, action: str, context: dict) -> bool:
        return authority_id == "admin"


class ConstraintRegistry:
    """
    Evaluates all registered constraints sequentially.
    Early failure stops evaluation.
    Does not perform routing or state transitions.
    """

    def __init__(self):
        self._constraints = []

    def register(self, constraint: Constraint):
        self._constraints.append(constraint)

    def validate(self, authority_id: str, plugin_id: str, action: str, context: dict) -> dict:
        """
        Evaluates all applicable constraints.
        Returns results dict with pass/fail per constraint and overall result.
        """
        results = {}
        for constraint in self._constraints:
            name = constraint.__class__.__name__
            if constraint.applies_to(authority_id, plugin_id, action):
                passed = constraint.check(authority_id, plugin_id, action, context)
                results[name] = passed
                if not passed:
                    # Early failure
                    results["__passed__"] = False
                    return results
        results["__passed__"] = True
        return results
