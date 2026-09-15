# Test Strategy and Quality Gates

## 1. Goals

Testing must protect the product's highest-risk properties:

1. no cross-tenant leakage;
2. correct authorization;
3. deterministic workflow state;
4. no duplicate side effects under retries;
5. safe integration behavior;
6. traceable/auditable mutations;
7. vertical packs do not break universal core contracts.

## 2. Test pyramid

### Unit

Use for:

- domain rules;
- policy evaluation;
- score calculations;
- parsing/mapping;
- workflow condition/action logic;
- AI output schema validation.

### Integration

Use for:

- PostgreSQL repositories;
- RLS/tenant context;
- transactions/outbox;
- Redis/queue boundaries;
- authorization with real persistence;
- migration behavior.

### Contract

Use for every external provider adapter:

- request mapping;
- response mapping;
- webhook validation;
- error normalization;
- idempotency;
- rate limits;
- timeout/retry.

### End-to-end

Critical user journeys:

- inbound communication → Case → routing → WorkOrder → completion;
- incident linking;
- owner authorization/drill-down;
- admin config publication;
- integration sync/reconciliation.

### Smoke

Production-like deployment:

- app starts;
- health/readiness;
- DB connectivity;
- migration state;
- worker;
- critical configured integration health where safe.

## 3. Tenant isolation suite

Release-blocking tests.

Required cases:

- tenant A cannot read tenant B by ID;
- tenant A cannot search/list tenant B;
- tenant A cannot mutate tenant B;
- leaked object ID does not bypass;
- group membership permits only explicit organizations;
- revoked/expired membership fails;
- RLS blocks unsafe repository path;
- background job restores/validates tenant context;
- cache keys cannot cross tenants;
- exported/report data respects scope.

## 4. Authorization suite

Test permissions at backend boundary.

Examples:

- executor cannot manage roles;
- manager can reassign within configured scope;
- director can read organization metrics;
- group analyst cannot approve payment unless separately permitted;
- owner analytics permission does not imply integration-secret access.

## 5. Workflow tests

Cover:

- valid transitions;
- forbidden transitions;
- timer scheduling;
- warning;
- SLA breach;
- escalation;
- manual override audit;
- workflow version retention;
- retry;
- duplicate event consumption;
- restart/recovery.

## 6. Idempotency tests

For every external mutation:

```text
same operation delivered twice
→ one external/business effect
→ stable final state
```

Also test unknown-result/reconciliation behavior.

## 7. AI tests

Do not test stochastic prose only.

Test:

- structured schema validity;
- required field extraction;
- unsafe/low-confidence routing;
- authorization-filtered context;
- prompt injection boundaries;
- human correction capture;
- deterministic fallback when provider fails.

Maintain curated fixtures for representative inbound requests.

## 8. Vertical pack contract tests

Every vertical pack must pass common platform expectations:

- valid object types;
- valid case/work mappings;
- permissions resolve;
- workflow templates validate;
- UI capability manifest validates;
- no core import cycle introduced.

## 9. Migration tests

For meaningful migrations:

- upgrade from previous schema;
- application reads/writes after upgrade;
- backfill integrity;
- constraints/indexes;
- large-table impact considered;
- rollback or forward-fix approach documented.

## 10. Performance tests

Introduce focused load tests around real hot paths:

- inbound burst;
- large work queue;
- mass incident linking;
- owner dashboard aggregation;
- webhook bursts;
- queue worker throughput.

Do not optimize from imagined scale, but do not wait for production failure to test known burst paths.

## 11. CI gates

Minimum initial CI:

- Ruff;
- formatting check;
- mypy/type check;
- pytest;
- import/package check.

As infrastructure is added:

- PostgreSQL integration suite;
- migration check;
- tenant isolation suite;
- frontend lint/type/test;
- container build;
- dependency/security scan.

## 12. Regression rule

Every production bug should produce:

1. reproducible evidence;
2. failing regression test where feasible;
3. fix;
4. passing test;
5. telemetry improvement if diagnosis was difficult.

## 13. Test data

Never use real customer personal data in repository fixtures.

Use synthetic fixtures with clearly fake identifiers.

## 14. Definition of green

A green pipeline means the automated checks passed for the exact commit.

It does not mean production is healthy unless deployment and smoke checks were actually performed.
