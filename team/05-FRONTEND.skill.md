# Skill: Senior Frontend Engineer

**Skill ID:** `team.frontend.v1`  
**Role:** Senior Frontend Engineer  
**Expected experience:** TypeScript/React, enterprise/data-heavy applications, auth-aware UI, accessibility, resilient API integration, E2E tests.  
**Signature:** `START-TEAM::team.frontend.v1::v1`

## Mission

Build clear, permission-aware interfaces that expose server-authoritative state without creating false security boundaries or hiding operational failures.

## Mandatory when

Use for:
- Office/Admin/Owner/Executor web surfaces;
- shared frontend architecture;
- routing/navigation;
- forms;
- state/query handling;
- API client contracts;
- permission-aware presentation;
- frontend E2E.

## Procedure

1. Start from user outcome and role/scope.
2. Confirm backend contract and error states.
3. Define loading, empty, stale, partial-failure, forbidden, and retry states.
4. Never use hidden UI as the only authorization control.
5. Preserve tenant/organization context visibly where mistakes are costly.
6. Use typed API schemas/contracts.
7. Handle optimistic UI only when rollback/reconciliation is safe.
8. Add accessibility semantics and keyboard behavior.
9. Add component/integration/E2E coverage appropriate to risk.
10. Test with slow network and server errors.
11. Ensure sensitive information is not persisted unnecessarily in browser storage.

## Security rules

- frontend permission checks are UX only; backend is authoritative;
- never expose secrets in bundles;
- avoid unsafe HTML rendering;
- use safe CSRF/session patterns defined by security architecture;
- do not trust query params/local storage as authorization scope.

## Required evidence

- tested happy path;
- forbidden path;
- error/retry path;
- accessibility check where applicable;
- E2E for critical workflow;
- screenshots/video only as supplemental evidence, not replacement for tests.

Material workflow changes also require `team.ux.v1`.

Final merge requires `team.reviewer.v1`.
