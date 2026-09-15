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

## Mandatory feature preflight and execution ledger

Before implementing **any feature**, the agent/developer MUST perform a fresh audit of the repository state relevant to that feature. Do not rely on an old plan or assume a documented capability already exists.

### Pre-feature audit

Inspect at minimum:

- current `CONTEXT.md` active-feature section;
- relevant specs and ADRs;
- current domain/application/API code;
- database models and latest migrations;
- authorization/tenant enforcement;
- admin/configuration surfaces;
- existing tests at the intended seams;
- E2E and smoke coverage;
- CI workflow;
- integration adapters involved;
- logs/metrics/traces for an existing runtime path, if one exists;
- open/closed issues that overlap the feature.

Record the audit in `CONTEXT.md` **before writing production code**.

The audit must state:

1. what already exists;
2. what is partial;
3. what is missing;
4. what can be reused;
5. what must be prefactored first;
6. architecture/security/tenant risks;
7. migrations/integration impact;
8. agreed public test seams;
9. exact feature plan and acceptance criteria.

### CONTEXT.md is the live execution ledger

For the feature currently being implemented, `CONTEXT.md` must contain an **Active Feature Execution** section with:

- feature/ticket/spec;
- audit baseline and commit SHA;
- dependencies/blockers;
- intended user-visible outcome;
- no-hardcode/configuration decisions;
- schema/API/UI changes;
- permissions and tenant scope;
- observability plan;
- test seams;
- unit/integration/contract/E2E/smoke plan;
- migration/rollout plan;
- numbered implementation steps;
- progress log with completed steps and evidence;
- final verification results;
- follow-ups.

Update this section step-by-step during implementation. Do not wait until the end and reconstruct history from memory.

When the feature is complete, move the final concise outcome into the execution history section and prepare `Active Feature Execution` for the next feature.

### No-hardcode gate

Before implementation and again during review, explicitly check that the feature does not hardcode mutable business values.

If a value may differ by organization, vertical, business unit or operational policy, it should normally be:

- typed configuration;
- database-backed;
- scoped;
- validated;
- editable in the appropriate admin/control plane;
- versioned/audited when material.

A feature is incomplete if routine behavior still requires source editing or manual SQL.

### Test-first vertical slices

Use the repository's pre-agreed testing seams:

1. **HTTP/API seam** for user-visible backend behavior;
2. **domain/application service seam** for complex deterministic business rules when the API seam would be too broad;
3. **provider adapter seam** for third-party contracts;
4. **browser/user-journey seam** for E2E;
5. **deployed service seam** for smoke.

Each implementation ticket should be a tracer-bullet vertical slice where possible:

`failing behavior test → minimal implementation → focused checks → next slice`.

Do not write a horizontal pile of implementation-detail tests before the behavior exists.

### Mandatory verification layers

Every feature must explicitly decide and document all of the following, even if one is genuinely not applicable:

- unit/domain behavior;
- database/repository integration;
- authorization and tenant isolation;
- migrations;
- external adapter contract;
- workflow/idempotency/retry behavior;
- API integration;
- E2E user journey;
- smoke/deployability;
- observability/audit;
- no-hardcode/admin configurability.

"Not applicable" requires a reason in `CONTEXT.md`.

### Feature completion gate

A feature cannot be marked done until:

- its acceptance criteria pass;
- focused tests pass;
- full backend/frontend test suite appropriate to the changed surface passes;
- tenant-isolation/security checks pass;
- E2E for the primary happy path and critical failure/permission path passes;
- smoke checks pass in a production-like environment or the repository's defined smoke environment;
- CI is green for the exact commit;
- code review against both repository standards and originating spec is complete;
- documentation and `CONTEXT.md` contain actual verification evidence;
- no unresolved high-severity finding remains.

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

---

## Shared Engineering Baseline — Start + AuRoom

This shared baseline supplements repository-specific rules; it never replaces stricter local architecture, release, security, channel, or product constraints.

### Engineering playbook and task flow
- Treat `Bambale0/skills` as the primary engineering playbook. Also inspect relevant safe guidance from `Bambale0/claw` and `anthropics/skills`.
- Do not use deprecated skills. Use in-progress skills only when they fit and account for their experimental status.
- Large ambiguous work: use a wayfinder-style flow.
- Feature development where applicable: `grill-with-docs → to-spec → to-tickets → implement → tdd → code-review`.
- Debugging: diagnose from evidence first (logs, telemetry, DB/runtime state, reproducible behavior), then patch.
- Never claim tests, CI, deploy, or production state that was not actually verified.

### Mandatory feature preflight and CONTEXT ledger
Before implementing any material feature or cross-cutting refactor, perform a fresh audit of the current repository state. Inspect relevant docs/specs/ADRs, code, schemas/migrations, auth, admin/config surfaces, tests, CI, integrations, and runtime telemetry when available.

Use the repository-designated execution ledger for active work. If `CONTEXT.md` is explicitly documented as that ledger, maintain it. If `CONTEXT.md` already serves another purpose, do not repurpose it; use an existing repository-local ledger path or create `docs/agents/EXECUTION.md`. Record baseline commit/SHA, current state, what exists/partial/missing/reusable, risks/dependencies, migrations/integrations/permissions/rollout impact, intended user outcome and acceptance criteria, no-hardcode/configuration decisions, observability plan, test seams, numbered steps with progress evidence, final verification, and follow-ups. Do not reconstruct it only at the end.

### No hardcode and control plane
Mutable business/runtime behavior must not require source edits, manual SQL, or redeploys. Prices, tariffs, categories, statuses, SLA, prompts, provider/model selection, routing, thresholds, schedules, feature availability, notification templates, retry/fallback policy, permissions, and integration mappings should normally be typed, validated, database-backed, scoped, auditable, and manageable through the appropriate authenticated admin/control plane.

Secrets are not business configuration. Never expose plaintext secrets in frontend bundles, logs, API responses, Git, or ordinary database settings.

### Architecture and integrations
- Prefer a modular monolith with explicit module interfaces and seams unless scaling, security, reliability, or ownership evidence justifies extraction.
- Important cross-module state changes should use explicit, typed, versionable, traceable, retry-safe/idempotent events where eventing is appropriate.
- Keep provider-specific HTTP payload handling behind typed integration adapters/ports.
- External integrations must define auth, finite timeouts, bounded retries/backoff, rate-limit behavior, idempotency, webhook verification where supported, reconciliation, data ownership/sync direction, observability, and failure semantics.
- Avoid parallel sources of truth.

### Security and AI authority
Authorization is enforced server-side. UI hiding is never sufficient. Preserve ownership/tenant boundaries where applicable and treat data leakage as a release blocker.

AI may classify, summarize, extract, recommend, and execute only explicitly permitted workflows. It must not bypass authorization, approvals, deterministic validation, financial controls, legal signing, or tenant/data isolation. Low-confidence or high-impact actions should fail closed or escalate.

### Observability first
Logging and telemetry are part of the implementation. Critical paths should expose what happened, when, for which actor/entity/scope, through which provider, duration, retries, failure reason, and user-visible effect. Propagate useful request/trace/correlation IDs. Never log secrets or unnecessary personal data.

### Test-first vertical slices and completion gate
Prefer `failing behavior test → minimal implementation → focused checks → next slice`.

For every material feature, explicitly cover where applicable: unit/domain behavior, DB/repository integration and migrations, authorization/ownership/tenant isolation, provider contracts, workflow/idempotency/retry, API integration, browser/bot E2E, smoke/deployability, observability/audit, and admin configurability/no-hardcode.

Regression fixes should get regression tests when feasible. Do not mark work complete until applicable acceptance criteria and checks pass; when repository CI exists and is accessible, it is green for the exact commit; review against repository standards and the originating spec is complete; and no unresolved high-severity finding remains. If CI is unavailable or the repository has no CI, record that explicitly and run the closest available local checks instead.

### Delivery
Final engineering reports should state what changed; important files/components; skills/flows used; exact tests/checks and results; migrations/config/admin changes; risks/follow-ups; and PR/commit/deploy SHA when applicable.
