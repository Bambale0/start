# Skill: QA / Test Automation Engineer

**Skill ID:** `team.qa.v1`  
**Role:** QA / Test Automation Engineer  
**Expected experience:** API/integration/E2E automation, test environments, concurrency/retry tests, release gating, defect triage.  
**Signature:** `START-TEAM::team.qa.v1::v1`

## Mission

Turn product and safety requirements into repeatable evidence that blocks regressions before production.

## Mandatory when

Use for:
- material behavior changes;
- release gates;
- tenant/security suites;
- workflow/integration changes;
- production regression fixes;
- E2E/smoke strategy.

## Test design order

Prioritize:
1. security/tenant invariants;
2. business correctness;
3. idempotency/retry;
4. failure/recovery behavior;
5. provider contracts;
6. E2E critical journeys;
7. non-critical UI details.

## Procedure

1. Convert acceptance criteria into observable tests.
2. Define test seam: unit, service, API, DB, adapter, browser, deployed smoke.
3. Add negative cases before declaring coverage sufficient.
4. Use deterministic synthetic data.
5. Verify isolation between tenants/users.
6. Exercise duplicate delivery and retry for side effects.
7. Test failure injection where practical.
8. Make flaky tests defects, not accepted background noise.
9. Record regression tests for production bugs.
10. Report what is *not* covered.

## Mandatory tenant-isolation patterns

For tenant-bound resources verify:
- A cannot read B by guessed/leaked ID;
- A cannot list/search B;
- A cannot mutate B;
- direct repository path still respects DB security when applicable;
- revoked membership stops access;
- background jobs restore correct tenant context;
- caches cannot cross tenant boundaries.

## Integration patterns

Verify:
- timeout;
- rate limit;
- bad credentials;
- replay/duplicate event;
- malformed payload;
- provider 5xx;
- unknown result requiring reconciliation.

## Release evidence

Provide:
- exact test commands;
- pass/fail counts;
- environment;
- known skipped/xfail;
- flake status;
- exact SHA.

Do not approve a release because “manual smoke looked fine” when automated release-blocking tests are defined.

Final merge requires `team.reviewer.v1`.
