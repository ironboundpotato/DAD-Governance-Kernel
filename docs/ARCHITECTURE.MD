# D.A.D. Architecture Overview

## Evaluation Pipeline

Action Request

↓

Delegation Validation

↓

Constraint Evaluation

↓

Drift Classification

↓

Deterministic State Routing

↓

Structured Logging

↓

Return to IDLE

## Purpose

This document provides a structured breakdown of the core subsystems that make up the Deterministic Autonomous Directives kernel.

---

## 1. Delegation Registry

The Delegation Registry establishes authority boundaries.

It performs:

- Registration of authorities  
- Assignment of delegations  
- Validation of incoming authorization requests  
- Rejection of unauthorized actions  

No implicit authority exists.  
All delegations must be explicit and verifiable.

---

## 2. Constraint System

Constraints are deterministic pass/fail rules.

Each constraint:

- Evaluates a specific condition  
- Returns True (allow) or False (block)  
- Introduces no side effects  
- Cannot silently override other constraints  

Constraints handle policy enforcement.

---

## 3. Drift Engine

The Drift Engine detects and classifies system instability.

Levels:

- L1 — Cosmetic  
- L2 — Ambiguity  
- L3 — Structural Instability  
- L4 — Critical Fault  

The Drift Engine classifies only.  
It does not decide outcomes.

---

## 4. Deterministic State Machine

The State Machine combines:

- Delegation results  
- Constraint outcomes  
- Drift severity  

It produces one reproducible state transition per action.

Undefined or illegal transitions generate explicit errors.

---

## 5. Structured Logging

Every evaluation produces a structured record:

- Input  
- Delegation result  
- Constraint outcomes  
- Drift classification  
- Final routed state  
- Decision result  

Logs are used for audits, debugging, and safety validation.

---

End of document.
