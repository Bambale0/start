# Security, Tenancy and Authorization

## 1. Threat model summary

Start can aggregate operational, financial, document and communication data across several companies. A tenant leak or owner-account compromise is therefore a critical failure.

Primary risks:

- cross-tenant data leakage;
- privilege escalation;
- compromised owner account;
- leaked integration credentials;
- insecure webhook processing;
- unauthorized payment/signature actions;
- AI prompt/data exfiltration;
- audit tampering;
- stale/revoked access remaining active.

## 2. Identity

Use central authentication.

A user has one global account and may hold multiple memberships.

Recommended maturity path:

- password or federated login;
- MFA;
- WebAuthn/passkeys;
- device/session management;
- risk-based step-up authentication.

Group owners/high-privilege admins should require stronger authentication than ordinary low-risk roles.

## 3. Tenant isolation

Defense in depth:

### API layer

Resolve memberships server-side.

Reject any selected organization not present in the actor's authorized scope.

### Service layer

Pass a typed authorization/tenant context to application services.

### Repository layer

Tenant-aware repository methods.

### Database layer

Use PostgreSQL Row Level Security for tenant-bound tables when practical.

Example concept:

```text
current organization scope
→ DB session setting/context
→ RLS policy
→ rows restricted to authorized tenant
```

Do not treat RLS as a replacement for application authorization. It is an additional guard.

## 4. Owner/group access

A founder's account is not an unrestricted superuser.

Model:

```text
User
→ GroupMembership
→ Group permissions
→ authorized organizations
```

Possible permissions:

- group.companies.read;
- group.analytics.read;
- group.finance.read;
- group.documents.read;
- group.operations.drilldown;
- group.memberships.manage.

Individual organization permissions may further restrict actions.

A person can therefore have broad visibility but not payment/signature authority.

## 5. RBAC + contextual policy

RBAC provides reusable roles.

Contextual rules restrict data/actions by:

- business unit;
- assigned object;
- own tasks;
- document type;
- amount;
- risk level;
- organization;
- group.

Every sensitive backend endpoint performs authorization independently of frontend visibility.

## 6. Step-up authentication

Require recent stronger authentication for high-impact actions such as:

- managing owner memberships;
- rotating integration credentials;
- changing security policies;
- approving high-value payment requests;
- initiating legal signature flows;
- exporting large sensitive datasets.

Thresholds are configurable policy, not hardcoded product values.

## 7. Secrets

Never store plaintext provider secrets in normal application tables.

Use:

- cloud secret manager / Vault-like system; or
- envelope encryption with a separately managed master key.

Application DB stores secret references and metadata.

Admin UI:

- create/replace;
- test connection;
- rotate;
- revoke.

After save, display masked values only.

## 8. Webhooks

Every provider adapter must:

- validate signature/authenticity when available;
- reject stale/replayed signed requests when protocol supports it;
- use idempotency/deduplication;
- record provider event ID;
- respond quickly and queue heavy processing;
- never trust payload tenant identity without mapping it to a known IntegrationConnection.

## 9. Sensitive data

Apply least collection.

Classify data at least into:

- public/non-sensitive;
- internal business;
- personal data;
- financial;
- credential/secret;
- high-sensitivity document.

Logging defaults must avoid full raw payloads.

## 10. Audit

Append-oriented audit required for:

- login/security events;
- role/membership changes;
- integration changes;
- workflow config publication;
- financial approval;
- document approval/signature initiation;
- destructive/archive actions;
- privileged data export.

Audit records should capture actor, scope, action, target, request/trace and outcome.

## 11. AI security

### Authorization before retrieval

AI only receives data the actor is authorized to access.

Do not rely on the model to “remember not to mention another tenant.”

### Tool authorization

Each tool/action invoked by AI is authorized server-side.

### Prompt injection

Treat external emails, documents, chats and provider content as untrusted data, not instructions.

Do not allow document text to redefine system/tool policies.

### High-impact actions

AI may recommend, prepare or route high-impact actions but cannot silently bypass configured human approvals.

## 12. Session security

Support:

- short-lived access tokens/sessions;
- refresh rotation or secure server sessions;
- revocation;
- device/session list;
- logout-all;
- new-device notification for high-privilege accounts;
- rate limiting/brute-force protection.

## 13. Network and service security

- TLS everywhere;
- private DB/cache networks where possible;
- least-privileged service credentials;
- egress restrictions for sensitive workers when practical;
- dependency and image scanning;
- regular patching.

## 14. Backups

- encrypted backups;
- point-in-time recovery for PostgreSQL;
- documented retention;
- restore testing;
- access controls separate from app operators when possible.

A backup that has never been restored is not a verified backup.

## 15. Security release blockers

Do not release if:

- tenant isolation tests fail;
- an endpoint trusts client tenant scope without validation;
- secret appears in repository/logs;
- webhook authenticity is required but unimplemented;
- sensitive action lacks authorization/audit;
- owner privileges are implemented as hidden hardcoded user IDs.
