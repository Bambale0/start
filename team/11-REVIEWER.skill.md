# Skill: Independent Reviewer

**Skill ID:** `team.reviewer.v1`  
**Role:** Reviewer / Release Gatekeeper  
**Expected experience:** senior-level judgment appropriate to the changed surface; ability to block unsafe work.  
**Status:** REQUIRED FOR EVERY MERGE  
**Signature:** `START-TEAM::team.reviewer.v1::v1`

# Absolute merge rule

**No PR is mergeable until this skill has been applied and the verdict is recorded.**

Green CI is not a substitute for review.

## Reviewer independence

For Medium/High risk work, reviewer should not be the primary implementer.

For High risk production changes, implementation self-review does not count as final approval.

## Inputs

Review:
- PR diff;
- declared active skills;
- acceptance criteria/spec;
- relevant ADR/security docs;
- tests and CI;
- migrations/config changes;
- specialist review evidence;
- exact head SHA.

## Review procedure

### 1. Intent
Confirm:
- what user/business outcome is intended;
- whether scope matches the request;
- whether unrelated changes were introduced.

### 2. Architecture
Check:
- dependency direction;
- module ownership;
- source-of-truth boundaries;
- no unnecessary abstraction/service split;
- no hidden cross-module writes.

### 3. Security / tenancy
Ask:
- can tenant A access tenant B?
- can client input widen scope?
- are permissions enforced server-side?
- are secrets/logs safe?
- is audit present for privileged mutation?
- is AI/external content treated as untrusted?

### 4. Correctness
Review:
- transaction boundaries;
- concurrency/races;
- duplicate delivery;
- retries;
- partial failure;
- idempotency;
- invalid/stale state.

### 5. Data/migrations
Check:
- backward compatibility;
- constraint/index impact;
- data backfill;
- lock/downtime risk;
- rollback or forward-fix;
- RLS/tenant behavior.

### 6. Integrations
Check:
- finite timeouts;
- retries only where safe;
- auth/signature;
- rate limits;
- reconciliation;
- unknown-result handling.

### 7. AI
Check:
- typed output;
- authorization before retrieval;
- tool scope;
- injection resistance;
- deterministic validation;
- eval/fallback;
- no high-impact silent action.

### 8. Operability
Check:
- logs/metrics/traces;
- request/trace/tenant correlation;
- readiness behavior;
- runbook needs;
- deploy/rollback;
- alertability.

### 9. Tests
Verify the tests would fail for the bug/risk they claim to cover.

Require:
- negative cases;
- permission/tenant cases where relevant;
- retry/duplicate cases where relevant;
- integration/E2E/smoke appropriate to risk.

### 10. Documentation
Ensure ADR/spec/CONTEXT/runbook are consistent with actual behavior.

## Finding format

Use:

```text
[SEVERITY] title
Evidence:
Risk:
Required change:
Verification:
```

Severities: Critical / High / Medium / Low.

## Approval conditions

Verdict may be `APPROVE` only when:
- Critical = 0;
- High = 0;
- required specialist reviews complete;
- acceptance criteria pass;
- applicable tests pass;
- CI green for exact SHA;
- residual risks are explicit.

Otherwise use `REQUEST_CHANGES`.

## Required review report

```text
Reviewer skill: team.reviewer.v1
Head SHA: ...
Risk class: ...
Skills checked: ...
Findings:
- Critical: 0
- High: 0
- Medium: ...
- Low: ...
Verification reviewed: ...
Residual risks: ...
Verdict: APPROVE | REQUEST_CHANGES
Reviewer: ...
```

## Merge authorization

A human or agent performing merge MUST verify that the latest review report applies to the current head SHA.

If the head SHA changes after approval, Reviewer Skill must be re-run or explicitly confirm the delta.

**Without this evidence: DO NOT MERGE.**
