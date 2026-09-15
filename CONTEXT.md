# Product Context, Current State and Execution Ledger

This file is the canonical live context for product and implementation work.

It serves four purposes:

1. shared domain vocabulary;
2. honest audit of what is actually implemented;
3. master implementation order;
4. live per-feature execution ledger.

Before implementing any feature, update **Active Feature Execution** with a fresh audit and detailed plan.

---

# 1. Product

**Start** is an AI-enabled multi-company Business Operating System.

It is not a single-company CRM and not an ERP replacement.

It provides:

- isolated company workspaces;
- global identity with scoped memberships;
- universal workflow/case/task/asset primitives;
- vertical industry packs;
- integration orchestration;
- role-specific interfaces;
- cross-company Owner Control;
- management intelligence;
- an authorized knowledge/retrieval layer for large document and communication corpora.

The first vertical is **Property Management**, designed generically for управляющие организации / ЖСК / ТСЖ and similar operators.

No customer/company name belongs in the universal core or Property Management contract.

---

# 2. Core hierarchy

~~~text
Group
└── Organization
    └── BusinessUnit
        └── Object / Project / Location
            └── Process / Case / Incident / WorkOrder / Task
~~~

Not every organization needs every level.

---

# 3. Canonical terms

## Group
Management/ownership aggregation of organizations.

## Organization
Company or independent operational/legal business boundary. Organization is a tenant and security boundary.

## BusinessUnit
Department, branch, region, team, service line or operational subdivision.

## User
Global authenticated identity. A User has no business access merely by existing.

## Membership
Connects User to Group / Organization / BusinessUnit scope with explicit permissions.

## Role / Permission
Role is a reusable permission bundle. Permission is an atomic backend capability. Contextual policy can narrow access.

## Person
Business person record: resident, customer, applicant, employee contact, driver, etc. Not automatically an authenticated User.

## Counterparty
External legal entity / entrepreneur / contractor / supplier.

## Object
Managed business context, e.g. Building, Premise, ConstructionSite, Depot.

## Asset
Physical/logical resource with lifecycle/state/cost history.

## Communication
Normalized email, message, call, web submission or notification.

## Case
Business item requiring handling and history.

## Incident
Shared operational event affecting many Cases/Objects/People.

## WorkOrder
Executable work assigned to a person/team/contractor.

## Task
Smaller actionable unit linked to another business process/entity.

## Workflow
Versioned process logic:
~~~text
trigger → conditions → actions → assignment → SLA/timers → escalation → result
~~~

## Document
Business document metadata and authoritative storage/provider reference.

## FinancialEvent
Normalized management fact/intent about money. Not a statutory accounting entry by default.

## KnowledgeSource
Reference to an authoritative Document, Communication or other business entity that can be indexed for retrieval.

## KnowledgeChunk
Derived, rebuildable text segment used for lexical/semantic search. It carries tenant/permission scope and source version metadata.

## EmbeddingRecord
Derived vector representation of a KnowledgeChunk. It is never a source of truth.

## Vertical Pack
Configuration/extension package mapping universal primitives to an industry.

Initial packs:
- Property Management;
- Construction;
- Fleet / Service.

## Interactive Employee Agent
Human-invoked read-first agent operating under the invoking user's exact permissions. It searches structured business data and Knowledge, explains/summarizes/compares, creates drafts, and may only request mutations through the controlled Action Gateway.

## Routine Automation Agent
Workflow/event-invoked read-first agent with a bounded task envelope, structured output and configured budgets. It proposes classifications/decisions/drafts; deterministic workflow/application services perform state changes.

## Action Gateway
Single controlled path for agent-initiated writes. It validates tenant scope, permission, business rules, idempotency and confirmation/approval policy before calling normal application services.

## AttentionEvent
A scoped signal that a business/integration event requires human awareness or acknowledgement. Delivery policy is configurable and may use realtime in-app, messenger, email, push or fallback/escalation channels.

## NotificationPolicy
Versioned tenant configuration defining severity, recipients, immediate/digest behavior, acknowledgement, escalation, fallback channels, quiet hours and grouping. No urgent timing/recipient/channel values are hardcoded.

## Owner Control
High-level UX for founders/owners/group managers focused on money, risk, deviations, assets, projects, contractors and decisions.

---

# 4. Current implementation audit

**Audit baseline:** main at `c87b39a03edf15db21a0d009740d83dfd94f40c9` for repository state review. Documentation-only commits may advance main without changing implemented runtime capabilities.

## Actually implemented

### Application foundation
- Python package;
- FastAPI application factory;
- `/health/live`;
- `/health/ready`;
- typed Pydantic settings;
- structured logging bootstrap;
- Dockerfile;
- Docker Compose with API/PostgreSQL/Redis foundation.

### Platform primitives
- `RequestContext`;
- explicit organization-context check;
- explicit permission check helper;
- generic `DomainEvent` envelope.

### Quality/tooling
- Ruff;
- mypy strict;
- pytest;
- GitHub Actions CI;
- compile/lint/format/type/test checks;
- basic health and RequestContext tests.

### Documentation/architecture
- Product spec;
- Property Management spec;
- Owner Control spec;
- Admin Control Plane spec;
- security/integration/observability docs;
- test strategy;
- ADRs;
- implementation roadmap;
- engineering rules;
- accepted ADR for a derived knowledge index with PostgreSQL + pgvector first.

## Partially implemented

### Tenant / authorization
Only request-context primitives exist.

Missing:
- persisted users/groups/organizations;
- memberships;
- roles/permissions;
- authentication/session management;
- PostgreSQL RLS;
- tenant-aware repositories;
- admin access management.

### Observability
Structured logger bootstrap exists.

Missing:
- request IDs;
- trace propagation;
- OpenTelemetry;
- persistent audit;
- business metrics;
- dashboards/alerts.

### Infrastructure
PostgreSQL and Redis containers exist.

Missing:
- SQLAlchemy persistence;
- Alembic;
- DB readiness;
- background queue;
- object storage;
- production deploy;
- backup/restore verification.

## Not implemented

No Property Management business feature is implemented.

Also not implemented:
- vector extension/schema;
- document parsing/chunking;
- embeddings;
- hybrid retrieval;
- RAG/knowledge search;
- browser E2E suite;
- production-like smoke suite.

## Important rule

Documentation describes target behavior; it must never be interpreted as proof that the capability already exists.

---

# 5. Mandatory implementation lifecycle

Every feature follows this process.

## Step 0 — fresh audit before production code

Inspect:
- current branch/tree and latest commit;
- `CONTEXT.md`;
- relevant spec/ADR;
- overlapping implementation;
- latest migrations;
- permissions/tenant enforcement;
- admin/configuration behavior;
- tests at public seams;
- E2E/smoke coverage;
- CI;
- integrations involved;
- logs/metrics if runtime exists;
- related issues.

Record:
1. exists;
2. partial;
3. missing;
4. reusable;
5. prefactor needed;
6. risks;
7. schema/migration impact;
8. integration impact;
9. agreed test seams;
10. exact implementation plan.

## Step 1 — detailed feature plan

Before code, document in **Active Feature Execution**:
- user-visible outcome;
- dependencies/blockers;
- schema;
- API;
- UI;
- configuration/admin;
- permissions/tenant scope;
- events/workflows;
- observability/audit;
- migrations/rollout;
- tests;
- E2E;
- smoke;
- acceptance criteria.

## Step 2 — no-hardcode gate

Anything that may differ by organization/process is configuration-driven unless proven immutable.

Examples:
- case categories/statuses/priorities;
- SLA/routing/escalation;
- chat trigger rules;
- required form fields;
- notification templates/channels;
- asset/planned-work/legal-document types;
- estimate lifecycle;
- AI provider/model/prompt/confidence policy;
- embedding provider/model;
- chunking strategy;
- retrieval weights;
- report definitions.

Runtime business configuration must be typed, validated, tenant-scoped and manageable through the control plane.

## Step 3 — vertical slice + TDD

Preferred seams:
1. HTTP/API;
2. domain/application service for complex deterministic logic;
3. provider adapter contract;
4. browser/user journey;
5. deployed smoke seam.

Loop:
~~~text
RED behavior test
→ minimal implementation
→ GREEN
→ focused checks
→ update CONTEXT progress
→ next tracer bullet
~~~

## Step 4 — mandatory verification matrix

Every feature explicitly covers or marks N/A with reason:
- unit/domain;
- repository/DB integration;
- migration;
- authorization;
- tenant isolation/RLS;
- workflow/state;
- idempotency/retry;
- provider contract;
- API integration;
- E2E happy path;
- E2E permission/error path;
- smoke;
- logs/metrics/audit;
- no-hardcode/admin configurability.

## Step 5 — review

Two-axis review:
- repository standards;
- originating spec/ticket.

No unresolved high-severity finding.

## Step 6 — close execution ledger

Record:
- exact commit/PR;
- test commands/results;
- E2E result;
- smoke result;
- migrations;
- tenant/security verification;
- CI run;
- known limits;
- follow-ups.

---

# 6. Master implementation order

Detailed per-feature plans live in `docs/roadmap/FEATURE_IMPLEMENTATION_PLAN.md`.

Required order:

~~~text
F00 Runtime/Test Foundation
↓
F01 Identity / Tenancy / Authorization / RLS
↓
F02 Configuration + Admin Control Plane
↓
F03 Universal Domain Core
↓
F04 Events / Outbox / Workflow / SLA
↓
F05 Knowledge & Retrieval / pgvector
↓
A01 Shared Agent Runtime / Action Gateway
↓
A02 Interactive Employee Agent
↓
A03 Routine Automation Agent
↓
C01 Realtime Attention / Notification Engine
↓
Property Management vertical slices
↓
Integration Hub
↓
Manager / Director Control
↓
Owner Control
↓
Second Vertical
↓
Cross-company Intelligence
~~~

Foundational tickets may overlap only when their security/data dependencies are explicit.

---

# 7. Active Feature Execution

## Feature

**F00 — Runtime/Test Foundation**

Status: **PLANNED — implementation not started in this execution ledger.**

## Audit baseline

Current runtime has only FastAPI scaffold, health endpoints, typed settings, structured logger bootstrap, RequestContext/DomainEvent primitives and basic CI/tests.

Missing:
- SQLAlchemy persistence;
- Alembic;
- real PostgreSQL integration tests;
- pgvector extension verification;
- request correlation middleware;
- persistent audit;
- E2E harness;
- production-like smoke harness;
- container build check;
- migration check;
- DB readiness.

## User/developer outcome

After F00, every later feature can be built against repeatable database, migration, E2E and smoke infrastructure instead of adding ad-hoc test setup per feature.

## Planned changes

1. add async SQLAlchemy engine/session boundary;
2. add Alembic baseline;
3. use PostgreSQL image/environment capable of pgvector extension;
4. add migration enabling `vector` extension, but no knowledge tables yet;
5. add DB-backed readiness;
6. add request/correlation middleware;
7. add persistent AuditEvent skeleton or explicitly defer persistence to F01 with a tested interface;
8. create integration-test database fixture;
9. create deterministic synthetic tenant/test data factory;
10. add E2E harness;
11. add smoke harness against built container;
12. add container build + migration + smoke jobs to CI.

## No-hardcode decisions

- database/Redis URLs from settings;
- test DB credentials isolated to CI/dev;
- no production credentials;
- vector dimensions are not defined in foundation;
- no embedding model is selected in source;
- no tenant/business config in environment constants.

## Test seams

- application HTTP seam;
- database session/repository infrastructure seam;
- built Docker service seam.

## Planned verification

### Unit
- settings parsing where meaningful;
- correlation/context helpers.

### Integration
- Postgres connection;
- transaction rollback fixture;
- vector extension present;
- migration from empty DB;
- DB readiness failure/success.

### E2E
- launch app against clean Postgres;
- liveness/readiness;
- correlation header round-trip.

### Smoke
- build image;
- boot API + Postgres + Redis;
- run migrations;
- health/readiness returns healthy.

### CI
- compile;
- Ruff;
- mypy;
- pytest unit/integration;
- migration check;
- Docker build;
- smoke.

## Acceptance criteria

- clean environment reaches green state using documented commands;
- migrations create the same schema consistently;
- pgvector extension availability is verified;
- tests never rely on developer machine state;
- CI verifies exact commit;
- no business feature is added during F00.

## Progress log

- 2026-09-15: repository audit completed.
- 2026-09-15: mandatory feature-audit and execution-ledger process added to AGENTS.md.
- 2026-09-15: vector knowledge layer accepted architecturally via ADR 0007.
- Implementation has not started yet.

---

# 8. Execution history

No business feature has been completed yet under the mandatory execution-ledger process.
