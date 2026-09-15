# Product Specification — Start / AI Business OS

## 1. Problem

Multi-business owners and operating teams often work through disconnected systems:

- 1C/accounting;
- EDO;
- banks;
- email;
- telephony;
- messengers;
- spreadsheets;
- industry CRMs;
- task trackers;
- manual status reporting.

The resulting cost is not only software fragmentation. It creates human relay work:

- reading;
- copying;
- classifying;
- forwarding;
- reminding;
- reconciling;
- compiling reports;
- escalating too late.

A traditional CRM usually optimizes one department or one industry. Start targets the layer above: a common operational control plane across different businesses.

## 2. Vision

Each company behaves like a standalone office application for its employees while sharing a common platform underneath.

A founder/owner with explicit permissions signs in with one global account and can access all authorized businesses from any device.

The platform translates low-level business events into the right abstraction for each role:

- worker: what do I need to do?
- manager: what is not being done?
- director: where is the process deviating?
- owner: where are money, quality or risk outside acceptable bounds and what decision is needed?

## 3. Primary personas

### Operator / office employee

Goals:

- stop manually reading multiple sources;
- receive a prioritized work queue;
- avoid duplicate data entry;
- resolve exceptions.

### Executor / field worker

Goals:

- see assigned work;
- accept/start/complete with minimal UI;
- attach evidence/materials/comments;
- avoid office-system complexity.

### Manager

Goals:

- see workload and bottlenecks;
- control SLA;
- manage teams and contractors;
- act on exceptions.

### Company Director

Goals:

- manage company-level health;
- understand cost/quality;
- identify systematic failures;
- drill into evidence when necessary.

### Group Owner / Founder

Goals:

- see all authorized businesses in one place;
- understand money, risk, projects, assets and anomalies;
- minimize operational attention;
- ask cross-company questions;
- drill down only when useful.

### Administrator / Integrator

Goals:

- configure businesses without code changes;
- manage roles, workflows, statuses, SLA and integrations;
- safely rotate secrets;
- audit changes.

## 4. Product surfaces

### Office Workspace

Tenant-branded interface for employees and local managers.

### Executor UI

Mobile-first minimal surface for work execution.

### Admin / Control Plane

Configuration of mutable business entities, permissions, workflows, integrations and vertical modules.

### Owner Control

Cross-company management surface with drill-down and AI-assisted analysis.

## 5. Functional capabilities

### Identity and organization

- global user account;
- group memberships;
- organization memberships;
- business-unit scope;
- RBAC + contextual restrictions;
- tenant branding/domain configuration;
- session/device management.

### Universal operations

- cases;
- incidents;
- work orders;
- tasks;
- objects;
- assets;
- people;
- counterparties;
- communications;
- documents;
- financial events;
- configurable workflow execution.

### Automation

- inbound classification;
- structured data extraction;
- entity resolution;
- duplicate detection;
- routing;
- SLA timers;
- reminders;
- escalation;
- notifications;
- summarization;
- anomaly detection;
- recommended actions.

### Management intelligence

- SLA;
- backlog;
- throughput;
- reopen/rework rate;
- cost per operation;
- object health;
- asset health;
- contractor score;
- management-attention queue.

### Cross-company intelligence

- consolidated counterparty view;
- cross-company spend;
- repeated supplier/material opportunities;
- anomalous prices;
- shared contractor performance;
- idle/underperforming assets;
- group-level risk.

## 6. Product principles

### Automate the action, not only the form

Do not replace a manual inbox with a prettier inbox.

When confidence and policy allow, the system should complete deterministic routine steps automatically.

### Humans manage exceptions

Routine success should remain quiet. Ambiguity and high-impact decisions surface to the right human.

### Progressive drill-down

Owner → company → unit → object → process → event.

The system supports drill-down without forcing high-level users to live in operational detail.

### One workflow, many channels

Email, phone, web, MAX, Telegram, VK and future channels are transport adapters into common domain processes.

### Explainability for management AI

Management recommendations should expose the underlying evidence/metrics, not merely an LLM opinion.

## 7. Initial vertical: Property Management

The first vertical validates:

- omnichannel intake;
- building/resident object structure;
- cases;
- incidents;
- work orders;
- SLA;
- executors;
- contractors;
- notifications;
- manager analytics.

See `docs/specs/CONTINENT_PROPERTY_MANAGEMENT.md`.

## 8. Later verticals

### Construction

Potential domain mappings:

- Object → construction site;
- Case → defect/issue;
- WorkOrder → construction task/remediation;
- Counterparty → subcontractor;
- Asset → construction equipment;
- Workflow → defect acceptance/remediation/inspection.

### Fleet / Service

Potential mappings:

- Asset → vehicle;
- Case → failure/service request;
- WorkOrder → repair/maintenance/trip task;
- Person → driver;
- Counterparty → repair shop/provider.

## 9. Out of scope for the initial product

- replacing statutory accounting;
- becoming an EDO operator;
- becoming a bank/payment network;
- full payroll engine;
- full warehouse/ERP replacement;
- autonomous legal signing;
- autonomous high-value payments;
- microservice decomposition without demonstrated need.

## 10. Product KPIs

Primary:

- Human Intervention Rate;
- Automation Rate;
- Cost per Case/Process;
- Time to Intake;
- Time to Assignment;
- SLA Compliance;
- Reopen/Rework Rate;
- Missed Request Rate;
- Operator Capacity;
- Management Attention Required.

Secondary:

- object/asset health trend;
- contractor quality;
- integration failure rate;
- reconciliation drift;
- user adoption;
- time saved by role.

## 11. Commercial validation path

1. solve a real operational pain in Континент;
2. measure baseline before automation;
3. measure impact after automation;
4. expose manager-level analytics;
5. present evidence to owners;
6. enable Owner Control;
7. connect a second, different business;
8. prove the core is reusable;
9. expand group-wide;
10. productize onboarding for unrelated customers.

## 12. Acceptance definition for product foundation

The foundation is valid when:

- tenant isolation is architectural, not UI-only;
- identity supports multi-company memberships;
- domain primitives are not property-management-specific;
- workflows are configuration-driven;
- integrations use provider-agnostic ports;
- observability/audit is part of the model;
- the Property Management pack can be implemented without changing the core's meaning;
- Owner Control can aggregate authorized organizations without bypassing tenant authorization.
