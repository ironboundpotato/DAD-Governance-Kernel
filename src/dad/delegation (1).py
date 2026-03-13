"""
D.A.D. Governance Kernel v0.1
Delegation Registry
Author: Kevin Gilbert
"""


class DelegationRegistry:
    """
    Maps authorities to allowed plugin actions.
    Authority -> Plugin -> Allowed Actions
    No wildcard permissions.
    No implicit authority creation.
    """

    def __init__(self):
        self._registry = {}

    def register(self, authority_id: str, plugin_id: str, actions: list):
        """Register explicit delegation for an authority."""
        if authority_id not in self._registry:
            self._registry[authority_id] = {}
        if plugin_id not in self._registry[authority_id]:
            self._registry[authority_id][plugin_id] = set()
        self._registry[authority_id][plugin_id].update(actions)

    def validate(self, authority_id: str, plugin_id: str, action: str) -> bool:
        """
        Pure function. Returns True if delegation is valid.
        No side effects. No implicit grants.
        """
        return (
            authority_id in self._registry
            and plugin_id in self._registry[authority_id]
            and action in self._registry[authority_id][plugin_id]
        )
