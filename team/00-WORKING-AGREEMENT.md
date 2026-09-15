# Start Team Working Agreement

**Document ID:** `team.working-agreement.v1`  
**Status:** Mandatory  
**Signature:** `START-TEAM::team.working-agreement.v1::v1`

## 1. Purpose

This agreement defines how production-grade changes are designed, implemented, verified, reviewed, and merged.

It applies to humans and coding agents.

## 2. Core delivery loop

Every meaningful change follows this sequence:

```text
discover
→ classify risk
→ select active team skills
→ inspect current implementation
→ state acceptance criteria
→ implement smallest safe vertical slice
→ run focused verification
→ run broader verification
→ specialist review(s)
→ Reviewer Skill
→ green CI on exact SHA
→ merge
```

Do not skip directly from implementation to merge.

## 3. Change classification

### Low risk
Examples:
- typo/documentation clarification;
- non-behavioral refactor with strong tests;
- internal developer tooling that cannot reach production state.

Required:
- author skill;
- `team.reviewer.v1`.

### Medium risk
Examples:
- normal API/domain feature;
- UI behavior;
- new internal event;
- non-destructive schema addition;
- new background job without sensitive authority.

Required:
- author skill;
- relevant specialist skill;
- `team.qa.v1` evidence where behavior changes;
- `team.reviewer.v1`.

### High risk
Examples:
- authentication/authorization/tenancy;
- RLS/security boundaries;
- secrets/credentials;
- financial or legal actions;
- AI tool/action authority;
- webhook verification;
- migrations touching existing data;
- external writes;
- deployment/network/IAM;
- backup/restore;
- cross-tenant reporting;
- destructive operations.

Required:
- author skill;
- Tech Lead review;
- Security review;
- relevant specialist review;
- QA/release evidence;
- independent `team.reviewer.v1`;
- green CI on exact SHA;
- no unresolved Critical/High finding.

## 4. Required specialist review matrix

| Change surface | Mandatory specialist skill |
|---|---|
| Auth, permissions, tenancy, RLS, secrets, webhooks | `team.security.v1` |
| Database schema, migration, indexes, locking, backup | `team.dba.v1` |
| Deployment, CI/CD, runtime, networking, observability | `team.platform-sre.v1` |
| External provider/API integration | `team.integration.v1` |
| AI retrieval, tool use, prompts, model policy, evals | `team.ai-llm.v1` + `team.security.v1` |
| Frontend user workflow | `team.frontend.v1` |
| Material UX/interaction change | `team.ux.v1` |
| Business semantics/workflow requirements | `team.product-domain.v1` |
| Cross-module architecture/boundary change | `team.tech-lead.v1` |

## 5. Merge gate — absolute rule

**Never merge without applying `team.reviewer.v1`.**

A merge is allowed only when all applicable conditions are true:

- PR declares active skills;
- implementation matches acceptance criteria;
- required specialist reviews are complete;
- Reviewer Skill report exists;
- Critical findings = 0;
- High findings = 0;
- Medium findings are fixed or explicitly accepted by the project owner with rationale;
- tests/checks appropriate to the change pass;
- CI is green for the exact head SHA;
- migrations/rollback or forward-fix plan is documented when applicable;
- tenant/security impact is explicitly reviewed;
- observability and audit impact is addressed;
- docs/ADRs/context are updated when behavior or architecture changed.

A coding agent MUST NOT call a merge action merely because CI is green.

## 5A. GitHub server-side enforcement

Repository process rules are not sufficient by themselves. The default branch MUST be protected by a GitHub branch protection rule or repository ruleset.

Required GitHub enforcement for `main`:

- require a pull request before merging;
- require at least 1 independent approving review;
- require at least one independent approving review;
- dismiss stale approvals when new commits are pushed;
- require Code Owner review only after independent code-owner users/teams are configured;
- require approval of the most recent reviewable push when available;
- require the repository CI status check to pass before merge;
- require branches to be up to date before merge;
- require conversation resolution before merge;
- block force pushes;
- block branch deletion;
- apply the rule to administrators/bypass actors as strictly as the repository plan allows;
- do not permit direct pushes to `main`.

The repository-local `team.reviewer.v1` review complements GitHub approval. Neither replaces the other.

A merge is valid only when both layers agree:

```text
GitHub protected-branch/ruleset gates green
+
team.reviewer.v1 APPROVE for current head SHA
=
merge eligible
```

## 6. Separation of duties

For Medium and High risk changes, the final Reviewer Skill should be performed independently from implementation whenever possible.

For High risk changes, self-review does not count as the final production approval.

The reviewer must be willing to block the change.

## 7. Evidence standard

Never report “tested”, “secure”, “works”, “production-ready”, or “green” without evidence.

Evidence should name:
- exact command/check;
- result;
- exact commit SHA where relevant;
- environment;
- important fixtures/services;
- known limitations.

## 8. Stop conditions

Stop merge/release when:
- authorization behavior is ambiguous;
- tenant isolation is unverified;
- a secret may have leaked;
- migration safety is unknown;
- a destructive path lacks recovery;
- an external mutation lacks idempotency/reconciliation;
- AI can bypass deterministic authorization/approval;
- production readiness depends on an untested assumption;
- required reviewer cannot validate the change.

## 9. Severity vocabulary

**Critical:** credible tenant leak, auth bypass, secret compromise, data loss, unauthorized financial/legal action, remote code execution, unrecoverable corruption.

**High:** likely production outage, privilege escalation path, unsafe migration, repeatable duplicate side effect, missing security control on sensitive path.

**Medium:** maintainability/reliability defect likely to cause future bugs or operational pain.

**Low:** localized quality/documentation/style issue with limited runtime risk.

## 10. Required PR evidence block

```text
Active skills:
- ...

Risk class:
- low | medium | high

Acceptance criteria:
- ...

Verification:
- command/check → result
- ...

Specialist reviews:
- skill → reviewer/evidence

Reviewer Skill:
- team.reviewer.v1
- verdict: APPROVE | REQUEST_CHANGES
- blocking findings: ...

Exact head SHA:
- ...
```
