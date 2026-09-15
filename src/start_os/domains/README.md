# Domain Modules

This directory contains industry-agnostic business domains.

Planned modules:

- people
- counterparties
- objects
- assets
- cases
- incidents
- work
- workflows
- documents
- finance
- communications
- analytics

Rules:

- domain modules do not depend on provider SDK payloads;
- vertical terminology belongs in vertical packs;
- tenant scope and authorization are explicit;
- important mutations emit typed domain events;
- mutable business taxonomies come from configuration rather than source enums.
