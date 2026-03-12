from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ActionRequest:
    authority: str
    action: str
    context: Dict[str, Any]


@dataclass
class Delegation:
    authority: str
    permitted: bool


@dataclass
class ConstraintViolation:
    constraint: str
    message: str


@dataclass
class DriftReport:
    level: str
    description: str