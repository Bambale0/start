# ADR 0005 — Global Identity with Scoped Memberships

**Status:** Accepted

## Context

Employees should experience one isolated company application, while founders may need access to several organizations from one account/device.

Hardcoded owner/admin IDs and tenant-local duplicate accounts are unsafe and hard to manage.

## Decision

A human has one global User identity.

Access is granted through explicit memberships scoped to:

- Group;
- Organization;
- BusinessUnit.

Roles are permission bundles. Contextual policies may further restrict access.

Owner/founder status is represented by membership/permissions, not a hidden superuser flag.

## Consequences

One person can have different roles in different organizations.

Revocation is centralized.

Owner Control can aggregate only the organizations authorized through group/org scope.

High-impact owner actions may require stronger/step-up authentication independently of read access.
