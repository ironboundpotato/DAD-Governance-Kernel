"""
D.A.D. Governance Kernel v0.1
Structured Logger
Author: Kevin Gilbert
"""

import uuid
from datetime import datetime, timezone


class StructuredLogger:
    """
    Append-only structured logging system.
    Every evaluation produces exactly one decision record.
    No field omissions permitted.
    """

    def __init__(self):
        self._log = []

    def record(
        self,
        authority_id: str,
        plugin_id: str,
        action: str,
        prior_state: str,
        delegation_valid: bool,
        constraint_results: dict,
        drift_severity: str,
        final_state: str,
        decision: str,
    ) -> dict:
        """
        Creates and appends a structured decision record.
        Returns the record.
        """
        entry = {
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "authority_id": authority_id,
            "plugin_id": plugin_id,
            "action": action,
            "prior_state": prior_state,
            "delegation_valid": delegation_valid,
            "constraint_results": constraint_results,
            "drift_severity": drift_severity,
            "final_state": final_state,
            "decision": decision,
        }
        self._log.append(entry)
        return entry

    def get_log(self) -> list:
        """Returns a copy of the full log. Append-only — no mutations."""
        return list(self._log)
