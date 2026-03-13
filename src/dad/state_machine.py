"""
D.A.D. Governance Kernel v0.1
State Machine
Author: Kevin Gilbert
"""

from drift_engine import DriftSeverity


class KernelState:
    INIT = "INIT"
    IDLE = "IDLE"
    EVALUATING = "EVALUATING"
    AUTHORIZED = "AUTHORIZED"
    BLOCKED = "BLOCKED"
    CONTAINMENT = "CONTAINMENT"
    ESCALATED = "ESCALATED"


# Valid state transitions
VALID_TRANSITIONS = {
    KernelState.INIT: [KernelState.IDLE],
    KernelState.IDLE: [KernelState.EVALUATING],
    KernelState.EVALUATING: [
        KernelState.AUTHORIZED,
        KernelState.BLOCKED,
        KernelState.CONTAINMENT,
        KernelState.ESCALATED,
    ],
    KernelState.AUTHORIZED: [KernelState.IDLE],
    KernelState.BLOCKED: [KernelState.IDLE],
    KernelState.CONTAINMENT: [KernelState.IDLE],
    KernelState.ESCALATED: [KernelState.IDLE],
}


class StateMachine:
    """
    Deterministic finite state machine.
    Illegal transitions raise exceptions.
    No silent fallback logic.
    """

    def __init__(self):
        self._state = KernelState.INIT
        self.transition(KernelState.IDLE)

    @property
    def state(self) -> str:
        return self._state

    def transition(self, new_state: str):
        """
        Performs a state transition.
        Raises ValueError on illegal transition.
        """
        allowed = VALID_TRANSITIONS.get(self._state, [])
        if new_state not in allowed:
            raise ValueError(
                f"Illegal state transition: {self._state} -> {new_state}"
            )
        self._state = new_state

    def route(self, delegation_valid: bool, constraints_passed: bool, drift_severity: str) -> str:
        """
        Deterministic routing based on evaluation results.
        Returns target state.
        """
        if not delegation_valid:
            return KernelState.BLOCKED

        if not constraints_passed:
            return KernelState.BLOCKED

        if drift_severity == DriftSeverity.L4:
            return KernelState.ESCALATED

        if drift_severity == DriftSeverity.L3:
            return KernelState.CONTAINMENT

        # L1 / L2
        return KernelState.AUTHORIZED
