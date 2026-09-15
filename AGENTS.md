# AGENTS.md — Start / Business OS Repository Instructions

## Mission

Build a production-grade, multi-company Business Operating System that removes routine operational work, keeps company data isolated, integrates existing business systems, and gives owners a safe cross-company control layer.

Prefer small, reviewable, tested changes over broad rewrites.

## Mandatory engineering playbook

Before any meaningful development, debugging, refactor, architecture or deployment task:

1. Read this `AGENTS.md`.
2. Read the relevant repository docs, especially architecture/spec/ADR files.
3. Treat `Bambale0/skills` as the primary engineering playbook.
4. Automatically select the relevant skill/flow for the task.
5. Use `in-progress` skills only when they fit the task and account for their experimental status.
6. Do not use deprecated skills.
7. For large ambiguous work, use the wayfinder-style flow.
8. For feature development, follow the user's preferred route where applicable:
   `grill-with-docs → to-spec → to-tickets → implement → tdd → code-review`.
9. For debugging, start with diagnosis/evidence before patching.
10. Do not claim a check, test, deployment or production state that was not actually verified.

If the skills repository cannot be accessed, state that fact rather than pretending its guidance was applied.

## Repository discovery before editing

Inspect the evidence relevant to the task before changing code:

- README and nearby docs;
- ADRs;
- existing domain models;
- database migrations;
- API schemas/routes;
- frontend patterns;
- integrations;
- authorization model;
- tests;
- Docker/deployment configuration;
- CI workflows;
- logs and telemetry for runtime problems.

Never invent an API field, database column, external payload, environment variable or deployment assumption.

## Non-negotiable product boundaries

### Universal core

The core MUST remain industry-agnostic.

Core entities may include concepts such as:

- Group;
- Organization;
- BusinessUnit;
- Membership;
- Person;
- Counterparty;
- Object;
- Asset;
- Case;
- Incident;
- WorkOrder;
- Task;
- Workflow;
- Contract;
- Document;
- FinancialEvent;
- Communication;
- Metric;
- Alert;
- AuditEvent.

Do not put `House`, `ResidentComplaint`, `PlumberTicket`, `ConstructionDefect` or similar vertical concepts into the universal core. Such concepts belong to vertical packs.

### Vertical packs

Vertical packs extend/configure the core. They MUST NOT become separate products with duplicated identity, authorization, workflow, document, finance, integration or analytics logic.

### Tenant isolation

Every company/organization is a hard security boundary.

Cross-company access exists only through explicit group/company memberships and permissions. Never trust a client-supplied `organization_id` by itself.

Tenant isolation must be enforced at multiple layers, including database-level controls where supported.

### Global owner access

Owners use the same global identity system as everyone else. `OWNER` is not a magical hardcoded root account.

Owner capabilities are explicit permissions scoped to groups/organizations. Sensitive actions can require step-up authentication.

### One source of truth

Do not create parallel sources of truth.

Examples:

- statutory accounting remains mastered by 1C/accounting systems;
- legally significant document originals remain mastered by the EDO provider;
- actual account balances/transactions remain mastered by the bank;
- Start masters operational workflows, configuration, audit and management intelligence.

### No hardcoded mutable business configuration

Mutable business/runtime values must not be buried in source code.

This includes:

- categories;
- statuses;
- SLA;
- priorities;
- routing rules;
- schedules;
- escalation thresholds;
- AI prompts;
- confidence thresholds;
- enabled channels;
- feature availability;
- integration mappings;
- prices/tariffs;
- roles/permissions;
- notification templates;
- provider/model selection;
- retry/fallback policies that operations may tune.

Use typed database-backed configuration and expose appropriate management through the admin/control plane.

Secrets belong in a secure secret mechanism, never Git or plaintext application tables.

## Architecture rules

### Start as a modular monolith

Begin as a modular monolith with explicit domain boundaries and event contracts.

Do not split into microservices merely because a module exists. Extract a service only when there is a demonstrated scaling, reliability, security or ownership reason.

### Event-driven internal boundaries

Important domain state changes should emit explicit events.

Events must be:

- typed;
- versionable;
- traceable;
- idempotently consumable;
- safe for retries.

Avoid hidden cross-module database writes.

### Integration adapters

All third-party systems sit behind typed ports/adapters.

No domain service should contain provider-specific HTTP payload handling.

Every external integration must define:

- authentication;
- timeouts;
- retries/backoff;
- rate-limit handling;
- idempotency;
- webhook verification where supported;
- data ownership;
- sync direction;
- reconciliation behavior;
- observability;
- failure semantics.

### AI is not an authority boundary

LLMs may classify, summarize, extract, recommend and execute explicitly allowed workflows.

Do not let AI bypass authorization, financial approval, legal signing, tenant isolation or deterministic validation.

Low-confidence or high-impact decisions fail closed/escalate to a human.

## Web/admin control plane

The platform must expose safe management surfaces for mutable entities.

A feature that requires editing source code, manual SQL or redeploying to change routine business behavior is incomplete unless the behavior is genuinely immutable technical configuration.

For applicable entities provide:

- list/search/filter;
- details;
- create/edit;
- enable/disable/archive;
- validation;
- change history;
- actor/audit metadata;
- safe secret replace/rotate/test workflows.

## Observability-first rule

Logging and telemetry are not follow-up work.

Every critical workflow and integration should make it possible to answer:

- what happened;
- when;
- for which tenant;
- for which actor;
- in which workflow/process;
- which external provider was involved;
- how long it took;
- whether it retried;
- why it failed;
- what user-visible effect occurred.

Propagate `request_id`, `trace_id`, `organization_id`, relevant entity IDs and integration correlation IDs.

Never log secrets or unnecessary personal data.

## Testing requirements

Every material change must include the appropriate tests.

Use, where applicable:

- unit tests for domain rules;
- integration tests for repositories and boundaries;
- contract tests for external adapters;
- migration tests;
- authorization/tenant-isolation tests;
- workflow transition tests;
- idempotency/retry tests;
- end-to-end tests for key user journeys;
- smoke tests for deployability.

A regression fix requires a regression test whenever technically feasible.

Tenant leakage is a release blocker.

## Database and migration rules

- PostgreSQL is the canonical relational store unless an ADR changes it.
- Migrations are reviewed as production changes.
- Prefer expand/migrate/contract for breaking schema evolution.
- Avoid destructive migrations in the same release as code that still relies on old data.
- Add indexes intentionally and verify query shape for high-volume paths.
- Use database constraints for critical invariants where practical.

## Security rules

Never commit:

- tokens;
- credentials;
- private keys;
- customer exports;
- production dumps;
- real personal data.

High-privilege accounts require strong authentication. Owner/group access requires MFA/passkeys as product maturity allows.

Sensitive actions require explicit authorization and complete audit history.

## Performance/reliability

Network calls require finite timeouts.

Retries must be bounded and used only where safe.

Mutating external operations require idempotency/reconciliation.

Avoid request-path blocking for long-running operations; queue/background execution with observable state.

## Delivery workflow

For each change:

1. discover and understand;
2. state the intended behavior/spec;
3. implement the smallest coherent vertical slice;
4. add/update tests;
5. run focused checks;
6. run broader checks appropriate to the changed surface;
7. review for tenant/security/configuration/observability regressions;
8. update docs/ADRs when architecture or public behavior changes.

## Definition of done

A task is done only when all applicable statements are true:

- relevant `Bambale0/skills` guidance was considered;
- architecture boundaries remain intact;
- no mutable business value was newly hardcoded;
- tenant isolation is preserved;
- authorization is explicit;
- external calls are bounded/observable;
- appropriate tests pass;
- regression tests exist for fixed bugs where feasible;
- logs/metrics/traces support production diagnosis;
- secrets and sensitive data are not exposed;
- docs/specs/ADRs match the implementation;
- the exact tested state is reported.

## Delivery report

Completed engineering work should state:

1. what changed;
2. important files/components;
3. skills/flows used;
4. tests/checks and actual results;
5. migrations/config/admin changes;
6. risks/follow-ups;
7. PR/commit/deploy SHA when applicable.
