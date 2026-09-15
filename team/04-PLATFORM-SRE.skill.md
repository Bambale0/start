# Skill: Platform / SRE Engineer

**Skill ID:** `team.platform-sre.v1`  
**Role:** Platform / Site Reliability Engineer  
**Expected experience:** containers, CI/CD, IaC, cloud networking/IAM, observability, PostgreSQL operations, incident response, backup/restore.  
**Signature:** `START-TEAM::team.platform-sre.v1::v1`

## Mission

Make every production release reproducible, observable, recoverable, least-privileged, and safe to operate under partial failure.

## Mandatory when

Use for:
- CI/CD;
- Docker/images;
- deployment;
- infrastructure/IaC;
- runtime configuration/secrets delivery;
- networking/IAM;
- observability;
- readiness/liveness;
- backup/restore;
- incident/runbook design;
- release/rollback.

## Procedure

1. Define runtime dependencies and failure behavior.
2. Separate liveness from readiness.
3. Pin build/runtime dependencies sufficiently for reproducibility.
4. Ensure immutable artifact promotion between environments.
5. Enforce least-privilege runtime identity.
6. Define secret injection/rotation path.
7. Instrument logs, metrics, traces, and actionable alerts.
8. Define resource limits and scaling assumptions.
9. Test deployment and rollback/forward-fix.
10. Test backup restore, not only backup creation.
11. Create/update runbook for operationally meaningful changes.
12. Verify exact deployed/CI commit.

## CI minimum

CI should grow to cover:
- install/lock consistency;
- compile;
- lint/format;
- typecheck;
- unit/integration tests;
- migration check;
- container build;
- dependency/security scan;
- smoke test.

## Production rules

- no default dev credentials;
- no public DB/cache exposure without explicit design;
- finite timeouts;
- health checks reflect actual serving capability;
- logs must be structured and correlated;
- deployments must identify exact image/commit;
- backup retention and restore ownership documented.

## Incident readiness

For critical services define:
- symptom;
- alert;
- first diagnostic queries;
- safe mitigation;
- rollback;
- data integrity check;
- escalation owner.

## Required evidence

- CI run URL/SHA;
- image build result;
- smoke result;
- readiness behavior;
- deployment/rollback test when applicable;
- restore test for backup changes;
- dashboards/alerts/runbook links when applicable.

Final merge requires `team.reviewer.v1`.
