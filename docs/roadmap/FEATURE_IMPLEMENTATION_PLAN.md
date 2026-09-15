# Feature-by-Feature Implementation Plan

This document is the master delivery plan for Start.

It is not a substitute for the per-feature audit in `CONTEXT.md`.

Before implementing any feature listed here:

1. audit the current repository state;
2. update `CONTEXT.md / Active Feature Execution`;
3. confirm the public test seams;
4. implement in tracer-bullet vertical slices;
5. run the full verification matrix;
6. perform standards + spec review;
7. record actual evidence in `CONTEXT.md`.

No feature is complete because "the code exists". It is complete only after verified behavior, tenant isolation, E2E, smoke and CI.

---

# Global rules for every feature

## No hardcode

Business values that can vary by organization/process must be persisted configuration, not source constants.

Applies to:

- categories;
- statuses;
- priorities;
- forms;
- SLA;
- routing;
- schedules;
- escalation;
- notification templates/channels;
- bot triggers;
- feature availability;
- roles/permissions;
- AI policies;
- embedding models;
- chunking/retrieval policies;
- legal document types;
- asset types;
- planned-work types;
- estimate states;
- report definitions.

## Required checks

Each feature must explicitly address:

- unit/domain;
- DB integration;
- migration;
- authorization;
- tenant isolation / RLS;
- workflow/state transitions;
- idempotency/retry if relevant;
- external adapter contract if relevant;
- API integration;
- E2E happy path;
- E2E permission/failure path;
- smoke;
- logs/metrics/audit;
- admin configurability.

---

# FOUNDATION

## F00 — Runtime and Test Foundation

### Outcome
All later features share repeatable database, migration, E2E and smoke infrastructure.

### Implementation
1. async SQLAlchemy engine/session;
2. Alembic baseline;
3. PostgreSQL + pgvector-capable local/test image;
4. enable vector extension;
5. DB readiness;
6. correlation/request middleware;
7. test DB fixtures;
8. synthetic data factories;
9. E2E harness;
10. smoke harness;
11. Docker build verification;
12. CI migration/smoke jobs.

### Tests
- settings unit tests;
- DB connect/rollback integration;
- migration empty → head;
- migration repeated environment;
- pgvector extension availability;
- readiness healthy/unhealthy;
- E2E boot + health;
- smoke built image + clean DB.

### Gate
No business behavior added.

---

## F01 — Identity, Tenancy, Memberships and Authorization

### Outcome
One global identity can safely access one or many organizations without cross-tenant leakage.

### Implementation
1. User;
2. Group;
3. Organization;
4. BusinessUnit;
5. Membership;
6. Role;
7. Permission;
8. auth/session foundation;
9. organization/group context selection;
10. authorization policy service;
11. tenant-aware repository base;
12. PostgreSQL RLS;
13. audit access changes;
14. access-management endpoints/admin slice.

### Tests
- policy unit tests;
- persistence integration;
- migration;
- RLS direct DB tests;
- tenant A cannot list/read/update/delete B;
- leaked UUID denied;
- revoked/expired membership denied;
- group membership scope;
- privilege escalation attempts;
- E2E login → organization switch;
- E2E forbidden cross-tenant URL;
- smoke ordinary + privileged session.

### Gate
Tenant leakage = release blocker.

---

## F02 — Configuration and Admin Control Plane Foundation

### Outcome
Operational behavior changes without source edits or manual SQL.

### Implementation
1. typed configuration registry;
2. tenant/group scope;
3. versioning;
4. draft/publish;
5. validation;
6. audit;
7. admin CRUD;
8. import/export without secrets;
9. feature/capability flags;
10. secret references.

Initial configurable classes:
- entity types;
- categories;
- statuses;
- priorities;
- SLA profiles;
- routing policies;
- templates;
- channel policies;
- AI policies;
- asset types;
- planned-work types;
- legal document types;
- estimate states.

### Tests
- schema validation;
- invalid config rejected;
- publish immutability;
- tenant isolation;
- audit diff;
- stale version conflict;
- E2E admin publish;
- E2E unauthorized user denied;
- smoke config survives restart.

---

## F03 — Universal Domain Core

### Outcome
Industry-agnostic primitives support future verticals.

### Implementation
1. Person;
2. Counterparty;
3. Object;
4. Asset;
5. Communication;
6. Case;
7. Incident;
8. WorkOrder;
9. Task;
10. Document metadata;
11. timeline;
12. attachment references;
13. ExternalReference;
14. generic query/filter conventions.

### Tests
- domain invariants;
- cross-tenant relationship rejection;
- repository integration;
- API permission matrix;
- lifecycle behavior;
- pagination/filter behavior;
- E2E generic Case → WorkOrder;
- smoke create/read after restart.

---

## F04 — Events, Outbox, Workflow and SLA Runtime

### Outcome
Configured business processes are durable, retry-safe and auditable.

### Implementation
1. persisted DomainEvent;
2. transactional outbox;
3. worker/publisher;
4. idempotency registry;
5. WorkflowDefinition;
6. WorkflowInstance;
7. transitions;
8. actions;
9. durable timers;
10. SLA profiles;
11. warning/escalation;
12. human approval step;
13. failure/retry state;
14. workflow timeline.

### Tests
- DB state + outbox atomicity;
- duplicate event safe;
- worker restart;
- version pinning;
- invalid transition;
- timer survives restart;
- SLA warning/breach;
- bounded retry;
- authorization of manual override;
- E2E configured workflow;
- smoke worker/queue.

---

# KNOWLEDGE / DOCUMENT INTELLIGENCE

## F05 — Knowledge Index and Hybrid Retrieval

### Outcome
Large volumes of documents/communications become securely searchable by exact terms and semantic meaning.

### Implementation
1. KnowledgeSource;
2. KnowledgeChunk;
3. EmbeddingRecord;
4. pgvector migration;
5. parser interface;
6. chunker interface;
7. embedding provider interface;
8. deterministic fake embedding adapter for tests;
9. full-text index;
10. vector index;
11. hybrid retrieval service;
12. permission/tenant pre-filter;
13. source checksum/versioning;
14. stale/rebuild lifecycle;
15. retrieval evidence references;
16. admin-visible indexing state.

### No-hardcode
- embedding model/provider configurable;
- vector dimension tied to configured embedding profile;
- chunk size/overlap configurable and versioned;
- retrieval weights/rerank policy configurable;
- no tenant filter embedded as optional client parameter.

### Tests
- parser/chunker units;
- embedding schema validation;
- vector insert/query integration;
- full-text + vector hybrid fixtures;
- tenant A cannot retrieve B;
- document-level permission filter;
- revoked access disappears;
- source update reindexes;
- delete propagation;
- idempotent rebuild;
- malformed doc failure state;
- E2E authorized semantic search;
- E2E prompt-injection content treated as data;
- smoke vector extension/index/search.

---

## F06 — Document Ingestion and Attachments

### Outcome
Photos, PDFs, scans and office documents become first-class linked business artifacts.

### Implementation
1. object storage port;
2. upload flow;
3. checksum;
4. metadata;
5. access policy;
6. signed/short-lived download;
7. entity links;
8. virus/file policy hook;
9. parse/index queue;
10. lifecycle/delete policy.

### Tests
- file type/size validation;
- checksum;
- tenant access;
- signed URL scope;
- duplicate content behavior;
- storage adapter contract;
- indexing trigger;
- E2E upload → Case → search;
- smoke upload/download in test storage.

---

# PROPERTY MANAGEMENT — MASTER DATA

## F07 — Buildings, Premises and Service Areas

### Outcome
The managed-property registry exists as the vertical object model.

### Implementation
1. Building type;
2. Premise type;
3. Service Area;
4. configurable attributes;
5. hierarchy;
6. responsible BusinessUnit;
7. import API;
8. search/filter.

### Tests
- hierarchy validation;
- tenant-scoped address uniqueness policy;
- import idempotency;
- cross-tenant parent denial;
- E2E create building + premises;
- smoke list/detail.

---

## F08 — Residents and Client Base

### Outcome
Applicants are reusable resident/person records linked to premises and history.

### Implementation
1. resident profile projection;
2. contacts;
3. person ↔ premise relationship;
4. relationship types;
5. normalization;
6. duplicate candidate detection;
7. controlled merge;
8. request history projection.

### Tests
- phone/contact normalization;
- duplicate candidate rules;
- merge preserving history;
- permission masking;
- tenant isolation;
- E2E resident created from first request;
- smoke profile lookup.

---

# PROPERTY MANAGEMENT — REQUESTS

## F09 — Unified Request Journal

### Outcome
Every resident/office request becomes one authoritative Case visible across the system.

### Implementation
1. org-scoped display numbering;
2. request Case profile;
3. configurable required fields;
4. priority/emergency classification field;
5. status/progress/deadline;
6. comments;
7. timeline;
8. filters/search;
9. linked resident/building/premise;
10. API/UI journal.

### Tests
- concurrency-safe numbering;
- required-field config;
- status rules;
- complete timeline;
- tenant filters;
- E2E request journal;
- smoke create/update/search.

---

## F10 — Manual Dispatcher Intake

### Outcome
Phone/offline requests use the same automation pipeline as digital channels.

### Implementation
1. fast entry UI/API;
2. resident lookup/create;
3. address lookup;
4. free-text problem;
5. configurable form;
6. classification/routing handoff;
7. source = manual/phone;
8. immediate feedback/number.

### Tests
- minimum configured fields;
- unknown resident;
- duplicate resident candidate;
- routing identical to digital intake;
- E2E dispatcher call intake → assigned Case;
- E2E forbidden role;
- smoke create.

---

## F11 — Web Intake

### Outcome
Resident/customer can submit structured request from web.

### Implementation
1. public/authenticated form mode;
2. configurable fields;
3. attachments;
4. anti-abuse;
5. resident resolution;
6. Case creation;
7. feedback.

### Tests
- validation;
- abuse/rate-limit;
- attachment authorization;
- duplicate submission idempotency;
- E2E web → Case;
- smoke submission.

---

## F12 — Email Inbox

### Outcome
Incoming email becomes Communication and then Case/document/task according to configured policy.

### Implementation
1. EmailProvider port;
2. provider adapter;
3. tenant mailbox mapping;
4. polling/webhook mode depending provider;
5. body/attachment normalization;
6. dedup by provider message;
7. thread mapping;
8. review queue;
9. ingestion telemetry.

### Tests
- adapter contract;
- auth failure;
- timeout/retry;
- duplicate delivery;
- wrong tenant mapping;
- attachment ingestion;
- E2E email fixture → Case;
- degraded-provider smoke.

---

## F13 — House Chat Bot and Intake Form

### Outcome
A message in a building chat can become a structured request without an operator copying it manually.

### Implementation
1. MessengerProvider contract;
2. chat → Building mapping;
3. configurable keyword/rule triggers;
4. AI trigger policy;
5. bot CTA;
6. intake form/deep link;
7. known resident prefill;
8. photos/docs;
9. Case creation;
10. acknowledgement.

### Tests
- trigger rules;
- irrelevant message no Case;
- duplicate event idempotency;
- tenant/chat mapping;
- permissions for bot config;
- provider contract;
- E2E chat event → form → Case;
- smoke webhook/poll handling.

---

## F14 — AI Intake, Classification and Routing Suggestions

### Outcome
Routine requests are structured and routed automatically when confidence/policy allow.

### Implementation
1. AI provider port;
2. prompt/template policy;
3. typed extraction schema;
4. category mapping;
5. urgency suggestion;
6. object/person resolution;
7. confidence policy;
8. deterministic routing engine;
9. human-review queue;
10. human correction capture.

### No-hardcode
- models;
- prompts;
- thresholds;
- categories;
- routes;
- fallback policy.

### Tests
- schema parsing;
- representative fixtures;
- low-confidence fallback;
- prompt-injection content;
- provider failure;
- corrected classification telemetry;
- E2E high-confidence auto-route;
- E2E low-confidence review;
- smoke with deterministic fake provider.

---

## F15 — Routing Engine

### Outcome
A Case reaches the correct functional block/assignee using tenant-defined policy.

### Implementation
1. rule model;
2. conditions;
3. candidate pools;
4. qualification;
5. service area;
6. workload hook;
7. working-hours policy;
8. contractor responsibility;
9. manual override;
10. explanation/audit.

### Tests
- rule precedence;
- no-match fallback;
- conflicting rules validation;
- tenant isolation;
- manual override permission;
- E2E request → correct block;
- smoke routing config reload.

---

# PROPERTY MANAGEMENT — EXECUTION / SLA

## F16 — Executor Work Orders

### Outcome
Executor can accept, work, report and complete assigned work from a minimal mobile-friendly surface.

### Implementation
1. WorkOrder from Case/Incident;
2. accept/start/wait/complete;
3. reason codes;
4. progress;
5. comments;
6. before/after evidence;
7. materials;
8. result;
9. reassignment request;
10. verification requirement.

### Tests
- transition matrix;
- ownership/assignment access;
- evidence rules;
- concurrent transition conflict;
- audit timeline;
- E2E executor completes work;
- E2E another executor denied;
- mobile smoke.

---

## F17 — SLA, Deadlines and Escalation

### Outcome
System, not humans, tracks deadlines and escalations.

### Implementation
1. configured SLA profile binding;
2. response/assignment/acceptance/resolution timers;
3. warning;
4. breach;
5. escalation chain;
6. pause conditions;
7. deadline change policy;
8. reason/audit.

### Tests
- simulated clock;
- warning/breach;
- pause/resume;
- changed deadline permission;
- workflow retry;
- E2E overdue appears dashboard/escalates;
- smoke timer worker.

---

## F18 — Incident and Duplicate Consolidation

### Outcome
Mass identical reports preserve each resident Case but generate one operational Incident.

### Implementation
1. candidate matching service;
2. building/category/time signals;
3. semantic similarity optional via F05;
4. active Incident lookup;
5. auto-link policy;
6. manual merge/unlink;
7. affected residents/objects;
8. shared WorkOrders;
9. bulk feedback.

### Tests
- candidate scoring;
- false-positive guard;
- reversible link;
- cross-building constraints;
- semantic similarity fixture;
- idempotent repeated messages;
- E2E 15 reports → 1 Incident + 15 Cases;
- smoke mass-event path.

---

## F19 — Resident Feedback and Notification Engine

### Outcome
Residents get consistent state feedback without manual messages.

### Implementation
1. NotificationPolicy;
2. templates;
3. recipient resolution;
4. channels;
5. event triggers;
6. delivery state;
7. retries;
8. opt-out/consent hooks;
9. bulk Incident messages.

### Tests
- template variables;
- missing channel fallback;
- delivery idempotency;
- provider contract;
- permission/recipient scope;
- E2E Case status → resident message;
- smoke fake provider delivery.

---

## F20 — Operational Request Dashboard

### Outcome
Dispatch/management immediately sees exceptions: new, emergency, overdue, stalled, reopened.

### Implementation
1. query projections;
2. dashboard filters;
3. no-movement rule;
4. emergency queue;
5. overdue;
6. awaiting parties;
7. reopened;
8. Incident widgets;
9. freshness.

### Tests
- projection correctness;
- configurable thresholds;
- tenant scope;
- pagination/performance;
- E2E status changes reflected live/refresh;
- smoke dashboard query.

---

# PROPERTY MANAGEMENT — OBJECT / ASSET / PLANNED WORK

## F21 — Building 360

### Outcome
One digital passport shows the whole operational history/context of a building.

### Implementation
Aggregate:
- premises;
- residents;
- responsible teams;
- Cases;
- Incidents;
- WorkOrders;
- Assets;
- planned work;
- documents;
- contracts;
- legal matters;
- announcements;
- costs where integrated;
- health metrics.

### Tests
- aggregation permissions;
- tenant isolation;
- stale external data marking;
- E2E drill-down from building to Case/Asset;
- performance query test;
- smoke Building 360.

---

## F22 — Inventory / Assets

### Outcome
Every building shows what equipment/assets exist and their lifecycle.

### Implementation
1. configurable Asset types;
2. location;
3. serial/reference;
4. state;
5. responsible;
6. photos/docs;
7. commissioning/lifetime;
8. maintenance history;
9. failures;
10. repair cost links;
11. next inspection.

### Tests
- asset type config;
- lifecycle;
- relation to building;
- tenant isolation;
- E2E asset → repair WorkOrder;
- smoke asset registry.

---

## F23 — PPR / Planned Works

### Outcome
Inspections and recurring maintenance are planned, assigned and verified in the same work system.

### Implementation
1. PlannedWork definition;
2. recurring schedule;
3. object/asset applicability;
4. work volume;
5. materials;
6. assignee/contractor;
7. due date;
8. generated WorkOrder;
9. result/evidence;
10. follow-up deficiencies.

### Tests
- recurrence calculation;
- timezone;
- no duplicate generation;
- schedule edits/versioning;
- E2E scheduled PPR → WorkOrder → complete;
- smoke scheduler.

---

## F24 — Employee Task Management

### Outcome
Managers assign and monitor internal tasks linked to real business entities.

### Implementation
1. Task;
2. assignee/team;
3. deadline;
4. priority;
5. entity links;
6. dependency/block;
7. report/result;
8. manager queue.

### Tests
- permission;
- transition;
- overdue;
- dependency;
- E2E manager → employee → complete;
- smoke task queue.

---

# PROPERTY MANAGEMENT — RESIDENT EXPERIENCE

## F25 — Resident Portal

### Outcome
Resident sees profile, property context, requests, announcements and external financial data in one place.

### Implementation
1. resident authentication/link;
2. own premise scope;
3. request history;
4. new request;
5. attachments;
6. announcements;
7. account/tariff/balance projection via integration;
8. data freshness.

### Tests
- resident cannot see neighbor;
- multiple premises policy;
- external stale data;
- E2E login → request history → create;
- smoke portal.

---

# PROPERTY MANAGEMENT — LEGAL / DOCUMENTS

## F26 — Correspondence Registry

### Outcome
Official inbound/outbound documents are registered, numbered, assigned and controlled.

### Implementation
1. registry entry;
2. configurable type;
3. incoming/outgoing number policy;
4. sender/recipient;
5. deadline;
6. responsible;
7. linked Case/Document;
8. status;
9. timeline.

### Tests
- numbering concurrency;
- deadline;
- attachments;
- permission;
- E2E register → assign → respond;
- smoke search.

---

## F27 — Legal Workspace

### Outcome
Legal work remains linked to originating people, objects, requests and documents.

### Implementation
1. LegalCase;
2. applicant/counterparty;
3. legal type;
4. assigned lawyer;
5. deadlines;
6. courts/prosecutor/claim data;
7. hearings/events;
8. templates;
9. responses;
10. decision/closure;
11. knowledge retrieval integration.

### Tests
- restricted permission;
- legal timeline;
- deadline;
- template field validation;
- retrieval authorized legal corpus;
- E2E request → LegalCase → response;
- smoke legal search.

---

# PROPERTY MANAGEMENT — ESTIMATES / FINANCE

## F28 — Estimates

### Outcome
Work/incident/planned maintenance can carry a versioned estimate and later plan/fact.

### Implementation
1. Estimate;
2. line items;
3. work/material/resource;
4. quantity/unit/price;
5. versions;
6. approval workflow;
7. links to WorkOrder/Case/PPR;
8. actuals link;
9. variance.

### Tests
- arithmetic;
- version immutability;
- approval authorization;
- tenant isolation;
- E2E draft → approve → actuals;
- smoke estimate read.

---

## F29 — Resident Announcement Composer

### Outcome
Structured facts become clear resident announcements with safe AI assistance.

### Implementation
1. structured announcement facts;
2. target buildings/audience;
3. AI text draft;
4. deterministic fact validation;
5. preview;
6. approval policy;
7. channel delivery;
8. delivery report.

### Tests
- AI cannot change date/address/time facts silently;
- audience scope;
- template fallback;
- E2E compose → approve → send;
- smoke fake delivery.

---

## F30 — Monthly Operational Report

### Outcome
Monthly report is generated from system facts, not manual Excel.

### Implementation
Metrics:
- total Cases;
- categories;
- emergencies;
- Incidents;
- SLA;
- overdue;
- response/resolution percentiles;
- reopen/repeat;
- PPR completion;
- tasks;
- worst objects;
- contractors;
- automation/human intervention.

Add:
- report definition/config;
- generation;
- export;
- snapshot/version.

### Tests
- metric fixtures;
- percentile correctness;
- tenant/timezone boundary;
- immutable historical snapshot;
- E2E generate report;
- smoke export.

---

# INTEGRATIONS / MANAGEMENT

## F31 — Integration Hub Production Foundation

### Outcome
External systems connect through consistent, observable, safe adapters.

### Implementation
1. IntegrationConnection;
2. secret reference;
3. health;
4. SyncRun;
5. SyncCursor;
6. ExternalReference;
7. webhook registry;
8. reconciliation;
9. retry classes;
10. freshness state.

### Tests
- auth failure;
- timeout;
- retry;
- unknown mutation result;
- webhook authenticity;
- tenant mapping;
- secret masking;
- E2E connection test;
- smoke disabled/degraded provider.

---

## F32 — Accounting / 1C Read Integration

### Outcome
Start can display authoritative accounting reference/financial data without becoming accounting.

### Implementation
- provider contract;
- counterparties;
- contracts/relevant documents;
- payments/cost facts;
- receivables/payables as supported;
- external refs;
- freshness/reconciliation.

### Tests
- provider contract fixtures;
- mapping;
- duplicate sync;
- stale state;
- reconciliation;
- tenant isolation;
- E2E sync → visible projection;
- smoke sandbox/fake connector.

---

## F33 — EDO Integration

### Outcome
Official document state is visible and can participate in workflows while original remains with EDO provider.

### Implementation
- inbound metadata;
- document reference;
- signature state;
- approval routing;
- linked Case/Contract;
- sync/webhook;
- reconciliation;
- knowledge indexing of permitted content.

### Tests
- webhook signature;
- duplicate event;
- signature state mapping;
- permission;
- source-of-truth conflict;
- E2E receive → workflow;
- smoke provider.

---

## F34 — Bank Read Integration

### Outcome
Authorized users see real balances/transactions with freshness.

### Implementation
- accounts;
- balances;
- transactions;
- statements;
- external refs;
- freshness;
- reconciliation.

### Tests
- auth;
- pagination;
- duplicate transaction;
- stale data;
- tenant isolation;
- E2E sync → management view;
- smoke provider.

No payment write in this feature.

---

# MANAGEMENT LAYERS

## F35 — Contractor Performance

### Outcome
Managers compare contractors by price, SLA, rework and quality.

### Implementation
- contractor links;
- spend inputs;
- WorkOrder metrics;
- rework;
- complaints;
- score definition/version;
- drill-down evidence.

### Tests
- score fixtures;
- missing data;
- versioned score;
- evidence links;
- E2E contractor dashboard;
- smoke aggregate.

---

## F36 — Manager / Director Control

### Outcome
Management sees bottlenecks and deviations rather than chasing statuses.

### Implementation
- backlog;
- throughput;
- SLA;
- workload;
- object health;
- contractor metrics;
- repeat failures;
- planned work;
- costs/freshness;
- attention queue.

### Tests
- aggregate fixtures;
- permission;
- drill-down evidence;
- tenant isolation;
- E2E dashboard → evidence;
- smoke queries.

---

## F37 — Owner Control

### Outcome
One global account can safely control authorized businesses without entering each office CRM.

### Implementation
- group/org switcher;
- company cards;
- attention queue;
- cross-company metrics;
- money/risk views;
- mobile/PWA;
- step-up auth hooks;
- AI summary over authorized structured + knowledge context.

### Tests
- group authorization;
- no unauthorized company leakage;
- scoped drill-down;
- stale data disclosure;
- E2E owner logs in → sees multiple orgs → drill-down;
- E2E denied org absent;
- smoke Owner Control.

---

## F38 — Owner AI / Business Q&A

### Outcome
Owner can ask questions across authorized businesses and receive evidence-backed answers.

### Implementation
1. intent/query planner;
2. structured analytics retrieval;
3. authorized knowledge retrieval;
4. source/evidence list;
5. freshness;
6. answer policy;
7. optional recommended action;
8. no direct high-impact execution.

### Tests
- tenant/group scope;
- retrieval permission;
- stale evidence notice;
- prompt injection;
- unsupported question;
- evidence completeness;
- E2E "what requires attention?";
- E2E cross-tenant forbidden evidence never enters context;
- smoke deterministic model adapter.

---

# SCALE / PRODUCTIZATION

## F39 — Second Vertical Pack

### Outcome
Prove the architecture is reusable outside Property Management.

Choose Construction or Fleet/Service based on real access/value.

Tests must prove the second pack reuses:
- identity;
- core;
- workflow;
- documents;
- knowledge;
- integrations;
- analytics.

No copied core service accepted.

---

## F40 — Cross-company Intelligence

### Outcome
Owner gets insights impossible from one company CRM.

Implement:
- legal counterparty identity;
- group spend;
- price variance;
- shared contractor comparison;
- duplicated procurement;
- asset performance;
- anomaly detection;
- evidence-backed recommendations.

### Tests
- exact legal identity vs fuzzy-name false match;
- permission scope;
- data completeness/freshness;
- recommendation evidence;
- E2E cross-company query;
- smoke group aggregate.

---

## F41 — Productized Onboarding

### Outcome
A new customer is configured, not forked.

Flow:
~~~text
Create Group
→ Add Organization
→ Select Vertical Pack
→ Configure identity/access
→ Import reference data
→ Connect systems
→ Configure workflows
→ Validate
→ Smoke
→ Launch
~~~

### Tests
- onboarding state machine;
- partial resume;
- invalid integration config;
- tenant isolation;
- seeded E2E new tenant;
- smoke generated tenant configuration.

---

# Completion definition for the whole Property Management vertical

The vertical is not considered production-ready until:

- request intake works across configured channels;
- manual and automatic paths converge to one Case model;
- every status change is reflected across journal/executor/resident/analytics views;
- Incident consolidates mass events safely;
- residents and Building 360 preserve complete history;
- Asset/PPR work shares the same WorkOrder model;
- legal/registry/estimates are linked to source business entities;
- documents are searchable through authorized hybrid retrieval;
- management reporting is generated from system facts;
- all mutable policy is admin-configurable;
- tenant isolation suite is green;
- critical E2E journeys are green;
- production-like smoke is green;
- CI is green for the exact release SHA;
- observability can reconstruct a failed business journey.
