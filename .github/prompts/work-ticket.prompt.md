---
description: Execute an approved implementation plan for a Jira ticket.
---
**Goal:** Implement the plan produced by `plan-ticket` with TDD, quality gates, and Jira + branch hygiene.

> This prompt assumes a plan file already exists. If not, run `plan-ticket`.

## Inputs
Required:
- **Jira ticket key:** {{JIRA_KEY}}
Optional:
- **Plan file:** `docs/plan/tickets/{{JIRA_KEY}}-plan.md` (default)
- **Repo root:** current workspace

---
## Mode Guard
```
RESULT=$(scripts/detect-ticket-mode.sh "${USER_INPUT}")
STATUS=$(echo "$RESULT" | jq -r .status)
JIRA_KEY=$(echo "$RESULT" | jq -r .jiraKey)
```
STATUS rules:
- need_ticket → request key & STOP
- plan_mode → ask to switch to planning; abort if yes
- replan_recommended → show issues; STOP until corrected
- ambiguous → ask user (plan/work)
- work_mode → continue

Additional validation:
- Plan file must exist & contain sections 1–10 (11 if present)
- Warn if stale (diagnostics) → require confirmation
- Redirect if user intent is scoping vs coding

---
## Phase 0: Parameters + Plan Load
0.1 Fetch Jira issue via Atlassian MCP (Jira) server (`jira_get_issue`); never ask user to paste ticket unless MCP unavailable (then record assumption). Validate key format `[A-Z]+-[0-9]+`.
0.2 Load plan; parse sections; fail fast if missing.
0.3 Summarize (Sections 1,3,5) for confirmation.
0.4 If not already In Progress, use MCP to transition (`jira_transition_issue`) and add start comment (`jira_add_comment`). If MCP fails, note fallback and proceed cautiously.

## Mode Guard
```
RESULT=$(scripts/detect-ticket-mode.sh "${USER_INPUT}")
STATUS=$(echo "$RESULT" | jq -r .status)
JIRA_KEY=$(echo "$RESULT" | jq -r .jiraKey)
```
STATUS rules:
- need_ticket → request key & STOP
- plan_mode → ask to switch to planning; abort if yes
- replan_recommended → show issues; STOP until corrected
- ambiguous → ask user (plan/work)
- work_mode → continue

Additional validation:
- Plan file must exist & contain sections 1–10 (11 if present)
- Warn if stale (diagnostics) → require confirmation
- Redirect if user intent is scoping vs coding

(See `includes/branch-commit-guidance.md` for naming & commit rules.)

---
## Phase 2: TDD (RED)
2.1 Unit tests (nominal + boundary + error) 
2.2 Integration tests (containers/mocks) 
2.3 Contract/API tests (OpenAPI variants & error codes) 
2.4 Regression tests (historical bugs) 
2.5 Ensure new tests FAIL (prove validity)

---
## Phase 3: Implement (GREEN)
3.1 Domain / DTOs
3.2 Service interfaces + impls
3.3 Data layer (repos, indexes)
3.4 Controllers / API (validation, auth)
3.5 Config / env vars (+ validation)
3.6 Migrations (backward compatible)
3.7 Feature flag wiring (default OFF)
3.8 Iterate `./gradlew test` until GREEN
3.9 Refactor (no behavior change)

---
## Phase 4: Docs & Artifacts
4.1 Update README / module docs
4.2 Update CHANGELOG
4.3 Update runbooks / dashboards / alerts
4.4 If schema changed:
   - Update schema artifacts + init scripts
   - Update `docs/api/openapi.yaml` & Bruno collection
   - `node scripts/check-schema-drift.js` → PASS

---
## Phase 5: Quality Gates
| Gate | Command / Action | Pass |
|------|------------------|------|
| Build & Unit | `./gradlew test` | All green |
| Integration | `./gradlew integrationTest` (if exists) | Green |
| Contract/API | Contract suite | All validate |
| Lint/Style | Repo tooling | No blocking issues |
| Schema Drift | `node scripts/check-schema-drift.js` | No drift |
| Security/Input | Review validation & logging | Safe, no secrets |
| Feature Flags | Confirm default OFF or justified | Documented |
| Coverage | Compare baseline | No unjustified drop |

Failures → fix root cause (never dilute tests).

---
## Phase 6: Acceptance Verification
6.1 Load ACs (Section 3) 
6.2 Map each AC → tests (unit/integration/contract) 
6.3 Negative & error path spot checks 
6.4 Document deviations (justify or request plan update)

---
## Phase 7: Commit & PR
7.1 `git add .`
7.2 `git commit -S -m "feat(<scope>): {{JIRA_KEY}} <concise summary>"` (use `fix|chore|refactor|docs|test` as appropriate)
7.3 `git push -u origin <prefix>/{{JIRA_KEY}}-short-kebab-summary`
7.4 Open PR (template) including: ticket, plan link, summary, risk (plan §6), rollout (plan §9), test evidence, flag usage
7.5 Request CODEOWNERS & domain reviewers
7.6 Comment PR link in Jira & transition → Code Review

---
## Phase 8: Handoff Summary (Output)
- Files changed (count + key paths)
- New tests by category
- Flags introduced
- Outstanding risks / mitigations
- Next steps (review → merge → deploy)

---
## Error Matrix
| Issue | Action |
|-------|--------|
| Missing plan section | STOP; request fix |
| All tests pass in RED | Strengthen tests |
| Build fail | Fix latest change / revert then retest |
| Drift fail | Update artifacts → rerun drift check |
| Jira transition fail | Log + proceed; notify user |
| Ambiguous instruction | Batch clarifying question |

Escalate after 2 failed remediation attempts.

---
## Verification Checklist
- [ ] Jira status updated + PR link
- [ ] All new tests added & GREEN
- [ ] Schema artifacts & drift check (if schema)
- [ ] Feature flag(s) documented (default OFF)
- [ ] Signed conventional commit(s)
- [ ] PR open & reviewers requested
- [ ] Each AC satisfied or deviation documented
- [ ] Handoff summary produced

## Success Criteria
PR open, tests green, ACs verified, Jira updated, handoff summary delivered.

## Working Rules
- Strict TDD (RED → GREEN → Refactor)
- No scope creep beyond plan
- Reuse existing patterns; cite reused modules
- CONTRIBUTING.md overrides plan
- No production logic without tests
- New behavior behind feature flag unless trivial & low risk

---
## References
- Shared guidance: `.github/prompts/includes/branch-commit-guidance.md`
- Plan schema (optional validation aid): `.github/prompts/includes/plan-file-structure.schema.json`
