# Example Execution

This example demonstrates a single evaluation cycle of the D.A.D. Governance Kernel.

The kernel evaluates an action request before execution through the deterministic pipeline:

Delegation → Constraints → Drift → Routing → Logging

---

## Example Input

**Authority**

admin

**Plugin**

file_writer

**Action**

write_file

**Context Signals**

system_mode: normal  
resource_usage: 0.40  
heartbeat_ok: true  
execution_latency_ms: 100  
error_flag: false  
file_size: 500  
max_file_size: 1024

---

## Evaluation Pipeline

### Step 1 — Delegation Validation

Authority mapping checked:

admin → file_writer → write_file

Delegation result:

VALID

---

### Step 2 — Constraint Evaluation

Constraints executed:

- MaintenanceModeConstraint
- MaxFileSizeConstraint
- AuthorityWriteRestriction

Constraint results:

MaintenanceModeConstraint: PASS  
MaxFileSizeConstraint: PASS  
AuthorityWriteRestriction: PASS

---

### Step 3 — Drift Classification

Observed signals:

resource_usage: 0.40  
heartbeat_ok: true  
execution_latency_ms: 100  
error_flag: false

Drift severity returned:

L1 (Cosmetic)

---

### Step 4 — State Routing

Routing inputs:

Delegation: PASS  
Constraints: PASS  
Drift: L1

Resulting system state:

AUTHORIZED

---

## Decision Record

Example structured output produced by the governance kernel.

event_id: b2d88e4c-89a0-4d93-bb3a-41e9b7c3f21e  
timestamp: 2026-01-01T00:00:00Z  
authority_id: admin  
plugin_id: file_writer  
action: write_file  
prior_state: IDLE  

delegation_valid: true  

constraint_results  
MaintenanceModeConstraint: true  
MaxFileSizeConstraint: true  
AuthorityWriteRestriction: true  

drift_severity: L1  

final_state: AUTHORIZED  

decision: AUTHORIZED

---

## Result

The action request is approved by the governance kernel.

Execution authority is granted and the system returns to the **IDLE** state awaiting the next evaluation cycle.