# Start — AI Business OS

> Working name for a multi-company operating system that unifies day-to-day operations, integrations, analytics and owner-level control without replacing specialized systems such as 1C, EDI/EDO providers or banks.

## Product thesis

Each company receives its own isolated operational workspace tailored to its business domain. Employees see only the company, objects, processes and permissions relevant to their work.

Owners and founders use a global account with access to the companies and groups where they have explicit membership. Their interface is intentionally different from the employee CRM: it focuses on money, risks, deviations, assets, projects, quality and decisions that require management attention.

The platform's purpose is to:

- reduce manual operational work;
- remove dependence on inboxes, chats and spreadsheets;
- lower cost per business operation;
- improve SLA, quality and auditability;
- connect existing 1C, EDO, banks, telephony, email and messengers into one workflow layer;
- give owners a single control surface across several independent businesses;
- make new industry deployments configuration-driven instead of separate CRM rewrites.

## First proving ground

The first vertical pack is **Property Management**, with `Континент` as the pilot use case.

The pack is expected to cover the useful functional class of dispatching platforms such as Dispatcher24:

- omnichannel intake;
- resident/customer cases;
- buildings and managed objects;
- dispatching and work orders;
- executors and contractors;
- SLA;
- incidents and mass outages;
- notifications;
- operator and manager dashboards;
- analytics.

The differentiator is not another ticketing UI. The platform automates intake, classification, deduplication, routing, reminders, escalation and reporting, and then exposes the same universal core to construction, fleet/service and other businesses.

## Product layers

```text
                         START / BUSINESS OS
                                 │
                  ┌──────────────┴──────────────┐
                  │                             │
            GLOBAL IDENTITY                 GROUP LAYER
                  │                             │
          Users / Memberships              Owner Control
          Roles / Permissions              Group Analytics
                  │                         Owner AI
       ┌──────────┼──────────┐                  │
       │          │          │                  │
   Tenant A    Tenant B   Tenant C              │
  Континент    Стройка    Автопарк              │
       │          │          │                  │
   Vertical    Vertical   Vertical              │
     Pack        Pack       Pack                │
       └──────────┬──────────┘                  │
                  ▼                             │
             UNIVERSAL CORE ◄───────────────────┘
                  │
      Workflow / Cases / Tasks / Assets
      Documents / Finance Events / Comms
      Analytics / Audit / Integration Hub
                  │
      ┌───────────┼────────────┬────────────┐
      ▼           ▼            ▼            ▼
      1C          EDO         Banks      Channels
```

## Architectural principles

1. **One universal core, many vertical packs.** Industry-specific behavior is configuration and extension, not duplicated core logic.
2. **Hard tenant isolation.** A company is an independent security and data boundary.
3. **Global identity, scoped membership.** A person has one account; access comes from explicit group/company memberships and permissions.
4. **Role-specific UX.** Worker, manager, director and owner receive different abstractions over the same data.
5. **Owner attention is scarce.** Healthy operations stay quiet; deviations are escalated with context and recommended actions.
6. **Existing systems remain systems of record where appropriate.** 1C owns statutory accounting, EDO owns legally significant originals, banks own balances and transactions; Start owns operational workflows and management intelligence.
7. **Configuration over hardcode.** Mutable business rules, statuses, SLA, routing, thresholds, integrations and feature availability must be data-driven and admin-managed.
8. **Events over hidden coupling.** Important state changes emit auditable domain events.
9. **Observability from day one.** Technical telemetry and business-process telemetry are part of the definition of done.
10. **Automation must be measurable.** Human Intervention Rate, cost per case, SLA, rework and management attention are first-class product KPIs.
11. **Fail closed on sensitive automation.** Money, signatures, access, destructive actions and low-confidence AI decisions require explicit controls.
12. **Modular monolith first.** Keep domain boundaries clean; split services only when scale or isolation justifies it.

## Repository map

- [AGENTS.md](AGENTS.md) — mandatory engineering rules for agents and contributors.
- [CONTEXT.md](CONTEXT.md) — domain vocabulary and product context.
- [docs/product/PRODUCT_SPEC.md](docs/product/PRODUCT_SPEC.md) — product requirements and personas.
- [docs/architecture/SYSTEM_ARCHITECTURE.md](docs/architecture/SYSTEM_ARCHITECTURE.md) — target architecture.
- [docs/architecture/DOMAIN_MODEL.md](docs/architecture/DOMAIN_MODEL.md) — canonical domain model.
- [docs/architecture/SECURITY.md](docs/architecture/SECURITY.md) — tenancy, authorization and security.
- [docs/architecture/INTEGRATIONS.md](docs/architecture/INTEGRATIONS.md) — integration hub and system-of-record rules.
- [docs/architecture/OBSERVABILITY.md](docs/architecture/OBSERVABILITY.md) — logs, traces, metrics and audit.
- [docs/specs/CONTINENT_PROPERTY_MANAGEMENT.md](docs/specs/CONTINENT_PROPERTY_MANAGEMENT.md) — first vertical/pilot specification.
- [docs/specs/OWNER_CONTROL.md](docs/specs/OWNER_CONTROL.md) — global owner experience.
- [docs/roadmap/IMPLEMENTATION_PLAN.md](docs/roadmap/IMPLEMENTATION_PLAN.md) — phased delivery plan.
- [docs/testing/TEST_STRATEGY.md](docs/testing/TEST_STRATEGY.md) — testing and quality gates.
- [docs/adr/](docs/adr/) — architecture decisions.

## Initial technical direction

- Python 3.12+
- FastAPI
- PostgreSQL
- SQLAlchemy 2.x + Alembic
- Redis for cache/coordination where justified
- asynchronous workers behind a queue abstraction
- React/TypeScript frontends planned as separate apps for office/manager and owner control
- OpenTelemetry-compatible tracing
- structured logging
- Docker-first local/prod packaging
- GitHub Actions CI

The exact infrastructure provider, queue implementation, frontend framework details and external integration vendors are intentionally replaceable behind contracts.

## Delivery strategy

The first commercial path is:

```text
Universal Core
    ↓
Континент Property Management Pack
    ↓
Automate dispatch/operator routine
    ↓
Measure real savings and quality
    ↓
Manager analytics
    ↓
Owner Control
    ↓
Connect second company
    ↓
Prove cross-industry universality
    ↓
Group-wide rollout
    ↓
Productize as standalone B2B SaaS/platform
```

See the implementation plan for scope and acceptance gates.
