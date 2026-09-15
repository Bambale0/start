# System Architecture

## 1. Architectural goal

Create one platform that can power isolated company applications and a cross-company owner layer without creating separate codebases per business.

## 2. High-level components

```text
Clients
├── Office Web
├── Manager Web
├── Owner Web
├── Executor Mobile/PWA
└── Admin Web
        │
        ▼
API / BFF Layer
        │
        ▼
┌────────────────────────────────────────────┐
│              Modular Monolith              │
│                                            │
│ Identity        Organizations              │
│ Authorization   People/Counterparties      │
│ Objects/Assets  Cases/Incidents            │
│ Work/Tasks      Workflow Engine            │
│ Documents       Finance Events             │
│ Communications  Integrations               │
│ Attention / Notifications                   │
│ Analytics       Audit                      │
│ Knowledge/Search Retrieval                  │
│ Vertical Packs  Owner Intelligence         │
└────────────────────────────────────────────┘
        │
        ├── PostgreSQL + pgvector
        ├── Redis/cache/coordination
        ├── Queue / background workers
        └── Object storage
                │
                ▼
Integration Hub
├── Accounting / 1C
├── EDO
├── Banks
├── Email
├── Telephony
├── MAX / Telegram / VK
└── Future adapters
```

## 3. Why modular monolith first

The early risk is incorrect domain boundaries, not traffic volume.

A modular monolith gives:

- one deployment unit;
- simpler transactions;
- easier refactors while domain knowledge grows;
- lower operational overhead;
- fast end-to-end testing.

Modules still require explicit APIs/contracts.

Direct cross-module table mutation is discouraged.

A future service extraction requires evidence such as:

- materially different scaling profile;
- security/isolation requirement;
- reliability blast-radius reduction;
- independent release need;
- dedicated team ownership;
- external contract boundary.

## 4. Suggested application layout

```text
apps/
  api/
  worker/
  office-web/
  owner-web/
  admin-web/

src/start/
  platform/
    identity/
    organizations/
    authorization/
    audit/
    events/
    configuration/

  domains/
    people/
    counterparties/
    objects/
    assets/
    cases/
    incidents/
    work/
    workflows/
    documents/
    finance/
    communications/
    analytics/
    knowledge/

  integrations/
    accounting/
    edo/
    banking/
    email/
    telephony/
    messaging/

  verticals/
    property_management/
    construction/
    fleet/

  intelligence/
    intake/
    extraction/
    routing/
    anomaly_detection/
    owner_assistant/
    retrieval/
    embeddings/
```

The initial scaffold may be smaller; this is the target dependency map.

## 5. Dependency rule

Dependencies flow inward:

```text
Provider Adapters / UI
        ↓
Application Services
        ↓
Domain
        ↓
Platform Primitives
```

Domain code must not import HTTP provider payloads or frontend concerns.

Vertical packs may depend on stable platform/domain extension points but must not make the universal core depend on a specific vertical.

## 6. Request context

Every authenticated request resolves an explicit context:

```text
Actor
Session
Selected Organization
Group Scope (when applicable)
Permissions
Correlation / Trace
```

A client cannot elevate access by changing an organization ID.

The API resolves authorized scope server-side from memberships.

## 7. Data architecture

Primary relational database: PostgreSQL.

Recommended early model: shared database + tenant-keyed rows + Row Level Security for tenant-bound data.

Reasons:

- efficient cross-organization owner queries under authorized group context;
- lower operational burden than database-per-tenant;
- transactional consistency;
- simpler analytics foundation.

See the tenancy ADR.

Separate schemas/databases can be added for regulated/special customers later behind repository boundaries.

## 8. Event architecture

Use explicit internal domain events.

Examples:

```text
case.created
case.classified
case.assigned

incident.created
incident.case_linked

work_order.started
work_order.completed
work_order.verified

sla.warning
sla.breached

document.received
document.approved
document.signed

financial_event.recorded
payment_request.approved

integration.sync_failed
```

Events include:

- event_id;
- event_type;
- version;
- organization_id when tenant-bound;
- aggregate_type/id;
- occurred_at;
- actor;
- trace/correlation IDs;
- payload.

Consumers must tolerate duplicates.

## 9. Transactional outbox

For events that trigger asynchronous work/external side effects, prefer a transactional outbox:

```text
DB transaction:
  business state
  + outbox event

commit
  ↓
outbox publisher
  ↓
queue
  ↓
consumer
```

This avoids “DB committed but event lost” failure modes.

## 10. Workflow engine

The workflow engine evaluates versioned definitions.

Conceptually:

```text
Trigger
→ Conditions
→ Actions
→ Assignment
→ Timers/SLA
→ Escalation
→ Completion policy
```

Important requirements:

- workflow definitions are versioned;
- running instances retain the definition/version they started with unless an explicit migration occurs;
- actions are idempotent;
- timers survive process restarts;
- every transition is auditable;
- human approval can be a first-class step;
- low-confidence AI results can route to review.

Workflow definitions are data, not arbitrary executable code from admins.

## 11. Configuration

Configuration classes:

### Infrastructure bootstrap

Environment/secret manager:

- database URL;
- Redis URL;
- encryption master/bootstrap material;
- observability exporters.

### Business runtime configuration

Database/control plane:

- statuses;
- categories;
- SLA;
- routing;
- enabled modules;
- channels;
- AI policies;
- templates;
- pack configuration;
- integration mappings.

Business configuration is versioned/audited where material.

## 12. AI architecture

AI capabilities are application services behind typed contracts.

Examples:

- classify inbound communication;
- extract address/person/problem;
- resolve entity candidates;
- detect duplicates;
- summarize;
- recommend routing;
- detect anomalies;
- answer owner questions over authorized structured context.

AI output schemas are validated.

AI never grants authorization or directly bypasses deterministic workflow policy.

## 12A. Two agent contours

Start uses two separate agent modes.

### Interactive Employee Agent

Triggered by an authenticated user instruction.

Primary behavior:

- search/read authorized structured data;
- search/read authorized knowledge;
- summarize/explain/compare;
- prepare drafts;
- propose actions.

It inherits the user's effective permissions and tenant/group scope.

Its tool surface is deliberately small and mostly read-only.

Writes are routed through a controlled Action Gateway that validates permission, tenant scope, deterministic business rules, idempotency and confirmation policy.

### Routine Automation Agent

Triggered by configured workflow/event templates.

It receives a bounded task envelope:

- tenant scope;
- triggering entity/event;
- allowed evidence;
- expected structured output;
- agent policy/version;
- tool/time/cost budget.

It primarily reads context and returns a structured decision/proposal to Workflow Engine. Deterministic application services perform mutations.

Examples:

- classify request;
- extract address/person/problem;
- propose routing;
- detect likely duplicate/Incident;
- summarize document;
- draft resident notification;
- classify legal correspondence.

### Tool design

Prefer a few stable capability classes over a large entity-by-entity tool catalog.

Conceptually:

- business search/read;
- knowledge search;
- timeline read;
- metrics read;
- draft creation;
- controlled action proposal.

Adding a new entity should not automatically create a new direct LLM tool.

See ADR 0008.

## 13. Owner intelligence

Owner Control consumes normalized data from organizations under an authorized group.

It should rely on:

- metrics/aggregates;
- anomalies;
- alerts;
- evidence-backed summaries;
- drill-down links.

Do not make owners query every tenant operational table directly from the browser.

Server-side authorization and aggregation are mandatory.

## 14. Background jobs

Long-running work runs outside request handlers.

Examples:

- provider sync;
- document parsing;
- AI processing;
- notification delivery;
- SLA timers;
- reconciliation;
- analytics materialization.

Queue implementation is an infrastructure choice behind an abstraction and may evolve without changing domain APIs.

## 14A. Realtime attention and notifications

Domain/integration events may produce scoped AttentionEvents.

~~~text
Domain / Integration Event
        ↓
NotificationPolicy
        ↓
recipient resolution
        ↓
AttentionEvent
        ↓
realtime in-app + configured channels
        ↓
ACK / durable escalation timer
~~~

Urgent operational information should reach authorized users without manual page refresh.

The platform must distinguish:

- event occurred;
- notification queued;
- provider accepted;
- delivered when known;
- read/acknowledged when known.

The engine supports grouping and anti-noise so a mass Incident does not generate uncontrolled notification storms.

See `REALTIME_NOTIFICATIONS.md`.

## 15. Caching

Cache is derivative only.

Never place the only copy of business state in Redis.

Cache keys involving tenant data must include safe scope/version information.

Permission/configuration caches require explicit invalidation/versioning.

## 16. API design

Initial direction: REST/JSON with typed OpenAPI contracts.

Guidelines:

- resource IDs are opaque;
- tenant scope is derived/validated server-side;
- mutations support idempotency where retries are plausible;
- pagination is mandatory for collections;
- filtering/sorting are explicit;
- API errors are structured and traceable;
- provider raw payloads do not leak into core API contracts.

## 17. File/document storage

Binary artifacts live in object storage.

PostgreSQL stores metadata, access rules, checksums, provider references and relationships.

Sensitive documents use signed/short-lived access.

## 17A. Knowledge and retrieval architecture

Unstructured information is indexed through a derived Knowledge/Retrieval layer.

~~~text
Document / Communication / Domain Entity
        ↓
authoritative metadata + access policy
        ↓
parse / normalize
        ↓
versioned chunks
        ↓
embeddings
        ↓
PostgreSQL full-text + pgvector
        ↓
authorized hybrid retrieval
        ↓
optional rerank
        ↓
evidence-backed AI / user search
~~~

Rules:

- original files remain in object storage or their external system of record;
- document metadata/permissions remain authoritative in PostgreSQL;
- vector/text indexes are derivative and rebuildable;
- every tenant-bound chunk carries organization_id directly;
- access filtering happens before evidence enters AI context;
- embedding model, chunking and ranking policies are configuration/versioned data;
- source checksum/version controls freshness and reindex;
- deletion/revocation must make indexed evidence inaccessible immediately/fail closed;
- the retrieval implementation sits behind a provider-agnostic port.

Initial vector implementation is pgvector in the existing PostgreSQL topology. A dedicated vector service may replace the storage adapter later if measured scale/reliability/latency justifies it.

See ADR 0007.

## 18. Frontend architecture

Treat Office/Admin and Owner Control as different UX surfaces over shared APIs.

The same person may have access to several surfaces depending on membership.

Company branding/navigation is capability-driven.

Do not create one giant menu and hide items only in the browser; backend authorization remains authoritative.

## 19. Availability and degradation

External provider failure must not collapse unrelated platform functions.

Examples:

- EDO unavailable → queue/surface sync state; operations not needing EDO remain usable.
- AI unavailable → deterministic/manual fallback where configured.
- messenger unavailable → case remains; delivery status is visible.
- accounting sync unavailable → cached mirrored data marked stale; no fabricated freshness.

## 20. Architecture review triggers

Review/ADR required when changing:

- tenant model;
- authentication model;
- source-of-truth boundaries;
- workflow semantics;
- event envelope;
- external write authority;
- AI authority level;
- core-vs-vertical boundary;
- database topology;
- service decomposition.
