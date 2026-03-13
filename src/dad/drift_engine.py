"""
D.A.D. Governance Kernel v0.1
Drift Engine
Author: Kevin Gilbert
"""


class DriftSeverity:
    L1 = "L1"  # Cosmetic
    L2 = "L2"  # Ambiguity
    L3 = "L3"  # Structural Instability
    L4 = "L4"  # Critical Breach


class DriftEngine:
    """
    Classifies system stability based on signal inputs.
    Returns severity level only.
    Does not perform routing.
    Rule-based and deterministic.
    """

    def classify(self, signals: dict) -> str:
        """
        Evaluates signals and returns the highest applicable severity level.
        Identical inputs always produce identical outputs.
        """
        error_flag = signals.get("error_flag", False)
        heartbeat_ok = signals.get("heartbeat_ok", True)
        resource_usage = signals.get("resource_usage", 0.0)
        execution_latency_ms = signals.get("execution_latency_ms", 0)

        # L4 — Critical Breach
        if error_flag and not heartbeat_ok:
            return DriftSeverity.L4

        # L3 — Structural Instability
        if not heartbeat_ok:
            return DriftSeverity.L3
        if resource_usage >= 0.90:
            return DriftSeverity.L3
        if execution_latency_ms >= 5000:
            return DriftSeverity.L3
        if error_flag:
            return DriftSeverity.L3

        # L2 — Ambiguity
        if resource_usage >= 0.70:
            return DriftSeverity.L2
        if execution_latency_ms >= 1000:
            return DriftSeverity.L2

        # L1 — Cosmetic (baseline)
        return DriftSeverity.L1
