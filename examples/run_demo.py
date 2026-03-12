"""
D.A.D. Governance Kernel — Example Execution

This script demonstrates a simple evaluation using the
Deterministic Autonomous Directives kernel.

Run with:

python examples/run_demo.py
"""

import json

from dad.kernel import DADKernel
from dad.types import ActionRequest


def main():

    kernel = DADKernel()

    request = ActionRequest(
        authority="admin",
        action="write_file",
        context={
            "resource_usage": 0.2,
            "target": "/data/output.txt"
        },
    )

    result = kernel.evaluate(request)

    print("\nD.A.D. Evaluation Result\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()