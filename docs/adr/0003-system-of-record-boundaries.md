# ADR 0003 — Systems of Record Stay Specialized

**Status:** Accepted

## Context

The product aims to give users one operational window, but rewriting accounting, EDO and banking systems would add risk and destroy focus.

## Decision

Start is the system of record for:

- operational workflows;
- cases/incidents/work orders/tasks;
- platform configuration;
- memberships/authorization;
- audit;
- management analytics derived by the platform.

External authoritative systems remain authoritative for their classes:

- 1C/accounting → statutory accounting;
- EDO provider → legally significant document original/signature state;
- bank → actual account balance/transaction state.

Start mirrors, links, reconciles and orchestrates these systems through adapters.

## Consequences

The UI can be unified without pretending all data originates locally.

Every integration must display freshness and reconciliation state.

External write capabilities require explicit approval/security design.
