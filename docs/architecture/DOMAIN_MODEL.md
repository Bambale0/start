# Canonical Domain Model

## 1. Goals

The model must:

- support unrelated industries;
- preserve hard tenant boundaries;
- enable cross-company owner views through explicit group scope;
- represent operational work independently from communication channels;
- preserve audit/history;
- avoid encoding business taxonomies as enums in source.

## 2. Identity and organization

### User

Global authenticated identity.

Key concepts:

- id;
- authentication identity;
- status;
- security settings;
- session/device metadata.

A User is not tenant-bound.

### Group

Application-level aggregation of organizations.

Fields conceptually include:

- id;
- name;
- status;
- configuration;
- created_at.

### Organization

Tenant and business boundary.

Conceptual fields:

- id;
- legal/display name;
- status;
- branding/config;
- timezone/locale;
- vertical capabilities.

### BusinessUnit

Hierarchical organizational subdivision.

Supports:

- branch;
- department;
- region;
- team;
- service line.

### Membership

Authorization relationship.

Conceptual shape:

```text
Membership
- user_id
- scope_type: GROUP | ORGANIZATION | BUSINESS_UNIT
- scope_id
- role_id
- status
- valid_from / valid_until
```

Do not encode owner user IDs in source.

## 3. Authorization model

### Role

Named reusable bundle.

### Permission

Atomic capability such as:

```text
cases.read
cases.manage
work_orders.assign
finance.read
payment_requests.approve
documents.approve
group.analytics.read
integrations.manage
```

### Policy condition

Optional contextual restriction:

- own business unit;
- assigned objects;
- own work orders;
- monetary threshold;
- document type;
- organization;
- time/device risk.

Authorization is evaluated server-side.

## 4. People and counterparties

### Person

A real-world person record used by business processes.

It may represent:

- resident;
- customer;
- employee contact;
- applicant;
- driver;
- responsible contact.

Authentication is optional and separate.

### Counterparty

An external business/legal party.

Possible links:

- contracts;
- documents;
- financial events;
- work orders;
- supplier/contractor performance.

Cross-company identity resolution must distinguish “same legal entity” from “similar text name”.

## 5. Object model

### Object

A managed context/location/project object.

Core fields:

- organization_id;
- type_id;
- parent_object_id;
- name;
- external references;
- status;
- structured attributes.

Vertical packs define allowed object types/attributes.

### Asset

An owned/managed resource with lifecycle.

Core concerns:

- organization;
- object/location;
- asset type;
- status;
- responsible party;
- acquisition/value metadata where needed;
- maintenance/repair history;
- documents;
- costs.

## 6. Operational model

### Case

A business item requiring handling.

Fields conceptually:

- organization_id;
- case_type_id;
- source;
- subject/person;
- object;
- priority;
- status;
- assigned unit/person;
- workflow instance;
- SLA policy/version;
- timestamps;
- structured attributes.

### Incident

A shared operational event.

An Incident can link many Cases and affect many Objects/Assets.

This prevents mass events from becoming duplicate independent work.

### WorkOrder

Executable operational activity.

Can originate from:

- Case;
- Incident;
- preventive maintenance;
- project;
- manual initiation;
- workflow.

Tracks:

- assignment;
- acceptance;
- start/finish;
- evidence;
- materials/resources;
- result;
- verification;
- costs.

### Task

Generic actionable step.

Do not overload Task to represent every business entity.

## 7. Workflow model

### WorkflowDefinition

Versioned process definition.

### WorkflowInstance

One execution bound to a specific definition version.

### WorkflowStep/Transition

Auditable runtime state changes.

### Timer

Durable future condition for SLA/reminders/escalation.

## 8. Communication model

### Conversation

Optional grouping of communications across a context.

### Communication

Normalized message/call/email/web event.

Core metadata:

- organization;
- provider/channel;
- direction;
- sender/recipient references;
- provider message ID;
- occurred_at;
- normalized text/transcript;
- attachment refs;
- linked Person/Case/Incident;
- raw provider reference;
- delivery state.

Provider payload remains adapter-owned.

## 9. Document model

### Document

Business metadata and access reference.

May point to:

- object storage;
- EDO provider;
- accounting system;
- external URL/reference.

Metadata may include:

- document type;
- counterparty;
- amount/currency;
- effective dates;
- workflow status;
- signature state;
- checksum;
- source-of-record reference.

### Contract

Domain specialization for long-lived obligations/relationships.

Links:

- parties;
- documents;
- organization;
- amount/limits;
- dates;
- payment terms;
- related work/assets/objects.

## 9A. Knowledge and retrieval model

### KnowledgeSource

Reference to an authoritative source that is eligible for indexing.

Typical sources:

- Document;
- Communication;
- Case/Incident narrative;
- Asset manual;
- Legal Case material;
- external document mirrored through an IntegrationConnection.

### KnowledgeChunk

Derived text segment.

Conceptual fields:

- organization_id;
- optional group_id;
- source_type / source_id;
- source checksum/version;
- chunk ordinal;
- normalized text;
- structured metadata;
- permission scope;
- parser version;
- chunker policy/version;
- lifecycle state.

A KnowledgeChunk is rebuildable and is never the authoritative business record.

### EmbeddingRecord

Derived vector representation.

Conceptual fields:

- chunk_id;
- embedding profile/version;
- provider/model identifier;
- dimension;
- vector;
- created_at;
- stale/rebuild state.

No domain rule depends on one hardcoded embedding provider/model.

### RetrievalPolicy

Versioned configuration for:

- lexical/vector retrieval;
- candidate counts;
- ranking/fusion;
- optional reranking;
- source-type filters;
- freshness constraints.

Authorization filters are not optional retrieval policy: they are mandatory security constraints.

## 10. Finance model

### FinancialEvent

Normalized management record.

Possible types are configuration-driven and may represent:

- invoice;
- payment observed;
- payment request;
- obligation;
- accrual mirror;
- budget allocation;
- cost allocation.

A FinancialEvent is not automatically a statutory accounting entry.

### PaymentRequest

Controlled intent to create/approve a payment.

High-impact transitions require authorization and audit.

### Budget

Optional management budget model.

## 11. Configuration model

Avoid source enums for business taxonomies.

Prefer configuration entities:

- EntityType;
- StatusDefinition;
- Category;
- PriorityDefinition;
- SLAProfile;
- RoutingRule;
- NotificationPolicy;
- WorkflowDefinition;
- MetricDefinition;
- ScoreDefinition;
- Feature/Capability config.

Technical enums are acceptable for stable protocol/runtime concepts.

## 12. Integration model

### IntegrationConnection

Tenant-owned provider connection.

Contains:

- provider type;
- organization;
- enabled state;
- secret reference;
- non-secret config;
- capabilities;
- last health/sync state.

### ExternalReference

Maps a Start entity to a provider entity.

```text
organization_id
provider
entity_type
local_entity_id
external_id
version/etag where relevant
```

### SyncCursor / SyncRun

Tracks incremental synchronization and reconciliation.

## 13. Audit model

### AuditEvent

Records material actions/config changes.

Fields:

- actor;
- effective scope;
- action;
- target;
- before/after references or structured diff;
- time;
- request/trace;
- origin;
- result.

Audit events are append-oriented.

## 14. Analytics model

Operational tables should not become ad-hoc dashboard databases.

Introduce:

- metric definitions;
- metric facts;
- aggregates/materialized views;
- alert/anomaly records;
- score versions.

Every composite score stores its formula/config version.

## 15. Tenant key rule

Tenant-bound entities carry `organization_id` directly unless there is a strong relational reason not to.

Do not rely on a long join chain to determine tenant ownership for authorization-critical tables.

Group-level entities have explicit `group_id`.

Cross-tenant aggregation occurs only under an authorized group context.

## 16. Soft delete / archival

Prefer lifecycle state/archive for business records that are referenced by history.

Hard delete is reserved for safe cases and privacy/legal requirements with explicit policy.

## 17. IDs and timestamps

- opaque UUID/UUIDv7-style identifiers are preferred;
- timestamps stored in UTC;
- organization timezone used for presentation/business rules;
- provider IDs are never used as primary internal IDs.
