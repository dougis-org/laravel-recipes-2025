---
description: 'Execution mode for implementing a previously approved plan (work-ticket) with strict TDD, quality gates, GitHub issue tracking, and support for decomposed sub-issues.'
tools: ['mcp-github/github_issue_read', 'mcp-github/github_issue_write', 'mcp-github/github_add_issue_comment', 'mcp-github/github_create_branch', 'mcp-github/github_list_branches', 'mcp-github/github_push_files', 'mcp-github/github_sub_issue_write', 'desktop-commander/create_directory', 'desktop-commander/edit_block', 'desktop-commander/get_file_info', 'desktop-commander/interact_with_process', 'desktop-commander/kill_process', 'desktop-commander/list_directory', 'desktop-commander/list_processes', 'desktop-commander/move_file', 'desktop-commander/read_file', 'desktop-commander/read_multiple_files', 'desktop-commander/start_process', 'desktop-commander/write_file']
---

# Work Ticket Chat Mode Specification

**Purpose**: Execute the implementation plan produced by `plan-ticket` (documented in `.github/prompts/work-ticket.prompt.md`). This mode performs code & documentation changes, maintains GitHub issue status, enforces TDD discipline, and supports full workflow iteration over decomposed sub-issues.

## Preconditions
- Plan must exist in GitHub issue as comment with `## Implementation Plan` header
- If plan missing: halt and instruct user to run plan-ticket first
- For decomposed issues: analyze-plan must confirm completion for parent and all sub-issues
- All CRITICAL findings from analyze-plan must be resolved before work begins

## High-Level Flow
1. Fetch GitHub issue; validate plan exists in issue comments
2. Check for analyze-plan completion via comment header
3. **Decomposition Detection**: Check if issue has sub-issues
   - If YES: Execute Sub-Issue Iteration Loop (full clarify→plan→analyze→work per sub-issue)
   - If NO: Execute Phase 0-7 implementation workflow
4. For single issue or each sub-issue in sequence:
   - Phase 0: Setup & Plan Review
   - Phase 1: Test-Driven Development (RED)
   - Phase 2: Implement (GREEN)
   - Phase 3: Docs & Artifacts
   - Phase 4: Quality Gates
   - Phase 5: Acceptance Verification
   - Phase 6: Commit & PR
   - Phase 7: Handoff Summary
5. Update GitHub issue with execution summary and link to PRs

## Pre-Work Gate
- Verify analyze-plan has completed (check for `## Analysis Results` comment header)
- If analyze-plan found CRITICAL issues: halt and require resolution before proceeding
- Load plan from `## Implementation Plan` comment
- Validate plan contains all 10 required sections (per plan-ticket.chatmode.md)
- Summarize plan back to user for confirmation before work begins

## Sub-Issue Iteration Loop (Decomposed Work)
If issue has sub-issues:
1. **Retrieve sub-issues** from GitHub issue
2. **For each sub-issue** (in dependency order):
   - Output iteration header: `## Sub-Issue Slice N: {{sub_issue_title}}`
   - Add `slice:N` label to sub-issue
   - **Prerequisite Checks**:
     - Check for clarifications (require clarify-ticket if missing)
     - Check for plan (require plan-ticket if missing)
     - Check for analysis (require analyze-plan if missing; block on CRITICAL)
   - Execute Phase 0 (Setup & Plan Review) for sub-issue
   - Execute Phases 1-7 (full implementation workflow)
   - Record completion with PR link in execution summary
3. After all sub-issues complete:
   - Verify all slice PRs are ready
   - Prepare merge order based on dependencies
   - Output final handoff summary combining all slices

## TDD Enforcement Policy
- **RED**: Create failing tests first; verify they fail for correct reason
- **GREEN**: Implement minimal code to pass tests
- **REFACTOR**: Clean up while keeping tests green
- **Blocking Rule**: Refuse to write production code if corresponding test not yet created
- **Test Coverage**: All acceptance criteria must map to test cases
- **Quality Gates**: Tests must pass, coverage must meet threshold (if defined), no regressions

## Phase Execution Model
### Phase 0: Setup & Plan Review
- Create/checkout working branch: `<prefix>/#{{ISSUE_NUMBER}}-short-kebab-summary`
- Display plan sections: Summary, AC, Approach, Implementation Steps
- Confirm plan accuracy and any necessary adjustments
- Document any deviations discovered during review

### Phase 1: Test-Driven Development (RED)
- Create test files per plan Test Plan section
- Write failing test cases for each acceptance criterion
- Verify tests fail for correct reasons
- Commit test scaffolding with message: `test(#{{ISSUE_NUMBER}}): add failing tests for [feature name]`

### Phase 2: Implement (GREEN)
- Implement code to make tests pass
- Follow Laravel conventions (per AGENTS.md)
- Use feature flags for new runtime behavior (default OFF)
- Implement documentation inline (PHPDoc, comments for complex logic)
- Commit implementation with message: `feat(#{{ISSUE_NUMBER}}): implement [feature name]`

### Phase 3: Docs & Artifacts
- Update README/CONTRIBUTING if needed
- Update CHANGELOG with entry
- Create/update migration files if database schema changed
- Add inline code documentation
- Commit with message: `docs(#{{ISSUE_NUMBER}}): update documentation for [feature name]`

### Phase 4: Quality Gates
- **All Tests Pass**: `php artisan test` (100% success, no warnings)
- **Schema Check**: Verify database migrations are correct
- **Linting**: Run style checks (if configured)
- **Security**: Check for secrets, unsafe patterns
- **Coverage**: Verify test coverage meets threshold
- Remediate any failures; do not proceed until all gates pass

### Phase 5: Acceptance Verification
- Map each acceptance criterion to corresponding test(s)
- Run spot checks: manually verify critical user-facing features
- Document verification results
- Confirm no scope creep introduced

### Phase 6: Commit & PR
- Consolidate related commits into logical change sets (conventional format)
- Sign all commits with: `git commit -S`
- Create PR with:
  - Title: `[#ISSUE_NUMBER] feature/bugfix summary`
  - Body: Plan sections (Summary, AC, Approach, Tests, Rollout)
  - Link to issue: `Closes #ISSUE_NUMBER`
  - Reference analyze-plan results
- Request review

### Phase 7: Handoff Summary
- Output execution summary:
  - Changes made (file count, line changes)
  - Tests created (count, coverage impact)
  - Risks realized and mitigations applied
  - Deviations from plan (with rationale)
  - PRs created with merge status
  - Next steps (review, merge, deployment)

## GitHub Issue Interaction Rules
- **issue_read**: Always first to ensure context currency and check for comments
- **issue_write**: Only for status transitions (e.g., add label `in-progress`, remove on completion)
- **add_issue_comment**: For execution progress, analysis results, and completion summary
- **create_branch**: Create working branch per issue (or sub-issue if decomposed)
- **sub_issue_write**: Link implementation PRs to parent issue; manage sub-issue status

## Plan Parsing & Validation
Required sections in plan comment:

1. Summary
2. Assumptions & Open Questions
3. Acceptance Criteria
4. Approach & Design Brief
5. Step-by-Step Implementation Plan
6. Effort, Risks, and Mitigations
7. File-Level Change List
8. Test Plan
9. Rollout & Monitoring Plan
10. Handoff Package

If any are missing: abort and request plan correction via issue comment.

## Execution Tracking
Maintain live tracking:
- **steps_completed**: Ordered list of completed implementation steps
- **tests_added**: File paths and test method names
- **files_modified**: Path → change summary
- **risks_realized**: Description and mitigation status
- **deviations**: Original step → adjustment rationale and approval

Document in final issue comment or sub-issue tracking comment.

## Error Handling & Recovery
**Error Scenarios**:
1. Test suite fails → Review test, fix implementation, re-run
2. Plan section invalid → Document deviation, propose correction, proceed with approval
3. Quality gate fails (lint/coverage) → Fix issue, re-run gate, confirm pass
4. File path changed → Discover new path, document deviation, update plan
5. Dependency unavailable → Resolve via dependency management, re-run gates
6. Sub-issue prerequisite missing → Halt, require clarify/plan/analyze for sub-issue
7. Schema conflict → Review migration, resolve conflicts, re-run schema check
8. Test flakiness → Isolate test, fix root cause, verify stable pass

**Recovery**: For each error, retry once; if persists, escalate as risk with mitigation and mark for follow-up.

## Commit Message Format
```
<type>(#ISSUE_NUMBER): <subject>

<body>

Signed-off-by: Name <email@example.com>
```

**Types**: `feat`, `fix`, `test`, `docs`, `chore`, `refactor`

## Quality Assurance Checklist
Before PR creation, verify:
- ✅ All tests pass (`php artisan test`)
- ✅ Test coverage meets threshold (if defined)
- ✅ No new TODOs without issue references
- ✅ Code follows Laravel conventions (per AGENTS.md)
- ✅ Documentation complete (README, CHANGELOG, inline)
- ✅ Feature flags implemented for new runtime behavior
- ✅ Security review completed
- ✅ Database migrations valid (if applicable)
- ✅ Acceptance criteria all satisfied (per spot checks)
- ✅ Deviations documented with rationale
- ✅ Rollback procedure defined (if needed)
- ✅ Commits are signed (-S flag)
- ✅ PR body complete with context
- ✅ Sub-issues tracked (if decomposed)
- ✅ Final summary generated

## Rollout & Monitoring
- Feature flags default to OFF
- Document kill-switch commands in PR and issue
- Verify observability (metrics, logs, traces) implemented or stubbed with ticket
- Define canary/progressive rollout steps if complex

## Completion Criteria
Execution ends when:
- All acceptance criteria satisfied and tested
- All quality gates passing
- All commits signed and pushed
- PR created with full context
- Issue updated with execution summary
- For decomposed work: all sub-issues merged or in review
- Handoff summary provided

## Example Start Acknowledgment
"Executing GitHub Issue #123. Plan loaded (10 sections, 4 acceptance criteria). Decomposition detected (2 sub-issues). Beginning Pre-Work Gate validation... Confirming analyze-plan completion and launching Sub-Issue Iteration Loop."

End of work-ticket chat mode specification.
