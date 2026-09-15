# Start Team Skills

This directory defines the repository-local operating skills for the team building **Start** to production-grade quality.

These files are executable working instructions, not job descriptions.

## Mandatory rule

Before meaningful work, an author or coding agent MUST:

1. read `AGENTS.md`;
2. identify the applicable skill(s) below;
3. read those skill files before changing implementation;
4. follow their required evidence and handoff rules;
5. run `team/11-REVIEWER.skill.md` before merge.

**No change may be merged without Reviewer Skill evidence.**

For security-sensitive, data-sensitive, migration, infrastructure, integration, or AI-action changes, Reviewer Skill is necessary but not sufficient: the specialist review listed in `team/00-WORKING-AGREEMENT.md` is also required.

## Skill catalog

| Skill ID | Role | File |
|---|---|---|
| `team.tech-lead.v1` | Tech Lead / Principal Engineer | `01-TECH-LEAD.skill.md` |
| `team.backend.v1` | Senior Backend Engineer | `02-BACKEND.skill.md` |
| `team.security.v1` | Security / AppSec Engineer | `03-SECURITY.skill.md` |
| `team.platform-sre.v1` | Platform / SRE Engineer | `04-PLATFORM-SRE.skill.md` |
| `team.frontend.v1` | Senior Frontend Engineer | `05-FRONTEND.skill.md` |
| `team.qa.v1` | QA / Test Automation Engineer | `06-QA-AUTOMATION.skill.md` |
| `team.product-domain.v1` | Product / Domain Analyst | `07-PRODUCT-DOMAIN.skill.md` |
| `team.ai-llm.v1` | AI / LLM Engineer | `08-AI-LLM.skill.md` |
| `team.integration.v1` | Integration Engineer | `09-INTEGRATION.skill.md` |
| `team.ux.v1` | Product / UX Designer | `10-UX-PRODUCT-DESIGN.skill.md` |
| `team.reviewer.v1` | Independent Reviewer | `11-REVIEWER.skill.md` |
| `team.dba.v1` | DBA / Data Reliability Engineer | `12-DBA-DATA-RELIABILITY.skill.md` |

## How to declare skills in a PR

Add a section:

```text
Active skills:
- team.backend.v1
- team.security.v1

Review skills:
- team.reviewer.v1
- team.dba.v1
```

A PR without declared active skills and reviewer evidence is incomplete.

## Skill signature format

Each skill is signed with:

```text
START-TEAM::<skill-id>::v1
```

The signature identifies the operating contract version applied to the work.
