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

## Mandatory repository-local team skills

The repository-local operating skills in `team/` are mandatory working instructions, not optional role descriptions.

Before any meaningful implementation, refactor, infrastructure, security, integration, AI, UX, data, or product-spec change:

1. Read `team/README.md` and `team/00-WORKING-AGREEMENT.md`.
2. Select the applicable role skill(s) from `team/*.skill.md`.
3. Read each selected skill before editing.
4. Declare the active skill IDs in the PR/change report.
5. Follow each selected skill's required procedure, evidence, stop conditions, and handoff.
6. Add specialist review skills required by the matrix in `team/00-WORKING-AGREEMENT.md`.
7. Apply `team.reviewer.v1` from `team/11-REVIEWER.skill.md` before merge.

### Absolute merge gate

**DO NOT MERGE without Reviewer Skill evidence for the current head SHA.**

A human or agent MUST NOT invoke a merge action unless all applicable conditions are true:

- `team.reviewer.v1` has produced an `APPROVE` verdict for the current head SHA;
- Critical findings = 0;
- High findings = 0;
- mandatory specialist reviews are complete;
- applicable verification/tests pass;
- CI is green for the exact head SHA;
- unresolved Medium findings are fixed or explicitly accepted by the project owner with rationale.

If the head SHA changes after review, re-run Reviewer Skill or explicitly review the delta and bind approval to the new SHA.

For Medium/High risk work, final review should be independent of the primary implementation. For High risk production changes, self-review does not count as final production approval.

### Skill selection guide

- cross-module architecture/platform primitives → `team.tech-lead.v1`;
- API/domain/repository/worker implementation → `team.backend.v1`;
- auth/tenancy/RLS/secrets/webhooks/security → `team.security.v1`;
- CI/CD/runtime/deploy/observability/recovery → `team.platform-sre.v1`;
- frontend behavior → `team.frontend.v1`;
- test/release evidence → `team.qa.v1`;
- business semantics/acceptance criteria → `team.product-domain.v1`;
- LLM/RAG/tools/evals → `team.ai-llm.v1`;
- external providers → `team.integration.v1`;
- material user workflow/UX → `team.ux.v1`;
- schema/migrations/RLS/performance/backup → `team.dba.v1`;
- every merge → `team.reviewer.v1`.

These repository-local skills complement `Bambale0/skills`; they do not replace the broader engineering playbook.

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
