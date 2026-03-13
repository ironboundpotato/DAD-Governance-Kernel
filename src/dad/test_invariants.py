"""
D.A.D. Governance Kernel v0.1
Deterministic Invariant Tests
Author: Kevin Gilbert
"""

from delegation import DelegationRegistry
from constraints import ConstraintRegistry, MaintenanceModeConstraint, MaxFileSizeConstraint, AuthorityWriteRestriction
from drift_engine import DriftEngine
from governance_kernel import GovernanceKernel
from logger import StructuredLogger
from state_machine import StateMachine, KernelState


def build_kernel():
    delegation = DelegationRegistry()
    delegation.register("admin", "file_writer", ["write_file"])
    delegation.register("operator", "compute_engine", ["compute_sum"])

    constraints = ConstraintRegistry()
    constraints.register(MaintenanceModeConstraint())
    constraints.register(MaxFileSizeConstraint())
    constraints.register(AuthorityWriteRestriction())

    drift = DriftEngine()
    logger = StructuredLogger()
    kernel = GovernanceKernel(delegation, constraints, drift, logger)
    return kernel, logger


def test_determinism():
    """Identical inputs must produce identical decisions."""
    print("[TEST] Determinism invariant...")

    context = {
        "system_mode": "normal",
        "resource_usage": 0.40,
        "heartbeat_ok": True,
        "execution_latency_ms": 100,
        "error_flag": False,
        "file_size": 500,
        "max_file_size": 1024,
    }

    kernel1, _ = build_kernel()
    kernel2, _ = build_kernel()

    r1 = kernel1.evaluate("admin", "file_writer", "write_file", context)
    r2 = kernel2.evaluate("admin", "file_writer", "write_file", context)

    assert r1["decision"] == r2["decision"], "FAIL: Decisions do not match"
    assert r1["drift_severity"] == r2["drift_severity"], "FAIL: Drift severity mismatch"
    assert r1["delegation_valid"] == r2["delegation_valid"], "FAIL: Delegation mismatch"
    print("  PASS: Identical inputs produce identical decisions")


def test_single_decision_per_request():
    """Each request must produce exactly one decision record."""
    print("[TEST] Single decision guarantee...")

    kernel, logger = build_kernel()
    context = {
        "system_mode": "normal",
        "resource_usage": 0.40,
        "heartbeat_ok": True,
        "execution_latency_ms": 100,
        "error_flag": False,
        "file_size": 500,
        "max_file_size": 1024,
    }

    kernel.evaluate("admin", "file_writer", "write_file", context)
    kernel.evaluate("admin", "file_writer", "write_file", context)

    assert len(logger.get_log()) == 2, "FAIL: Expected exactly 2 log entries"
    print("  PASS: Each request produces exactly one decision record")


def test_illegal_delegation_blocked():
    """Actions without explicit delegation must be blocked."""
    print("[TEST] Authority supremacy invariant...")

    kernel, _ = build_kernel()
    context = {
        "system_mode": "normal",
        "resource_usage": 0.40,
        "heartbeat_ok": True,
        "execution_latency_ms": 100,
        "error_flag": False,
        "file_size": 500,
        "max_file_size": 1024,
    }

    record = kernel.evaluate("unknown_agent", "file_writer", "write_file", context)
    assert record["decision"] == "BLOCKED", "FAIL: Undelegated action was not blocked"
    print("  PASS: Undelegated action correctly blocked")


def test_l3_routes_to_containment():
    """L3 drift must route to CONTAINMENT."""
    print("[TEST] L3 drift routing invariant...")

    kernel, _ = build_kernel()
    context = {
        "system_mode": "normal",
        "resource_usage": 0.95,
        "heartbeat_ok": True,
        "execution_latency_ms": 100,
        "error_flag": False,
        "file_size": 500,
        "max_file_size": 1024,
    }

    record = kernel.evaluate("admin", "file_writer", "write_file", context)
    assert record["decision"] == "CONTAINMENT", f"FAIL: Expected CONTAINMENT, got {record['decision']}"
    print("  PASS: L3 drift correctly routes to CONTAINMENT")


def test_l4_routes_to_escalated():
    """L4 drift must route to ESCALATED."""
    print("[TEST] L4 drift routing invariant...")

    kernel, _ = build_kernel()
    context = {
        "system_mode": "normal",
        "resource_usage": 0.40,
        "heartbeat_ok": False,
        "execution_latency_ms": 100,
        "error_flag": True,
        "file_size": 500,
        "max_file_size": 1024,
    }

    record = kernel.evaluate("admin", "file_writer", "write_file", context)
    assert record["decision"] == "ESCALATED", f"FAIL: Expected ESCALATED, got {record['decision']}"
    print("  PASS: L4 drift correctly routes to ESCALATED")


def test_illegal_state_transition_raises():
    """Illegal state transitions must raise exceptions."""
    print("[TEST] Illegal state transition invariant...")

    sm = StateMachine()
    try:
        sm.transition(KernelState.AUTHORIZED)  # Illegal from IDLE
        print("  FAIL: No exception raised on illegal transition")
    except ValueError:
        print("  PASS: Illegal transition correctly raised ValueError")


def test_kernel_returns_to_idle():
    """Kernel must return to IDLE after every evaluation."""
    print("[TEST] Kernel IDLE return invariant...")

    kernel, _ = build_kernel()
    context = {
        "system_mode": "normal",
        "resource_usage": 0.40,
        "heartbeat_ok": True,
        "execution_latency_ms": 100,
        "error_flag": False,
        "file_size": 500,
        "max_file_size": 1024,
    }

    kernel.evaluate("admin", "file_writer", "write_file", context)
    assert kernel.state == KernelState.IDLE, f"FAIL: Kernel state is {kernel.state}, expected IDLE"
    print("  PASS: Kernel correctly returns to IDLE after evaluation")


if __name__ == "__main__":
    print("=" * 60)
    print("D.A.D. Governance Kernel v0.1 — Invariant Tests")
    print("Author: Kevin Gilbert")
    print("=" * 60)
    print()

    test_determinism()
    test_single_decision_per_request()
    test_illegal_delegation_blocked()
    test_l3_routes_to_containment()
    test_l4_routes_to_escalated()
    test_illegal_state_transition_raises()
    test_kernel_returns_to_idle()

    print()
    print("=" * 60)
    print("ALL INVARIANT TESTS PASSED")
    print("=" * 60)
