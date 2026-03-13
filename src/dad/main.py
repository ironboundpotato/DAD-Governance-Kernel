"""
D.A.D. Governance Kernel v0.1
Execution Harness
Author: Kevin Gilbert
"""

import json
from delegation import DelegationRegistry
from constraints import ConstraintRegistry, MaintenanceModeConstraint, MaxFileSizeConstraint, AuthorityWriteRestriction
from drift_engine import DriftEngine
from governance_kernel import GovernanceKernel
from logger import StructuredLogger


def build_kernel():
    # Build registries
    delegation = DelegationRegistry()
    delegation.register("admin", "file_writer", ["write_file", "read_file"])
    delegation.register("operator", "compute_engine", ["compute_sum", "compute_avg"])

    constraints = ConstraintRegistry()
    constraints.register(MaintenanceModeConstraint())
    constraints.register(MaxFileSizeConstraint())
    constraints.register(AuthorityWriteRestriction())

    drift = DriftEngine()
    logger = StructuredLogger()

    kernel = GovernanceKernel(delegation, constraints, drift, logger)
    return kernel, logger


def run_example():
    kernel, logger = build_kernel()

    print("=" * 60)
    print("D.A.D. Governance Kernel v0.1")
    print("Author: Kevin Gilbert")
    print("=" * 60)

    # Example 1 — Clean authorized request
    print("\n[TEST 1] Admin writes file — clean system")
    context = {
        "system_mode": "normal",
        "resource_usage": 0.40,
        "heartbeat_ok": True,
        "execution_latency_ms": 100,
        "error_flag": False,
        "file_size": 500,
        "max_file_size": 1024,
    }
    record = kernel.evaluate("admin", "file_writer", "write_file", context)
    print(json.dumps(record, indent=2))

    # Example 2 — Invalid delegation
    print("\n[TEST 2] Unknown authority attempts action")
    record = kernel.evaluate("unknown_agent", "file_writer", "write_file", context)
    print(json.dumps(record, indent=2))

    # Example 3 — Structural instability (L3)
    print("\n[TEST 3] Admin writes file — high resource usage (L3 drift)")
    context_l3 = dict(context)
    context_l3["resource_usage"] = 0.95
    record = kernel.evaluate("admin", "file_writer", "write_file", context_l3)
    print(json.dumps(record, indent=2))

    # Example 4 — Critical breach (L4)
    print("\n[TEST 4] Admin writes file — error + heartbeat failure (L4 drift)")
    context_l4 = dict(context)
    context_l4["error_flag"] = True
    context_l4["heartbeat_ok"] = False
    record = kernel.evaluate("admin", "file_writer", "write_file", context_l4)
    print(json.dumps(record, indent=2))

    # Full log
    print("\n" + "=" * 60)
    print("FULL AUDIT LOG")
    print("=" * 60)
    for entry in logger.get_log():
        print(json.dumps(entry, indent=2))


if __name__ == "__main__":
    run_example()
