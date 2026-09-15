# Vertical Pack Model

## Goal

Support multiple industries without creating separate CRM codebases.

A Vertical Pack maps universal core primitives to a domain and provides configuration, UI composition and domain extensions.

## A pack may provide

- object types;
- asset types;
- case types;
- work-order types;
- default workflow templates;
- SLA templates;
- role templates;
- dashboards;
- forms;
- terminology/localization;
- validation extensions;
- domain-specific metrics;
- optional adapter mappings.

## A pack must not own

- authentication;
- global identity;
- tenant isolation;
- authorization engine;
- generic audit;
- generic workflow runtime;
- generic document transport;
- generic integration credential management;
- cross-company owner authorization.

Those remain platform responsibilities.

## Property Management pack

Examples:

```text
ObjectType:
  Building
  Premise

AssetType:
  Elevator
  Pump
  PipeSystem
  HeatingNode

CaseType:
  ResidentRequest
  Complaint
  ServiceRequest

WorkOrderType:
  Repair
  Inspection
  EmergencyResponse
  PlannedMaintenance

Capabilities:
  ResidentPortal
  HouseChatBot
  Inventory
  PlannedWorks
  LegalWorkspace
  CorrespondenceRegistry
  Estimates
  NotificationComposer
  MonthlyReporting
```

## Construction pack

Examples:

```text
ObjectType:
  ConstructionSite
  BuildingSection

AssetType:
  Equipment
  TemporaryInfrastructure

CaseType:
  Defect
  RFI
  SafetyIssue

WorkOrderType:
  Remediation
  Inspection
  ConstructionTask
```

## Fleet / Service pack

Examples:

```text
ObjectType:
  Depot

AssetType:
  Vehicle
  Trailer
  Equipment

CaseType:
  Breakdown
  MaintenanceNeed

WorkOrderType:
  Repair
  ScheduledMaintenance
  Inspection
```

## Pack configuration lifecycle

```text
Draft
→ Validate
→ Version
→ Publish
→ Apply to organization
→ Migrate configuration
→ Audit
```

Published pack versions are immutable. Changes create a new version.

Organizations may override explicitly allowed settings such as SLA, categories, labels and routing while retaining the pack's contracts.

## UI composition

The employee UI is composed from enabled capabilities.

Examples:

Property Management navigation may expose:

- Inbox / Requests;
- Buildings / Building 360;
- Residents;
- Incidents;
- Work Orders;
- Planned Works / PPR;
- Inventory / Assets;
- Legal Workspace;
- Documents / Registry;
- Estimates;
- Notifications;
- Tasks;
- Analytics.

Construction may expose:

- Projects;
- Sites;
- Defects;
- Contractors;
- Inspections.

The underlying platform still uses shared core APIs.

## Rule

If implementing a new vertical requires copying a core service, the architecture should be reviewed before proceeding.
