---
description: Build an execution plan for a GitHub issue using TDD and repo context (planning mode).
---

**Goal:** Produce a concise, unambiguous implementation plan that a separate engineer/agent can execute without further clarification. If decomposition is warranted, create sub-issues (slices) with full work details; otherwise document plan as a comment within the parent issue.

> Output only the plan (no extraneous narrative). Ask clarifying questions ONLY once if blocking gaps exist.

## Inputs

Required:

- GitHub issue URL or number: {{ISSUE_NUMBER}}
  Optional:
- Additional links/refs: {{ADDITIONAL_LINKS_OR_PATHS}}
- Target date / milestone: {{TARGET_DATE_OR_MILESTONE}}
- Repository: {{OWNER}}/{{REPO}}

If a URL is provided, extract the issue number and repository. Validate pattern `#[0-9]+` for issue numbers.

---

## Mode Guard (must pass before planning)

Confirm:
- Issue exists in GitHub repository (fetch via GitHub MCP)
- User intends planning (not implementation)
- No completed plan already exists in issue comments → if exists, direct to `work-ticket` mode

---

## Pre-Planning Check: Clarifications Required

**CRITICAL GATE**: Before proceeding with planning, verify that issue clarifications have been addressed.

1. Fetch the GitHub issue using GitHub MCP `issue_read` method `get_comments`.
2. Search issue comments for a `## Clarifications` section (indicates `clarify-ticket` has been run).
3. **If clarifications section DOES NOT exist:**
   - **STOP planning**
   - Output the following message to the user:
     ```
     ⚠️  CLARIFICATIONS REQUIRED BEFORE PLANNING
     
     Issue #{{ISSUE_NUMBER}} does not have a clarifications session recorded.
     
     Before creating a plan, ambiguities and missing details must be resolved through the clarification process.
     
     **Action Required**: Run the clarify-ticket prompt first:
     - Use: `clarify-ticket` with issue {{ISSUE_NUMBER}}
     - This will identify gaps and record Q&A directly in the issue
     - Once clarifications are complete, return here to run `plan-ticket`
     
     **Why?** A thorough plan requires:
     - Clear acceptance criteria & success signals
     - Defined data model & entities
     - Performance & security constraints
     - Edge case & error handling scenarios
     - Non-functional requirements (scalability, observability, etc.)
     
     Skipping clarification increases downstream rework risk significantly.
     ```
   - **Do NOT proceed further**. Terminate this session.

4. **If clarifications section DOES exist:**
   - Proceed to Step 0 below.
   - Reference clarifications throughout planning to ensure all ambiguities have been addressed.

---

## Step 0: Issue Verification & Branch Creation

1. Use the GitHub MCP server to fetch the issue (`issue_read` with method `get`); do NOT ask the user to paste raw issue details unless the MCP server is unavailable. Confirm issue number and repository format.
2. Ensure clean workspace (`git status` empty) and sync main:
   - `git checkout main && git pull --ff-only`
3. Determine branch prefix from issue labels or type (bug→bugfix, feature/story→feature, improvement/chore→chore, spike/investigation→spike). If no labels, infer from issue title.
4. Create or reuse shared issue branch (for parent/epic tracking):
   - Use the GitHub MCP server to list branches (`list_branches`) and to create a branch (`create_branch`).
   - `git switch -c <prefix>/#{{ISSUE_NUMBER}}-short-kebab-summary` (truncate ≤ ~60 chars) OR
   - `git switch <prefix>/#{{ISSUE_NUMBER}}-short-kebab-summary` if exists.
5. Confirm: "Planning #{{ISSUE_NUMBER}} on branch <prefix>/#{{ISSUE_NUMBER}}-short-kebab-summary".
6. Future GitHub issue comments (e.g., decomposition decisions, plan updates) must use GitHub MCP actions (`add_issue_comment`, `issue_write`)—never manual text unless MCP is unavailable (then note fallback in assumptions).
   (Shared conventions: `.github/prompts/includes/branch-commit-guidance.md`)

---

## Step 1: Ingest Issue

Collect: title, description, acceptance criteria (AC), labels, assignees, linked issues, comments, project context.
Extract:

- Problem statement
- In-scope vs out-of-scope
- Functional requirements
- Non-functional (perf, security, compliance, availability)
- Dependencies (services, data, other issues)
- Rollout expectations / flagging
- Success metrics & observability hooks
  Identify ambiguities & contradictions (list succinctly). If critical gaps, batch clarifying questions once, then proceed.

---

## Step 1.1: Decomposition Assessment

Evaluate whether the issue should be decomposed into independent, vertically-sliced sub-issues.

**Split into sub-issues when one or more apply:**
- Multiple distinct functional capabilities that can ship independently
- Data migration separable from feature behavior
- Risk isolation needed (e.g., schema → feature flag → public exposure)
- Parallelizable work streams (contract design, repository layer, service orchestration, observability)
- Different rollback domains/kill-switch requirements
- >1 API surface change (read vs write paths)
- >5 discrete acceptance criteria spanning multiple architectural layers
- Cross-cutting concerns requiring separate coordination

**Do NOT split when:**
- Changes are tightly coupled (artificial fragmentation adds overhead)
- Single functional capability
- Shared data model changes across all ACs
- Unified rollback strategy suffices
- <5 ACs or single architectural layer

**If decomposition is recommended:**

1. **Propose Work Breakdown Table** (for user review):

| Slice | Proposed Title | Type | Value/Rationale | Depends On | AC Mapping | Est. Effort | Primary Risks | Standalone Branch |
|-------|-----------------|------|-----------------|------------|-----------|-------------|---------------|-------------------|

2. **Map each original AC to exactly one slice** (no overlap/ambiguity). Include recommended branch naming for each slice.

3. **Await explicit user confirmation** before proceeding to sub-issue creation. Present decomposition with rationale:
   - Which slices provide value independently?
   - Which slices are prerequisites for others?
   - How do they enable parallel work?

4. **If user confirms decomposition:**

   a. **Create sub-issues** (one per slice):
      - Use GitHub MCP `issue_write` with method `create` for each sub-issue.
      - Title: `<Parent Title>: <Slice Action/Outcome>` (e.g., "User Auth: Database schema migration")
      - Description: Include:
        - **Slice context**: How this slice fits into parent work
        - **Acceptance criteria**: Numbered list unique to this slice
        - **Dependencies**: Link to prerequisite sub-issues (if any)
        - **Deliverable**: What constitutes "done" for this slice (testable, shippable unit)
        - **Notes**: Rollback strategy per slice, flag gating (if applicable), any constraints
      - Labels: Inherit parent labels + add `slice:<ordinal>` label (e.g., `slice:1`, `slice:2`)
      - Link to parent: Use GitHub MCP `sub_issue_write` method `add` to link each sub-issue to parent.

   b. **Create dedicated branches for each sub-issue**:
      - Use GitHub MCP `create_branch` for each slice.
      - Branch naming: `<prefix>/#{{SUB_ISSUE_NUMBER}}-slice-<slice-name>` (e.g., `feature/#42-slice-schema-migration`)
      - Rationale: Each slice can be developed, tested, and reviewed independently.

   c. **Establish dependency order** (if any):
      - Use GitHub MCP `sub_issue_write` with method `reprioritize` (if ordering matters) or add comments linking issues.
      - Document in parent issue comment: "Slice execution order: Slice #1 → Slice #2 → Slice #3"

   d. **Add a summary comment to parent issue** documenting the decomposition:
      - Use `add_issue_comment` to record: decomposition rationale, slice map, dependency graph, branch assignments.
      - Example: "Decomposed into 3 slices: #42 (schema), #43 (API), #44 (integration). Sequence: #42 → #43 → #44. Branches: feature/#42-slice-schema-migration, feature/#43-slice-api, feature/#44-slice-integration."

---

## Step 2: Repo & Doc Context Scan

Review: `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CHANGELOG.md`, `docs/**`, existing GitHub issue comments/plans for related issues.
Identify:

- Relevant modules/packages/classes
- Existing patterns for validation/logging/metrics/errors/retries/config/feature flags
- Similar implementations to reuse
- Existing feature flags; decide if new flag needed (`<domain>.<capability>.enabled`, default OFF)
- Architecture layering (controller → service → repo)
- API & schema governance (OpenAPI, migrations)
  Record only items materially affecting design.

---

## Step 3: Clarifications (Single Batch)

List only blocking items (privacy, auth roles, error contracts, SLA/SLO changes, data retention, rollout cadence, owner approvals). After responses (or assumptions), proceed.

---

## Step 4: Plan Construction

**If NO decomposition required:**
- Produce sections 1–10 (below) as a single issue comment on the parent issue.

**If decomposition required & slices created:**
- Produce a parent-level plan summary (Section 1, Section 2, decomposition map from Step 1.1) as a comment on parent issue.
- Produce full 10-section plans for EACH sub-issue as individual comments on each sub-issue (these are the detailed execution plans for engineers).
- Each sub-issue plan must be self-contained and independently executable.

Each implementation step must cite concrete file paths or new file placeholders. Prefer existing utilities over new ones. Default new runtime behavior behind a flag unless trivial & low risk.

---

## Required Output Sections (for Issue Comments)

### 1) Summary

- Issue: #{{ISSUE_NUMBER}} (or #{{SUB_ISSUE_NUMBER}} if sub-issue)
- One-liner: <what & why>
- Related milestone(s): <milestone names or n/a>
- Out of scope: <bullets>
- Slice context (if sub-issue): How this slice fits into parent work; prerequisite slices (if any)

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
- Work Breakdown & Dependencies (if parent-level plan): table + DAG narrative; link to sub-issues

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
- Per-slice effort roll-up if decomposed (parent issue only)

### 7) File-Level Change List

`path/to/File.php`: add logic X
(New) `path/to/NewFile.php`: purpose
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
- Per-slice rollout sequence (if decomposed; parent issue only)

### 10) Handoff & Next Steps

- Branch name: `<prefix>/#{{ISSUE_NUMBER}}-short-kebab-summary` (parent) or `<prefix>/#{{SUB_ISSUE_NUMBER}}-slice-<slice-name>` (sub-issue)
- Key commands (build/test/validate)
- Known gotchas / watchpoints
- Recommended reviewer(s)
- Link to parent issue (if sub-issue)
- Link to sub-issues (if parent with decomposition)

---

## Working Rules

(See `.github/prompts/includes/branch-commit-guidance.md` for branch & commit hygiene.)

- Do NOT implement production code here.
- Challenge ambiguities; make ≤2 explicit assumptions if still unresolved.
- Reuse existing patterns & utilities; avoid speculative abstractions.
- Signed commits (-S) with conventional format when committing code.
- New runtime behavior behind feature flag unless justified.
- Keep plan deterministic, minimal, test-driven, traceable.
- Dependency versions: If referencing an existing dependency, default to the version already declared in the project. For any new dependency (plugin, library, tool) required by the issue, use the Context7 MCP server to resolve and retrieve the latest stable release version at plan time; cite that version explicitly in the plan (pin it) and note the retrieval date. If Context7 unavailable, add an assumption and specify a placeholder `LATEST` tag to be resolved during implementation.
- Each sub-issue must be a **standalone, independently deliverable unit of work** in support of the overall feature. Engineers should be able to implement each slice without coordinating beyond the documented dependencies.
- Scope limit: Once the plan(s) are fully accepted (all sections complete, no open blocking questions) and posted as issue comment(s), this planning session terminates. Do not proceed to implementation steps here; direct any further work to the `work-ticket` prompt and clear transient context.

---

## Plan Publication (after constructing plan)

**Single-issue scenario (no decomposition):**
1. Use GitHub MCP to add the plan as an issue comment:
   - `add_issue_comment(owner, repo, issue_number, body)` where `body` is the complete 10-section plan in markdown.
2. Confirm: "Planning complete. Plan documented in issue comment. Branch: <prefix>/#{{ISSUE_NUMBER}}-short-kebab-summary"
3. Output next steps message:
   ```
   ✅ Plan #{{ISSUE_NUMBER}} is complete.
   
   **Next Step**: Review the plan for quality and completeness:
   
   Use: `analyze-plan` with issue #{{ISSUE_NUMBER}}
   
   This will:
   - Validate all plan sections are present and complete
   - Check test coverage against acceptance criteria
   - Identify ambiguities or missing details
   - Ensure implementation steps are feasible and sequenced correctly
   - Verify risks have mitigation strategies
   
   Once analysis is complete and any suggested refinements are approved:
   - Proceed to: `work-ticket` with issue #{{ISSUE_NUMBER}}
   ```

**Decomposed scenario (multiple sub-issues):**
1. Create sub-issues (if user confirmed decomposition) via GitHub MCP `issue_write`.
2. Link sub-issues to parent via GitHub MCP `sub_issue_write` method `add`.
3. Create dedicated branch for each sub-issue via GitHub MCP `create_branch`.
4. Add parent-level summary comment to parent issue (Section 1, Section 2, decomposition map).
5. Add detailed 10-section plan comment to EACH sub-issue (Section 1–10 tailored to that slice).
6. Add orchestration comment to parent: "Decomposition complete. Sub-issues: #42, #43, #44 with branch assignments. Execution sequence: #42 → #43 → #44. All plans documented in respective issue comments."
7. Output next steps message:
   ```
   ✅ Plan #{{ISSUE_NUMBER}} (parent) and slices #{{SUB_ISSUE_NUMBERS}} are complete.
   
   **Next Steps**:
   
   1. Review parent issue plan:
      Use: `analyze-plan` with issue #{{ISSUE_NUMBER}}
   
   2. Review each slice plan:
      Use: `analyze-plan` with issue #{{SUB_ISSUE_NUMBER_1}}
      Use: `analyze-plan` with issue #{{SUB_ISSUE_NUMBER_2}}
      (etc. for each slice)
   
   Analysis will validate each plan for completeness, test coverage, and feasibility.
   
   Once all analyses are complete and any suggested refinements are approved:
   - Proceed to implementation: `work-ticket` with issue #{{SLICE_ISSUE_NUMBER}}
   ```

---

## Sanity Checklist (mentally tick)

- ACs testable & mapped
- Each step has concrete file path(s)
- Risks have mitigation + fallback
- Observability & security addressed
- Feature flag(s) named & default OFF (or justification)
- Decomposition decision justified (if split); each slice is independently deliverable
- Each slice has dedicated branch assigned
- Each sub-issue has full plan comment (if decomposed)
- Plan(s) clearly formatted for issue comment (markdown readable)
- Slice dependencies documented and sequenced

## Output Instruction

Construct sections 1–10 formatted as markdown suitable for GitHub issue comment(s). 

**If no decomposition:** Output single 10-section plan for parent issue.

**If decomposition:** 
- Output parent-level summary (1–2 sections + decomposition map) as parent issue comment.
- Output full 10-section plan for each sub-issue as individual comments on respective sub-issues.

If blocking gaps remain after the one clarification batch, list them in Section 2 and proceed with explicit assumptions. After construction, publish via GitHub MCP (`add_issue_comment` and/or `issue_write` for sub-issues).
