# Product Context and Vocabulary

This file is the compact shared language for product, engineering and agents.

## Product

**Start** is the repository working name for an AI-enabled Business Operating System.

It is not a single-company CRM and not an ERP replacement.

It provides:

- isolated company workspaces;
- shared identity and permissions;
- universal workflow/case/task/asset primitives;
- vertical industry packs;
- integration orchestration;
- role-specific interfaces;
- cross-company owner control;
- management intelligence.

## Core hierarchy

```text
Group
└── Organization
    └── BusinessUnit
        └── Object / Project / Location
            └── Process / Case / WorkOrder
```

The hierarchy is flexible: not every organization needs every level.

## Canonical terms

### Group

A management/ownership aggregation of organizations.

It is not assumed to be a legal holding company. Group membership is an application-level construct used for scoped cross-company access and analytics.

### Organization

A company or independent operational/legal business boundary.

An organization is a tenant and security boundary.

### BusinessUnit

A department, branch, region, service line, site team or other subdivision.

### User

A globally authenticated human account.

A User does not gain access merely by existing.

### Membership

Connects a User to a Group or Organization with explicit role/permission scope.

### Role / Permission

A Role is a reusable permission bundle.

Permission is the atomic authorization capability.

The system supports contextual restrictions in addition to role permissions.

### Person

A domain person: resident, client, employee contact, patient contact, etc. Do not assume every Person is an authenticated User.

### Counterparty

An external legal entity/self-employed/provider/contractor with which the organization interacts.

### Object

A managed business context.

Examples by vertical:

- property management: building/premise;
- construction: construction site/project object;
- fleet: depot or operational site;
- service: customer facility.

### Asset

A physical or logical asset with lifecycle/state/cost history.

Examples: pump, elevator, truck, excavator, production line.

### Case

An item that requires business handling and history.

Examples: complaint, request, defect, order, claim.

### Incident

A shared event/problem that may affect multiple cases/objects/people.

Example: one water outage with 100 resident reports.

### WorkOrder

Executable operational work assigned to a team/person/contractor.

### Task

A smaller actionable unit. Tasks may belong to workflows, cases, work orders, documents or projects.

### Workflow

Configured process logic: trigger → conditions → actions → SLA → escalation → result.

### Document

A business document and its metadata/status/linkage. The legally significant original may remain in an EDO system.

### FinancialEvent

A normalized management event describing money-related facts or intentions: invoice, payment, obligation, budget event, allocation. It is not a replacement for statutory accounting entries.

### Communication

A normalized inbound/outbound communication across email, telephony, messenger, SMS, web or another channel.

### Vertical Pack

A configuration/extension package that maps universal core primitives to a domain.

Initial target packs:

- Property Management;
- Construction;
- Fleet/Service.

### Owner Control

A separate UX abstraction for founders/owners/group-level managers.

Owner Control prioritizes:

- money;
- risk;
- deviations;
- health scores;
- assets;
- projects;
- contractors;
- management decisions.

It does not default to raw operational queues.

### System of Record

The authoritative source for a class of data.

Start may mirror and enrich external data without becoming its source of truth.

## Pilot framing

The initial pilot use case is the property-management operation of **Континент**.

The employee-facing system should cover the useful functional class of dispatching tools while using automation to reduce manual reading, copying, routing, reminding and reporting.

The pilot is a proving ground for the universal core, not a reason to hardcode property-management concepts into the core.

## Product success

The product is successful when:

- routine work becomes machine-handled;
- humans handle exceptions and decisions;
- managers control deviations rather than chase statuses;
- owners can safely see and manage all authorized businesses from one account;
- onboarding a new business becomes configuration/integration work rather than a new CRM codebase.
