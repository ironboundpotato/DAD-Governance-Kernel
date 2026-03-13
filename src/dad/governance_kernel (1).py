"""
D.A.D. Governance Kernel v0.1
Governance Kernel — Orchestration Layer
Author: Kevin Gilbert
"""

from state_machine import StateMachine, KernelState


class GovernanceKernel:
    """
    Orchestrates all subsystems.
    Enforces evaluation order:
    Delegation -> Constraints -> Drift -> Routing -> Logging

    Receives all dependencies through constructor injection.
    No subsystem instantiation inside the kernel.
    Execution is atomic. No EXECUTING state.
    """

    def __init__(self, delegation_registry, constraint_registry, drift_engine, logger):
        self._delegation = delegation_registry
        self._constraints = constraint_registry
        self._drift = drift_engine
        self._logger = logger
        self._state_machine = StateMachine()

    @property
    def state(self) -> str:
        return self._state_machine.state

    def evaluate(self, authority_id: str, plugin_id: str, action: str, context: dict) -> dict:
        """
        Executes the full governance evaluation pipeline.
        Returns exactly one decision record per call.
        Kernel returns to IDLE after every evaluation.
        """
        prior_state = self._state_machine.state

        # Begin evaluation
        self._state_machine.transition(KernelState.EVALUATING)

        # Step 1 — Delegation
        delegation_valid = self._delegation.validate(authority_id, plugin_id, action)

        # Step 2 — Constraints
        signals = {k: v for k, v in context.items()
                   if k in ("resource_usage", "heartbeat_ok",
                             "execution_latency_ms", "error_flag")}
        constraint_results = self._constraints.validate(
            authority_id, plugin_id, action, context
        )
        constraints_passed = constraint_results.get("__passed__", False)

        # Step 3 — Drift Classification
        drift_severity = self._drift.classify(signals)

        # Step 4 — Routing
        target_state = self._state_machine.route(
            delegation_valid, constraints_passed, drift_severity
        )
        self._state_machine.transition(target_state)
        final_state = self._state_machine.state

        # Determine decision string
        decision = self._resolve_decision(target_state)

        # Step 5 — Log
        record = self._logger.record(
            authority_id=authority_id,
            plugin_id=plugin_id,
            action=action,
            prior_state=prior_state,
            delegation_valid=delegation_valid,
            constraint_results=constraint_results,
            drift_severity=drift_severity,
            final_state=final_state,
            decision=decision,
        )

        # Return to IDLE
        self._state_machine.transition(KernelState.IDLE)

        return record

    def _resolve_decision(self, state: str) -> str:
        decisions = {
            KernelState.AUTHORIZED: "AUTHORIZED",
            KernelState.BLOCKED: "BLOCKED",
            KernelState.CONTAINMENT: "CONTAINMENT",
            KernelState.ESCALATED: "ESCALATED",
        }
        return decisions.get(state, "UNKNOWN")

    def resolve_escalation(self):
        """
        External authority must explicitly call this to resolve ESCALATED state.
        Escalated state cannot self-resolve.
        """
        if self._state_machine.state != KernelState.ESCALATED:
            raise ValueError("Cannot resolve escalation: kernel is not in ESCALATED state.")
        self._state_machine.transition(KernelState.IDLE)
