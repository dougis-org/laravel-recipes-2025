---
description: Build an execution plan for a Jira ticket using TDD and repo context (planning mode).
---

**Goal:** Produce a concise, unambiguous implementation plan that a separate engineer/agent can execute without further clarification.

> Output only the plan (no extraneous narrative). Ask clarifying questions ONLY once if blocking gaps exist.

## Inputs

Required:

- Jira ticket key or URL: {{JIRA_KEY}}
  Optional:
- Additional links/refs: {{ADDITIONAL_LINKS_OR_PATHS}}
- Target date / milestone: {{TARGET_DATE_OR_MILESTONE}}

If the key is a URL, extract the key (e.g. SPCS-123). Validate pattern `[A-Z]+-[0-9]+`.

---

## Mode Guard (must pass before planning)

```
RESULT=$(scripts/detect-ticket-mode.sh "${USER_INPUT}")
STATUS=$(echo "$RESULT" | jq -r .status)
JIRA_KEY=$(echo "$RESULT" | jq -r .jiraKey)
```

Rules:

- need_ticket → request key & STOP
- work_mode → ask user to switch to work prompt; STOP if they confirm
- replan_recommended → show issues (.issues[]); proceed with adjustments after user acknowledgement
- ambiguous → ask user (plan vs work) → follow choice
- plan_mode → continue
  If a completed plan file already exists and user intent is implementation → direct them to `work-ticket`.

---

## Step 0: Ticket Verification & Branch Creation

1. Use the Atlassian MCP (Jira) server to fetch the issue (`jira_get_issue`); do NOT ask the user to paste raw ticket details unless the MCP server is unavailable. Confirm key format.
2. Ensure clean workspace (`git status` empty) and sync main:
   - `git checkout main && git pull --ff-only`
3. Determine branch prefix from Jira type (Bug→bugfix, Story/Feature/Task→feature, Improvement/Chore/Maintenance→chore, Spike/Investigation→spike) via the fetched issue type.
4. Create or reuse shared ticket branch:
   - Use the GitHub MCP server to list branches (`list_branches`) and to create a branch (`create_branch`).
   - `git switch -c <prefix>/{{JIRA_KEY}}-short-kebab-summary` (truncate ≤ ~60 chars) OR
   - `git switch <prefix>/{{JIRA_KEY}}-short-kebab-summary` if exists.
5. Confirm: "Planning {{JIRA_KEY}} on branch <prefix>/{{JIRA_KEY}}-short-kebab-summary".
6. Future Jira status/comments (e.g., decomposition decisions) must use Atlassian MCP actions (`jira_add_comment`, `jira_update_issue`)—never manual text unless MCP is unavailable (then note fallback in assumptions).
   (Shared conventions: `.github/prompts/includes/branch-commit-guidance.md`)

---

## Step 1: Ingest Ticket

Collect: title, description, acceptance criteria (AC), labels, components, links, comments, blockers, dependencies, security/performance notes.
Extract:

- Problem statement
- In-scope vs out-of-scope
- Functional requirements
- Non-functional (perf, security, compliance, availability)
- Dependencies (services, data, other tickets)
- Rollout expectations / flagging
- Success metrics & observability hooks
  Identify ambiguities & contradictions (list succinctly). If critical gaps, batch clarifying questions once, then proceed.

## Mode Guard
First, run the detection script and parse its JSON (pseudo):
```
RESULT=$(scripts/detect-ticket-mode.sh "${USER_INPUT}")
STATUS=$(echo "$RESULT" | jq -r .status)
JIRA_KEY=$(echo "$RESULT" | jq -r .jiraKey)
```
Rules:
- need_ticket → request key & STOP
- work_mode → ask user to switch to work prompt; STOP if they confirm
- replan_recommended → show issues (.issues[]); proceed with adjustments after user acknowledgement
- ambiguous → ask user (plan vs work) → follow choice
- plan_mode → continue
If a completed plan file already exists and user intent is implementation → direct them to `work-ticket`.

---
## Step 0: Ticket Verification & Branch Creation
1. Confirm ticket exists (light fetch / metadata) & key format.
2. Ensure clean workspace (`git status` empty) and sync main:
   - `git checkout main && git pull --ff-only`
3. Determine branch prefix from Jira type (Bug→bugfix, Story/Feature/Task→feature, Improvement/Chore/Maintenance→chore, Spike/Investigation→spike).
4. Create or reuse shared ticket branch:
   - `git switch -c <prefix>/{{JIRA_KEY}}-short-kebab-summary` (truncate ≤ ~60 chars) OR
   - `git switch <prefix>/{{JIRA_KEY}}-short-kebab-summary` if exists.
5. Confirm: "Planning {{JIRA_KEY}} on branch <prefix>/{{JIRA_KEY}}-short-kebab-summary".
(Shared conventions: `.github/prompts/includes/branch-commit-guidance.md`)

## Step 1.1: Decomposition Heuristic

If multiple separable deliverables (heuristics: >5 ACs, cross-layer changes, schema+API+flag, distinct capabilities), propose Work Breakdown Table:
| Slice | Key | Title | Type | Value | Depends | ACs | Effort (S/M/L) | Risks |
|-------|-----|-------|------|-------|---------|-----|----------------|-------|
Map each original AC to exactly one slice. Recommend: keep vs spin out (justification). Await user confirmation before splitting (no ticket creation here).

---

## Step 2: Repo & Doc Context Scan

Review: `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CHANGELOG.md`, `docs/**`, existing `docs/plan/tickets/*` for related keys.
Identify:

- Relevant modules/packages/classes
- Existing patterns for validation/logging/metrics/errors/retries/config/feature flags
- Similar implementations to reuse
- Existing flags; decide if new flag needed (`spcs.<domain>.<capability>.enabled`, default OFF)
- Architecture layering (controller → service → repo)
- API & schema governance (OpenAPI, migrations)
  Record only items materially affecting design.

---

## Step 3: Clarifications (Single Batch)

List only blocking items (privacy, auth roles, error contract, SLA/SLO changes, data retention, rollout cadence, owner approvals). After responses (or assumptions), proceed.

---

## Step 4: Plan Construction

Produce sections 1–11 exactly as specified (below). Each implementation step must cite concrete file paths or new file placeholders. Prefer existing utilities over new ones. Default new runtime behavior behind a flag unless trivial & low risk.
Persist the plan to `docs/plan/tickets/{{JIRA_KEY}}-plan.md` (create directory if missing). The persisted file content MUST match the output sections verbatim.

---

## Required Output Sections

### 1) Summary

- Ticket: {{JIRA_KEY}}
- One-liner: <what & why>
- Related milestone(s): <milestone IDs or n/a>
- Out of scope: <bullets>

### 2) Assumptions & Open Questions

- Assumptions: <bullets>
- Open questions (blocking -> need answers) numbered.

### 3) Acceptance Criteria (normalized)

Numbered list (testable, unambiguous).

### 4) Approach & Design Brief

Bullet subsections:

- Current state (key code paths)
- Proposed changes (high-level architecture & data flow)
- Data model / schema (migrations/backfill/versioning)
- APIs & contracts (new/changed endpoints + brief examples)
- Feature flags (name(s), default OFF, kill switch rationale)
- Config (new env vars + validation strategy)
- External deps (libraries/services & justification)
- Backward compatibility strategy
- Observability (metrics/logs/traces/alerts)
- Security & privacy (auth/authz, PII handling, rate limiting)
- Alternatives considered (concise)

### 5) Step-by-Step Implementation Plan (TDD)

Phases (RED → GREEN → Refactor). Enumerate steps with file specificity:

- Test additions first (unit, integration, contract, regression) ensuring initial FAIL
- Incremental implementation order (domain → service → repo → controller/API → migrations → flag wiring)
- Refactor pass (no behavior change)
- Docs & artifact updates (README, CHANGELOG, OpenAPI, drift script)
  Include validation command(s) for schema drift & build.

### 6) Effort, Risks, Mitigations

- Effort (S/M/L + rationale)
- Risks (ranked) with mitigation & fallback per item

### 7) File-Level Change List

`path/to/File.java`: add logic X
(New) `path/to/NewFile.kt`: purpose
Group logically (tests vs production vs docs).

### 8) Test Plan

Categorize: happy paths, edge/error, regression, contract, performance (if relevant), security/privacy checks, manual QA checklist.

### 9) Rollout & Monitoring Plan

- Flag(s) & default state
- Deployment steps (progressive enable / canary)
- Dashboards & key metrics
- Alerts (conditions + thresholds)
- Success metrics / KPIs
- Rollback procedure (exact commands/steps)

### 10) Handoff Package

- Jira link
- Branch & (future) PR name
- Plan file path
- Key commands (build/test/drift)
- Known gotchas / watchpoints

### 11) Traceability Map

| Criterion # | Requirement | Milestone | Task(s) | Flag(s) | Test(s) |
| ----------- | ----------- | --------- | ------- | ------- | ------- |

Every AC row filled (no blanks). Tasks reference milestone IDs if applicable.

---

## Working Rules

(See `.github/prompts/includes/branch-commit-guidance.md` for branch & commit hygiene.)

- Do NOT implement production code here.
- Challenge ambiguities; make ≤2 explicit assumptions if still unresolved.
- Reuse existing patterns & utilities; avoid speculative abstractions.
- Signed commits (-S) with conventional format when committing the plan.
- New runtime behavior behind feature flag unless justified.
- Keep plan deterministic, minimal, test-driven, traceable.
- Dependency versions: If referencing an existing dependency, default to the version already declared in the project. For any new dependency (plugin, library, tool) required by the ticket, use the Context7 MCP server to resolve and retrieve the latest stable release version at plan time; cite that version explicitly in the plan (pin it) and note the retrieval date. If Context7 is unavailable, add an assumption and specify a placeholder `LATEST` tag to be resolved during implementation.
- Scope limit: Once the plan is fully accepted (all sections complete, no open blocking questions) and the plan file is committed & pushed, this planning session terminates. Do not proceed to implementation steps here; direct any further work to the `work-ticket` prompt and clear transient context.

## Commit & Push (after writing plan file)

```
git add docs/plan/tickets/{{JIRA_KEY}}-plan.md
git commit -S -m "chore(plan): {{JIRA_KEY}} add implementation plan"
git push -u origin <prefix>/{{JIRA_KEY}}-short-kebab-summary
```

Open PR referencing the plan file; request CODEOWNERS.

## Sanity Checklist (mentally tick)

- ACs testable & mapped
- Each step has concrete file path(s)
- Risks have mitigation + fallback
- Observability & security addressed
- Feature flag(s) named & default OFF (or justification)
- Traceability table complete
- Plan file persisted at correct path

## Output Instruction

Return ONLY the 11 sections in order (no extra commentary). If blocking gaps remain after the one clarification batch, list them in Section 2 and proceed with explicit assumptions.
