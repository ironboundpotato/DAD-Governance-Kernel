import time
from typing import Dict, Any

from .types import ActionRequest


class DADKernel:
    """
    Deterministic Autonomous Directives Kernel
    """

    def __init__(self):
        self.allowed_authorities = {"admin", "system"}

    def evaluate(self, request: ActionRequest) -> Dict[str, Any]:

        start = time.time()

        delegation_ok = request.authority in self.allowed_authorities

        constraints_ok = True

        drift_level = "L1"

        decision = "AUTHORIZED" if delegation_ok and constraints_ok else "DENIED"

        result = {
            "authority": request.authority,
            "action": request.action,
            "delegation_ok": delegation_ok,
            "constraints": [constraints_ok],
            "drift": drift_level,
            "decision": decision,
            "evaluation_time_ms": round((time.time() - start) * 1000, 2),
        }

        return result