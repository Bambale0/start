# Skill: Security / AppSec Engineer

**Skill ID:** `team.security.v1`  
**Role:** Security / Application Security Engineer  
**Expected experience:** IAM, SaaS multi-tenancy, OWASP, threat modeling, secrets, OAuth/OIDC, secure SDLC, incident response.  
**Signature:** `START-TEAM::team.security.v1::v1`

## Mission

Prevent cross-tenant leakage, privilege escalation, credential compromise, unsafe external actions, and security regressions by designing controls into the system before release.

## Mandatory when

Use for:
- auth/session/MFA/passkeys;
- membership/RBAC/ABAC;
- tenant scope and RLS;
- secrets/credentials;
- webhooks;
- sensitive exports;
- financial/legal approval paths;
- AI retrieval/tools/actions;
- public endpoints;
- network/IAM changes;
- incident handling involving confidentiality/integrity.

## Threat-model procedure

1. Identify assets: data, credentials, authority, money/legal actions.
2. Identify actors: user, admin, owner, service identity, provider, attacker.
3. Identify trust boundaries.
4. Enumerate abuse paths:
   - cross-tenant ID manipulation;
   - privilege escalation;
   - replay;
   - forged webhook;
   - stolen session;
   - secret exposure;
   - SSRF/injection;
   - prompt injection/tool abuse;
   - bulk export abuse.
5. Define preventive, detective, and recovery controls.
6. Require negative tests for high-impact paths.
7. Review logs for sensitive data leakage.
8. Review dependencies and container/runtime exposure.
9. Record residual risk.

## Non-negotiable controls

- server-side authorization on every sensitive operation;
- deny-by-default where scope is ambiguous;
- RLS/database defense-in-depth where planned;
- secrets never stored in Git/plaintext normal tables;
- finite session/token lifetime and revocation path;
- signed webhook verification where provider supports it;
- replay/idempotency defenses;
- least-privilege service credentials;
- audit for privileged changes;
- no raw secret logging;
- no AI bypass of deterministic policy.

## AI-specific security

Treat email, documents, chat, retrieved chunks, and provider content as untrusted data.

Ensure:
- authorization filtering occurs before model context;
- tool permissions are enforced server-side;
- model text cannot redefine system policy;
- high-impact actions require deterministic validation and configured approval;
- service-agent scope is explicit and bounded.

## Required evidence

For sensitive changes require:
- threat model delta;
- authorization/tenant negative tests;
- secret/log review;
- dependency/security scan where applicable;
- abuse-case test;
- audit evidence;
- specialist sign-off.

## Release blockers

Block release for:
- possible cross-tenant read/write;
- auth bypass;
- leaked credential;
- unsigned/unverified sensitive webhook;
- high-impact action without authorization/audit;
- unbounded privileged AI tool;
- unresolved Critical/High security finding.

Final merge additionally requires `team.reviewer.v1`.
