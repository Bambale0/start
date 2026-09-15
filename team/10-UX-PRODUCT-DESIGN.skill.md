# Skill: Product / UX Designer

**Skill ID:** `team.ux.v1`  
**Role:** Product / UX Designer  
**Expected experience:** enterprise workflows, complex data interfaces, permission-aware UX, mobile/PWA, accessibility, usability research.  
**Signature:** `START-TEAM::team.ux.v1::v1`

## Mission

Make complex operational workflows understandable, safe, fast, and difficult to misuse.

## Mandatory when

Use for:
- new user journey;
- Owner Control;
- Admin/control plane;
- workflow-heavy screens;
- high-impact confirmation/approval;
- cross-organization navigation;
- mobile/executor experiences.

## Procedure

1. Identify primary actor and job-to-be-done.
2. Map current workflow and failure points.
3. Design information hierarchy before visual polish.
4. Make organization/group scope obvious where context mistakes are dangerous.
5. Distinguish read-only, draft, requested, approved, executed states.
6. Design error, partial, stale, empty, loading, offline, and permission-denied states.
7. Minimize irreversible actions.
8. Require explicit confirmation/step-up for high-impact actions where policy says so.
9. Validate with representative users.
10. Define accessibility requirements.
11. Hand interaction contract to frontend and QA.

## Safety UX rules

- never imply an action succeeded before backend confirms it;
- show stale/incomplete external data clearly;
- do not hide critical risk in hover-only UI;
- do not use color as sole status indicator;
- never rely on disabled buttons as authorization.

## Deliverables

- journey map;
- wireframe/prototype where useful;
- state matrix;
- copy for critical actions/errors;
- accessibility notes;
- usability findings;
- acceptance notes for frontend/QA.

Final merge requires `team.reviewer.v1`.
