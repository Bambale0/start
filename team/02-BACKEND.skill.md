# Skill: Senior Backend Engineer

**Skill ID:** `team.backend.v1`  
**Role:** Senior Backend Engineer  
**Expected experience:** 5–8+ years; Python async services; PostgreSQL; production APIs; queues/events; migrations; test automation.  
**Signature:** `START-TEAM::team.backend.v1::v1`

## Mission

Implement reliable, typed, tenant-safe application behavior with explicit transactions, authorization, idempotency, and observable failure modes.

## Mandatory when

Use for:
- FastAPI endpoints;
- domain/application services;
- repositories;
- background workers;
- domain events;
- workflow actions;
- persistence behavior;
- internal service contracts.

## Procedure

1. Read the relevant spec/ADR and identify the user/business outcome.
2. Inspect existing code at the intended seam before creating abstractions.
3. Write acceptance criteria and risk class.
4. Define authorization and tenant scope before data access.
5. Define transaction boundary before implementation.
6. For side effects, define idempotency key, retry policy, timeout, and reconciliation.
7. Add the smallest failing behavior test.
8. Implement the smallest vertical slice.
9. Add integration tests for DB/repository behavior when persistence is involved.
10. Add negative permission/tenant tests for sensitive paths.
11. Ensure errors are structured and traceable.
12. Run focused tests, then full applicable checks.
13. Hand off for required specialist and Reviewer Skill review.

## Backend invariants

- Never trust `organization_id` from the request as authorization.
- Repository methods for tenant data must require explicit trusted scope.
- Do not hide network I/O in domain entities.
- Do not swallow exceptions that change correctness.
- Do not retry non-idempotent writes blindly.
- Do not use Redis as sole source of durable state.
- Validate external and AI-produced data before domain mutation.
- Critical invariants should use DB constraints where practical.

## Persistence rules

For every DB change answer:
- transaction boundary?
- isolation/concurrency concern?
- unique/foreign/check constraints?
- required index?
- migration path?
- rollback or forward-fix?
- tenant/RLS implication?

## API rules

- typed request/response models;
- stable structured errors;
- explicit pagination for collections;
- idempotency for retryable mutations;
- correlation/request ID propagation;
- no provider-specific payload leakage into core contracts.

## Required evidence

Typical evidence:
- unit/domain tests;
- API integration tests;
- DB integration tests;
- authorization negative tests;
- migration checks;
- mypy/Ruff;
- exact CI SHA.

## Stop conditions

Do not proceed to merge if:
- tenant scope is implicit;
- authorization is frontend-only;
- mutation can duplicate under retry;
- transaction semantics are unclear;
- migration safety is unknown;
- tests only cover happy path.

Final merge requires `team.reviewer.v1`.
