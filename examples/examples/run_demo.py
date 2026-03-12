"""
D.A.D. Governance Kernel — Example Execution

This script demonstrates a simple evaluation using the
Deterministic Autonomous Directives kernel.

Run with:
python examples/run_demo.py
"""

from dad.kernel import DADKernel
from dad.types import ActionRequest


def main():
    # Initialize kernel
    kernel = DADKernel()

    # Register a simple delegation
    kernel.delegation.register("admin", "write_file")

    # Register a basic constraint
    def maintenance_constraint(request):
        return request.context.get("system_mode", "normal") != "maintenance"

    kernel.constraints.register(maintenance_constraint)

    # Example request
    request = ActionRequest(
        authority_id="admin",
        action="write_file",
        context={
            "system_mode": "normal",
            "resource_usage": 0.35,
            "heartbeat_ok": True,
            "execution_latency_ms": 120,
            "error_flag": False
        }
    )

    # Evaluate request
    result = kernel.evaluate(request)

    # Output decision
    print("\nD.A.D. Evaluation Result\n")
    print(f"Authority: {result['authority']}")
    print(f"Action: {result['action']}")
    print(f"Delegation OK: {result['delegation_ok']}")
    print(f"Constraint Results: {result['constraints']}")
    print(f"Drift Level: {result['drift']}")
    print(f"Decision: {result['decision']}")
    print(f"Event ID: {result['event_id']}")
    print(f"Timestamp: {result['timestamp']}")
    print()


if __name__ == "__main__":
    main()