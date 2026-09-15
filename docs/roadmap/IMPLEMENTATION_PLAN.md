# Implementation Plan

## Strategy

Build the universal platform and prove it through one narrow real workflow before expanding breadth.

The critical sequence is:

```text
Foundation
→ Universal Core
→ Континент pilot
→ measurable automation
→ manager analytics
→ Owner Control Lite
→ integrations
→ second vertical
→ cross-company intelligence
→ productized onboarding
```

## Phase 0 — Repository/Product Foundation

### Deliverables

- architecture/spec docs;
- engineering rules;
- ADRs;
- minimal runnable API;
- CI;
- local Docker setup;
- structured config/logging foundation.

### Exit gate

- repository checks pass;
- architecture boundaries documented;
- next work can be cut into vertical slices.

## Phase 1 — Identity, Tenancy and Authorization

### Deliverables

- User;
- Group;
- Organization;
- BusinessUnit;
- Membership;
- Role/Permission;
- organization context selection;
- authorization service;
- audit foundation;
- database tenant enforcement/RLS design;
- admin management for memberships/roles.

### Mandatory tests

- user with tenant A cannot access tenant B;
- group user sees only explicitly authorized organizations;
- revoked membership stops access;
- browser-supplied organization ID cannot elevate;
- privileged mutations are audited.

### Exit gate

No feature work proceeds to sensitive real data without verified tenant isolation.

## Phase 2 — Universal Operational Core

### Deliverables

- Object;
- Asset;
- Person;
- Counterparty;
- Case;
- Incident;
- WorkOrder;
- Task;
- generic timeline;
- attachments/document references;
- configuration taxonomies;
- basic APIs/admin.

### Exit gate

A generic Case → WorkOrder journey works without property-specific core code.

## Phase 3 — Workflow + Event Runtime

### Deliverables

- versioned workflow definitions;
- workflow instances;
- transitions;
- durable timers;
- SLA policies;
- reminders/escalations;
- domain event envelope;
- transactional outbox;
- background worker;
- idempotency primitives.

### Exit gate

A configured workflow can execute end-to-end and survive retry/restart without duplicate side effects.

## Phase 4 — Континент Pilot A: Office Intake

### Deliverables

- Property Management pack;
- buildings/premises;
- residents/contacts;
- email intake;
- web/manual intake;
- AI classification/extraction;
- entity/address resolution;
- duplicate candidates;
- routing;
- Case UI;
- manager work queue;
- executor status flow;
- notifications;
- baseline/product telemetry.

### Exit gate

The initiating office workflow can operate without manual retyping across inbox and CRM for high-confidence routine cases.

## Phase 5 — Incident + SLA Automation

### Deliverables

- incident detection/linking;
- mass-event handling;
- SLA dashboards;
- automatic reminders;
- escalation;
- reopen/verification;
- operator exception queue.

### Exit gate

Human Intervention Rate and SLA metrics are available and trustworthy.

## Phase 6 — Континент Pilot B: Omnichannel

### Deliverables

Prioritized according to customer channels:

- telephony;
- MAX;
- Telegram;
- VK;
- outbound messaging;
- channel delivery tracking.

### Exit gate

Channel adapters feed one common workflow without duplicated business logic.

## Phase 7 — Manager/Director Control

### Deliverables

- backlog/throughput;
- employee/team workload;
- contractor metrics;
- object health;
- repeat failure analysis;
- asset history;
- automation quality;
- director summary.

### Exit gate

Management can diagnose why a metric is bad and drill to evidence.

## Phase 8 — Owner Control Lite

### Deliverables

- global owner/group entrypoint;
- group/org switcher;
- company cards;
- critical attention queue;
- group-authorized metrics;
- owner AI summary over structured data;
- mobile/PWA-friendly views;
- MFA/passkey maturity for privileged access.

### Exit gate

An owner can view authorized companies without using employee operational screens.

## Phase 9 — Integration Hub v1

### Deliverables

- IntegrationConnection;
- secret references;
- sync runs/cursors;
- health/freshness;
- generic provider contracts;
- email production hardening;
- first 1C read connector;
- first EDO connector;
- first bank read connector.

### Exit gate

External data is normalized, freshness-visible and reconciled.

## Phase 10 — Finance/Documents/Procurement Workflow

### Deliverables

- contracts;
- documents;
- financial events;
- payment requests;
- approval workflow;
- procurement need/request;
- supplier comparison;
- EDO/1C/bank linkage.

### Safety

No autonomous signing/payment.

### Exit gate

One cross-system document/approval/payment-intent process can be handled from Start with external systems retaining legal/accounting authority.

## Phase 11 — Second Vertical

Choose the business with the clearest access/value.

Candidate A: Construction Pack.

Candidate B: Fleet/Service Pack.

### Goal

Prove core reuse.

### Exit gate

At least one materially different business operates on the same identity, workflow, integration and analytics primitives without copying the core.

## Phase 12 — Cross-company Intelligence

### Deliverables

- counterparty identity across organizations;
- group spend;
- price variance;
- shared contractor quality;
- duplicated procurement;
- asset performance;
- anomaly detection;
- evidence-backed owner recommendations.

### Exit gate

Owner Control creates value that no individual company CRM can provide alone.

## Phase 13 — Productized SaaS Onboarding

### Deliverables

- organization creation wizard;
- pack selection;
- configuration import/templates;
- connector marketplace/catalog;
- self-service role setup;
- guided data import;
- environment health checks;
- tenant branding/domains;
- billing/entitlements if commercial model requires it.

### Target onboarding

```text
Create Group
→ Add Organization
→ Select Vertical Pack
→ Import users/reference data
→ Connect systems
→ Configure workflows
→ Validate
→ Launch
```

No new codebase per customer.

---

# Workstream view

## Platform

Identity, tenancy, auth, config, audit, events.

## Operations

Cases, incidents, work, assets, workflows.

## Integrations

Email, communication, accounting, EDO, banking.

## Intelligence

AI intake, entity resolution, anomaly detection, owner assistant.

## Experience

Office, executor, admin, owner.

## Reliability

CI, migrations, observability, backups, security.

---

# Ticket slicing rule

Prefer tickets that deliver one coherent vertical capability.

Good:

> Receive an email for organization A, normalize it, create a Case through a configured rule, expose it in the work queue, emit telemetry and cover tenant isolation.

Bad:

> Build all email infrastructure.

Each ticket should state:

- user/business outcome;
- scope;
- acceptance criteria;
- data/schema impact;
- authorization;
- observability;
- tests;
- rollout/migration risk.

## Change gates

### Before implementation

- spec understood;
- relevant skill flow applied;
- affected architecture/ADR reviewed.

### Before merge

- tests;
- lint/type checks;
- migration review;
- tenant/security review;
- observability check;
- no hardcoded mutable business state.

### Before production

- smoke test;
- rollback/forward-fix plan;
- config/secrets present;
- migrations safe;
- dashboards/alerts adequate;
- exact commit identified.

## Commercial proof milestone

After stable Континент pilot, create a measured report:

- baseline vs current;
- request volume;
- automation rate;
- manual touches;
- intake/assignment time;
- SLA;
- missed/duplicate requests;
- rework;
- operator capacity.

This report is the bridge from employee-level sale to director/owner-level rollout.
