## Outcome

What user/business outcome does this change deliver?

## Scope

What changed and what intentionally did not change?

## Architecture

- [ ] Universal core remains industry-agnostic.
- [ ] No mutable business/runtime configuration was hardcoded.
- [ ] Relevant ADRs/docs were reviewed or updated.

## Tenant / Security

- [ ] Tenant scope is explicit and server-enforced.
- [ ] Authorization impact was reviewed.
- [ ] No secrets or real customer data were added.

## Data / Integrations

Describe migrations, integration contract changes, idempotency/reconciliation impact.

## Observability

Describe logs, metrics, traces or audit added/changed.

## Tests

List exact checks run and results.

## Rollout / Risk

Describe migration, rollback/forward-fix and remaining risks.

## Team skills / merge gate

- Active skills:
  - `team.<skill>.v1`
- Risk class: low / medium / high
- Mandatory specialist reviews:
  - [ ] Identified from `team/00-WORKING-AGREEMENT.md`
  - [ ] Completed or N/A with rationale
- Reviewer Skill:
  - [ ] `team.reviewer.v1` applied to the current head SHA
  - Verdict: APPROVE / REQUEST_CHANGES
  - Critical findings: 0 / N
  - High findings: 0 / N
- Exact head SHA reviewed:

> Do not merge if Reviewer Skill evidence is missing, stale for the current head SHA, or has unresolved Critical/High findings.

