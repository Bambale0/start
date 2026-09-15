# Operations Runbook — Foundation

This runbook evolves with deployment infrastructure.

## Deployment pre-check

Verify:

- exact commit SHA;
- CI green for that SHA;
- required secrets/config available;
- migration plan reviewed;
- backup/restore posture adequate;
- integration changes documented;
- tenant/security tests green;
- rollback or forward-fix plan understood.

## Post-deploy smoke

Verify:

- liveness;
- readiness;
- API process;
- database migration state once DB is mandatory;
- worker health;
- queue health;
- critical integration health;
- error rate/logs;
- one safe synthetic business journey where possible.

## Incident first response

Capture:

- start time;
- affected environment;
- affected organizations/capabilities;
- symptoms;
- trace/request/provider IDs;
- recent deploy/config changes.

Prefer diagnosis from telemetry over speculative patching.

## Integration degradation

If a provider is unavailable:

- expose degraded or stale state;
- queue only safe retriable work;
- avoid blind mutation retry after unknown result;
- reconcile before repeating uncertain writes.

## Database

Before destructive/data migrations:

- verify backup;
- estimate lock/scan impact;
- prefer expand/migrate/contract;
- monitor errors/latency;
- keep a forward-fix path.

## Security event

For suspected credential compromise:

- revoke/rotate credential;
- invalidate affected sessions where appropriate;
- preserve audit evidence;
- identify scope;
- review provider logs;
- document incident and permanent control improvement.

## Backups

Target architecture requires:

- encrypted PostgreSQL backups;
- point-in-time recovery;
- documented retention;
- periodic restore tests.

Do not state restore capability is proven until a restore has actually been tested.
