# GitHub Issue Planning & Implementation Workflow

## Overview

This document describes the complete workflow for planning and implementing GitHub issues in the laravel-recipes-2025 project. The workflow consists of six distinct phases, each with its own prompt and chat mode.

**Key Principle**: All work is documented within GitHub issues themselves—no separate plan files in the repository. This keeps all context, discussions, and decisions in one discoverable location.

---

## Complete Workflow

### Phase 1: Find Next Ticket
**Prompt**: `.github/prompts/find-next-ticket.prompt.md`  
**Chat Mode**: `.github/chatmodes/find-next-ticket.chatmode.md`

**Purpose**: Identify the next startable GitHub issue respecting priority and blocking relationships.

**Process**:
1. Fetch all open issues from the repository
2. Build dependency map from issue links (blocking relationships)
3. Identify startable issues (open state, all predecessors closed)
4. Sort by priority (highest first), then creation date (oldest first)
5. Present the issue to the user for confirmation
6. Upon user confirmation:
   - Mark issue as `in-progress` (add label)
   - Add a comment: "Issue marked as in-progress. Starting work on this issue."
7. Remind user to run `clarify-ticket` next

**Output**: Issue confirmed and marked as in-progress. User reminded to run clarify-ticket.

**Next Step**: Run `clarify-ticket` with the issue number

---

### Phase 2: Clarify Ticket
**Prompt**: `.github/prompts/clarify-ticket.prompt.md`

**Purpose**: Identify underspecified areas in the GitHub issue and reduce ambiguity before planning.

**Key Features**:
- Performs structured ambiguity scan using 10 taxonomy categories:
  - Functional Scope & Behavior
  - Domain & Data Model
  - Interaction & UX Flow
  - Non-Functional Quality Attributes
  - Integration & External Dependencies
  - Edge Cases & Failure Handling
  - Constraints & Tradeoffs
  - Terminology & Consistency
  - Completion Signals
  - Misc / Placeholders

**Process**:
1. Fetch the GitHub issue and its comments
2. Scan for ambiguities and missing details
3. Generate up to 5 targeted clarification questions
4. Ask one question at a time (interactive)
5. After each answer:
   - Add bullet point to clarifications comment: `- Q: <question> → A: <answer>`
   - Update issue description with refined details where applicable
6. Validate all updates to ensure no contradictions

**Output**: Clarifications comment on issue with Q&A session. Updated issue description if needed.

**When Done**: All critical ambiguities resolved OR 5 questions asked

**Next Step**: Run `plan-ticket` with the issue number

---

### Phase 3: Plan Ticket
**Prompt**: `.github/prompts/plan-ticket.prompt.md`  
**Chat Mode**: `.github/chatmodes/plan-ticket.chatmode.md`

**Purpose**: Create a comprehensive, TDD-first implementation plan for the issue.

**Key Features**:
- **Pre-Planning Gate**: Verifies that `clarify-ticket` has been run first
  - Searches for `## Clarifications` section in issue comments
  - If missing: stops and prompts user to run clarify-ticket first
  
- **Scope Decomposition**:
  - Evaluates whether issue should be split into sub-issues (slices)
  - Uses heuristics: >5 ACs, cross-layer changes, parallelizable work, etc.
  - If decomposition recommended: proposes Work Breakdown Table for user confirmation
  - If user confirms: creates sub-issues with full issue numbers and branch assignments

- **Plan Structure** (10 sections):
  1. Summary (issue number, one-liner, milestones, out-of-scope)
  2. Assumptions & Open Questions
  3. Acceptance Criteria (normalized & testable)
  4. Approach & Design Brief (current state, proposed changes, data model, APIs, flags, config, deps, backward compat, observability, security, alternatives)
  5. Step-by-Step Implementation Plan (TDD: RED tests, GREEN implementation, Refactor, docs)
  6. Effort, Risks, Mitigations
  7. File-Level Change List
  8. Test Plan (happy paths, edge cases, regression, contract, security)
  9. Rollout & Monitoring Plan (flags, deployment, dashboards, alerts, rollback)
  10. Handoff & Next Steps (branch name, commands, gotchas, reviewers)

**Plan Documentation**:
- **Single-issue**: Plan published as comment on parent issue
- **Decomposed**: 
  - Parent issue gets summary comment with decomposition map
  - Each sub-issue gets full 10-section plan as its own comment
  - Each sub-issue is independently deliverable

**Publication**:
1. All plans posted as GitHub issue comments
2. Branches created/assigned for each issue/slice
3. Clear next-steps message output

**Output**: Issue with plan comment(s). Sub-issues created if decomposed. All with branch assignments.

**Next Step**: Run `analyze-plan` with the issue number

---

### Phase 4: Analyze Plan
**Prompt**: `.github/prompts/analyze-plan.prompt.md`

**Purpose**: Review plan quality and completeness before implementation begins. Required gate between planning and work.

**Analysis Scope** (8 detection passes):
1. **Completeness Check**: All 10 sections present? AC aligned with issue? Clarifications exist?
2. **Ambiguity Detection**: Vague adjectives? Unresolved placeholders? Missing flag defaults?
3. **Test Coverage Analysis**: Happy paths? Edge cases? AC-to-test mapping?
4. **Implementation Feasibility**: Concrete file paths? TDD order? Logical sequencing?
5. **Risk Mitigation Alignment**: Risk-to-mitigation mapping? Rollback procedures?
6. **Consistency & Traceability**: Terminology drift? Data model consistency? Test-to-AC mapping?
7. **Non-Functional Requirements**: Performance targets? Security checks? Observability instrumentation?
8. **Decomposition Validation** (if applicable): Sub-issues exist? Slices independently deliverable? Dependencies sequenced?

**Severity Assignment**:
- **CRITICAL**: Missing AC, no test plan, unclear order, unresolved placeholders in code paths, missing section
- **HIGH**: Ambiguous risk/mitigation, feature flag without defaults, vague performance target, test-to-AC misalignment, missing paths
- **MEDIUM**: Terminology drift, incomplete decomposition, unclear edge cases, non-functional without verification
- **LOW**: Wording improvements, style consistency, documentation suggestions

**Report Includes**:
- Executive summary (status, issue counts, readiness)
- Findings table (ID, category, severity, section, summary, recommendation)
- Coverage summary (AC count, implementation steps, tests, risks, file changes, slices)
- Test-to-AC traceability percentage
- Non-functional requirements validation
- Decomposition status (if applicable)

**Refinement Workflow**:
1. User reviews findings
2. For HIGH/MEDIUM issues: User can approve concrete edits
3. If approved: updates applied to plan comment in issue
4. User can re-run `analyze-plan` to confirm resolution

**Output**: Structured analysis report. Optional refinement suggestions (with user approval).

**Readiness States**:
- **Ready to implement**: No CRITICAL issues, all sections complete, test plan clear, AC traceable
- **Needs refinement**: CRITICAL or HIGH issues; user must approve edits before proceeding
- **Blocked**: Multiple CRITICAL issues; recommend re-running clarify-ticket or plan-ticket

**Next Step**: 
- If CRITICAL issues: resolve and re-run analyze-plan
- If ready: proceed to work-ticket
- If refinements needed: approve edits and re-run analyze-plan

---

### Phase 5: Work Ticket (In Progress)
**Prompt**: `.github/prompts/work-ticket.prompt.md`  
**Chat Mode**: `.github/chatmodes/work-ticket.chatmode.md`

**Purpose**: Execute the implementation plan with TDD and quality gates.

**Pre-Work Gate**: Verifies that plan analysis has been completed
- Searches for plan analysis comment in issue
- Checks for CRITICAL issues in analysis
- If missing or CRITICAL issues: stops and directs user to run/resolve analyze-plan first

**Phase 0**: Setup & Plan Review
- Fetch issue and plan comment
- Parse and summarize (Sections 1, 3, 5, 7)
- Confirm with user before beginning
- Prepare workspace (git status, switch to branch, pull latest)

**Phase 1**: Test-Driven Development (RED)
- Unit tests (nominal, boundary, error)
- Integration tests (containers/mocks)
- Contract/API tests
- Regression tests
- Ensure new tests FAIL

**Phase 2**: Implement (GREEN)
- Domain / DTOs
- Service interfaces + impls
- Data layer (repos, indexes)
- Controllers / API
- Config / env vars
- Migrations (backward compatible)
- Feature flag wiring (default OFF)
- Iterate until tests pass
- Refactor (no behavior change)

**Phase 3**: Docs & Artifacts
- Update README / module docs
- Update CHANGELOG
- Update runbooks / dashboards / alerts
- Schema validation (if needed)

**Phase 4**: Quality Gates
- Build & Unit tests pass
- Integration tests pass
- Contract/API tests pass
- Lint/Style passes

**Phase 5**: Submission & Review
- Commit with signed commits
- Push to branch
- Create/update PR
- Link to issue
- Request review

**Next Step**: PR review and merge

---

## Branch Naming Conventions

All branches follow this pattern:

```
<prefix>/#{{ISSUE_NUMBER}}-short-kebab-summary
```

**Prefixes** (determined by issue label/type):
- `feature/` - Features and stories
- `bugfix/` - Bug fixes
- `chore/` - Chores and maintenance
- `spike/` - Spikes and investigations

**Examples**:
- `feature/#42-add-user-auth`
- `bugfix/#15-fix-recipe-parsing`
- `chore/#8-update-dependencies`

**For Slices** (decomposed issues):
```
<prefix>/#{{SUB_ISSUE_NUMBER}}-slice-<slice-name>
```

**Examples**:
- `feature/#42-slice-schema-migration`
- `feature/#43-slice-api-endpoints`
- `feature/#44-slice-integration-tests`

---

## Issue Labels

Standard labels used throughout the workflow:

- `in-progress` - Added during find-next-ticket when user confirms
- `slice:1`, `slice:2`, etc. - Added to sub-issues for ordering
- Priority labels (from GitHub): `P0`, `P1`, `P2`, etc.
- Type labels: `feature`, `bug`, `chore`, `spike`

---

## GitHub Issue Comments Structure

Each issue can have multiple comments, organized as follows:

1. **Original Issue Description**: Title, description, acceptance criteria
2. **Clarifications Comment**: `## Clarifications – Session YYYY-MM-DD` with Q&A bullets
3. **Plan Comment(s)**:
   - Single-issue: Full 10-section plan in one comment
   - Decomposed:
     - Parent issue: Summary + decomposition map comment
     - Each sub-issue: Full 10-section plan in its own comment
4. **Analysis Comment**: `## Plan Analysis Report – Issue #{{ISSUE_NUMBER}}`
5. **Work Progress Comments**: Status updates during implementation

---

## Summary: Complete Workflow Flow

```
find-next-ticket
    ↓ (confirm, mark in-progress)
clarify-ticket
    ↓ (resolve ambiguities)
plan-ticket
    ↓ (create full plan)
    ├─ (if decomposed: create sub-issues with plans)
    └─ (if single: create plan comment)
    ↓
analyze-plan
    ├─ (if CRITICAL issues: resolve, re-run analyze-plan)
    ├─ (if HIGH/MEDIUM: approve refinements, re-run analyze-plan)
    └─ (if ready: proceed)
    ↓
work-ticket
    ↓ (Phase 0-5: RED → GREEN → Refactor → Docs → Quality → Submit)
    ↓
GitHub PR
    ↓
Code Review & Merge
```

---

## Key Principles

1. **All Work Documented in Issues**: No separate spec or plan files in the repository
2. **Sequential Gates**: Each phase depends on previous completion
3. **User Confirmation**: Major decisions (find-next, decomposition, plan refinement) require explicit user confirmation
4. **TDD First**: All implementation follows RED → GREEN → Refactor discipline
5. **Deterministic**: Workflow is reproducible and consistent
6. **Traceable**: Every decision, assumption, and change is recorded and linked

---

## Files Reference

### Prompts
- `.github/prompts/find-next-ticket.prompt.md` - Issue selection logic
- `.github/prompts/clarify-ticket.prompt.md` - Ambiguity identification and resolution
- `.github/prompts/plan-ticket.prompt.md` - Comprehensive plan creation (with decomposition)
- `.github/prompts/analyze-plan.prompt.md` - Plan quality review and validation
- `.github/prompts/work-ticket.prompt.md` - Implementation execution
- `.github/prompts/constitution.prompt.md` - Project principles (referenced by analysis)
- `.github/prompts/includes/branch-commit-guidance.md` - Git conventions

### Chat Modes
- `.github/chatmodes/find-next-ticket.chatmode.md` - Mode boundaries for issue selection
- `.github/chatmodes/plan-ticket.chatmode.md` - Mode boundaries for planning (guidelines only)
- `.github/chatmodes/work-ticket.chatmode.md` - Mode boundaries for implementation (in progress)

### Workflows
- `.github/workflows/auto-resolve-outdated-comments.yml` - Auto-resolve stale PR comments

---

## Next Steps

The workflow is now complete through the analyze-plan phase. The work-ticket prompt has been partially updated to include the pre-work gate for plan analysis. Further work on work-ticket can proceed when ready.
