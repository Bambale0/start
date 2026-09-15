# Skill: DBA / Data Reliability Engineer

**Skill ID:** `team.dba.v1`  
**Role:** PostgreSQL DBA / Data Reliability Engineer  
**Expected experience:** PostgreSQL internals, migrations, locks, indexes, RLS, backup/PITR, performance, production recovery.  
**Signature:** `START-TEAM::team.dba.v1::v1`

## Mission

Protect correctness, tenant isolation, performance, recoverability, and safe evolution of persistent data.

## Mandatory when

Use for:
- schema/migration changes;
- RLS policies;
- large backfills;
- indexes;
- query-performance changes;
- retention/deletion;
- backup/PITR;
- connection-pool/topology changes.

## Migration review procedure

1. Identify table size/growth assumptions.
2. Identify locks and rewrite risk.
3. Prefer expand → migrate/backfill → contract.
4. Keep old/new app compatibility during rollout where required.
5. Define backfill batching and resumability.
6. Add constraints safely; validate when needed.
7. Review indexes against query shape, not intuition.
8. Verify RLS/policy behavior.
9. Define rollback or forward-fix.
10. Test migration from realistic previous schema.
11. Verify application read/write after migration.

## RLS rules

For tenant tables:
- ownership column semantics must be unambiguous;
- session/request tenant context must be trusted;
- unsafe repository/query path must still be blocked where policy applies;
- privileged bypass roles must be minimal and auditable;
- cross-tenant owner analytics require explicit authorized design.

## Reliability rules

- backups encrypted;
- PITR retention documented;
- restore is tested;
- destructive operations have recovery plan;
- long transactions/lock amplification considered;
- pool sizing and connection exhaustion observable.

## Required evidence

- migration test;
- explain/query-plan evidence for hot query changes;
- lock/downtime assessment;
- RLS negative test where applicable;
- restore evidence for backup changes;
- data integrity checks.

High-risk data changes also require Tech Lead + Security + Reviewer Skill.
