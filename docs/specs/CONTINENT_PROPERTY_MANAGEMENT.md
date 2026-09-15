# Континент — Property Management Pack Specification

## 1. Purpose

The Континент deployment is the first real proving ground for Start.

The employee-facing experience should cover the useful functional class of a modern property-management dispatch platform while materially reducing manual operator/deloproizvoditel routine.

The pilot must validate the universal platform. It must not cause property-management concepts to leak into the core.

## 2. Primary user problem

Today operational staff may need to:

- monitor email;
- monitor chats/messengers;
- read requests;
- identify person/address;
- understand the problem;
- copy details into a system;
- classify;
- choose an executor;
- remind executors;
- answer residents;
- detect duplicates/mass incidents manually;
- compile status reports.

The target state is:

```text
Incoming communication
→ automatic normalization
→ entity resolution
→ classification
→ duplicate/incident check
→ Case
→ routing
→ SLA
→ notifications
→ WorkOrder
→ verification
→ analytics
```

Human involvement is primarily for ambiguity, exceptions and decisions.

## 3. User roles

Initial role templates:

- Office Operator;
- Dispatcher;
- Site/Area Master;
- Executor;
- Contractor;
- Operations Manager;
- Company Director;
- Organization Admin.

Permissions remain data-driven.

## 4. Tenant UX

Континент employees should experience the platform as their own company system.

Branding/capabilities may include:

- company name/logo;
- enabled modules;
- role-based navigation;
- configured terminology.

Other companies are invisible unless the user has explicit memberships.

## 5. Property domain mapping

### Object types

- Managed Building;
- Entrance;
- Premise/Apartment;
- Service Area.

### Asset types

Examples, configurable:

- elevator;
- pump;
- heating node;
- pipe system;
- electrical equipment;
- access/door system.

### Person roles

- resident;
- owner;
- applicant/contact;
- employee contact.

### Case types

Initial examples:

- resident request;
- complaint;
- service request;
- emergency report;
- document/office request.

The list is admin-managed.

### WorkOrder types

- repair;
- inspection;
- emergency response;
- planned maintenance;
- verification.

## 6. Universal Inbox

### Sources

Initial supported source classes:

- email;
- web form;
- manual office entry.

Next:

- telephony;
- MAX;
- Telegram;
- VK;
- SMS/push outbound.

Each source becomes a normalized Communication.

### Inbox processing

Processing pipeline:

1. receive;
2. identify IntegrationConnection/mailbox/channel;
3. determine organization;
4. normalize payload;
5. resolve sender/person candidates;
6. extract address/object;
7. classify intent/category;
8. determine urgency;
9. search duplicates/active incidents;
10. create/link Case;
11. start workflow;
12. notify sender if policy allows.

### Confidence policy

AI output must include validated structured fields and confidence/evidence.

Outcomes:

- high confidence + low-risk policy → auto-process;
- uncertain fields → operator review;
- high-risk/emergency ambiguity → explicit escalation policy.

Confidence thresholds are configurable.

## 7. Case card

Minimum information:

- Case ID;
- source;
- applicant/contact;
- building/object;
- premise where relevant;
- problem/description;
- category;
- priority;
- status;
- responsible unit;
- assignee;
- SLA;
- linked Incident;
- linked WorkOrders;
- communications timeline;
- attachments;
- comments;
- materials/cost references;
- created/updated/closed timestamps;
- audit history.

## 8. Status lifecycle

Statuses are configured, but the initial workflow concept is:

```text
New
→ Classified
→ Assigned
→ Accepted
→ In Progress
→ Waiting
→ Completed
→ Verified
→ Closed
```

Side outcomes:

- Cancelled;
- Duplicate;
- Merged/Linked to Incident;
- Reopened.

Do not hardcode labels into the universal workflow engine.

## 9. Incident Engine

### Goal

Many reports of one event must not generate many independent repair actions.

Example:

100 residents report no water.

Target:

```text
Incident
├── affected objects
├── affected premises/people
├── linked Cases
├── one or more WorkOrders
├── responsible team
├── incident SLA
└── bulk notifications
```

### Incident candidate detection

Signals:

- same/similar category;
- same building/area;
- temporal proximity;
- known infrastructure dependency;
- operator manual link.

Automatic merge decisions should be reversible/auditable.

## 10. Routing

Routing may use:

- organization;
- service area;
- object;
- category;
- priority;
- qualification;
- shift;
- availability;
- workload;
- contractor responsibility.

The rule set is managed in admin.

Manual override remains possible for authorized users and is audited.

## 11. SLA

SLA profile can define:

- response target;
- assignment target;
- acceptance target;
- resolution target;
- verification target;
- warning schedule;
- escalation chain.

Timers are durable.

Changes to SLA definitions are versioned; running cases retain the relevant version unless explicitly migrated.

## 12. Work execution UI

Mobile-first executor surface.

Minimum actions:

- view assigned work;
- accept;
- start;
- pause/wait with reason;
- attach “before” evidence;
- comment;
- record used material/resource;
- attach “after” evidence;
- complete;
- request reassignment/escalation.

Do not expose unnecessary office CRM complexity.

## 13. Notifications

Events may trigger notifications:

- request registered;
- assigned;
- work started;
- delay/status change;
- incident recognized;
- work completed;
- verification/feedback.

Channel selection and templates are configurable.

Delivery result is tracked.

## 14. Contractor model

Contractors participate through scoped access or office-managed assignment.

Track:

- assigned work;
- completion;
- SLA;
- cost;
- rework;
- complaints;
- acceptance quality.

Contractor scoring is configuration-driven and versioned.

## 15. Building/Object 360

A building/object page should aggregate:

- current incidents;
- current cases;
- case history;
- assets;
- recurring failures;
- work history;
- contractors;
- documents/contracts links;
- operating cost data when integrated;
- health metrics.

This is a key differentiator over flat ticket lists.

## 16. Asset lifecycle

For relevant equipment:

- passport/reference data;
- location;
- responsible party;
- status;
- maintenance schedule;
- failure history;
- repair cost;
- downtime;
- documents.

This enables repair-vs-replacement analysis later.

## 17. Manager dashboard

Company managers need:

- active backlog;
- SLA;
- incidents;
- workload;
- overdue work;
- repeat requests;
- contractor performance;
- object health;
- automation failures;
- human-intervention queue.

## 18. Director dashboard

Higher abstraction:

- service quality trend;
- operating cost where data exists;
- worst objects;
- systematic categories;
- contractor quality;
- staffing/capacity;
- high-risk deviations.

## 19. Pilot scope recommendation

### Pilot A — inbound office automation

Start with:

- email inbox;
- web/manual form;
- object/address directory;
- Case;
- classification;
- deduplication;
- routing;
- SLA;
- executor status;
- notifications;
- manager analytics.

This directly targets the initiating employee's pain and produces measurable baseline/post-change metrics.

### Pilot B — omnichannel

Add:

- telephony;
- messenger channels;
- incident engine;
- contractor access.

### Pilot C — business integration

Add:

- 1C read;
- EDO;
- finance/cost linkage;
- object 360 management analytics.

## 20. Pilot baseline collection

Before automation record:

- inbound request volume/day/week;
- source split;
- number of manual touches;
- time from inbound to registration;
- time to assignment;
- missed requests;
- duplicates;
- operator staffing/time;
- SLA performance;
- reopen/repeat rate.

## 21. Pilot acceptance gates

### Gate 1 — correctness

- no tenant leakage;
- every inbound item is traceable;
- no silent data loss;
- assignment/workflow history auditable.

### Gate 2 — automation

- automation/human-intervention metrics collected;
- high-confidence items can complete intake/routing without manual copy/paste;
- uncertain items safely enter review.

### Gate 3 — quality

- SLA and reopen metrics exist;
- incident linking is visible and reversible;
- executor completion is auditable.

### Gate 4 — commercial proof

Produce before/after report using real platform metrics.

Do not claim salary/headcount savings unless the customer confirms labor economics.

## 22. Explicit non-goals of first release

- billing residents;
- full statutory ЖКХ accounting;
- full GIS ЖКХ replacement;
- full ERP/warehouse replacement;
- autonomous financial payments;
- autonomous legal signing.

These may integrate later without distorting the initial operational core.
