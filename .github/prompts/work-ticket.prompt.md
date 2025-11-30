---
description: Execute an approved implementation plan for a GitHub issue. Supports single issues and decomposed sub-issues with full workflow iteration.
---

**Goal:** Implement the plan produced by `plan-ticket` with TDD, quality gates, and branch hygiene. If the issue is decomposed into sub-issues, iterate through each sub-issue using the complete workflow (clarify → plan → analyze → work).

> This prompt assumes a plan comment already exists in the GitHub issue. If not, run `plan-ticket`. The plan must have passed `analyze-plan` review before work can begin.

## Inputs

Required:
- **GitHub issue number:** #{{ISSUE_NUMBER}} (or URL)
- **Repository:** {{OWNER}}/{{REPO}}
Optional:
- **Repo root:** current workspace

---

## Pre-Work Gate: Plan Analysis Required

**CRITICAL GATE**: Before proceeding with implementation, verify that the plan has been analyzed and approved.

1. Fetch the GitHub issue using GitHub MCP `issue_read` method `get_comments`.
2. Search issue comments for an `## Plan Analysis` comment or similar (indicates `analyze-plan` has been run).
3. **If analysis comment DOES NOT exist:**
   - **STOP implementation**
   - Output the following message:
     ```
     ⚠️  PLAN ANALYSIS REQUIRED BEFORE STARTING WORK
     
     Issue #{{ISSUE_NUMBER}} does not have a plan analysis review recorded.
     
     Before implementing, the plan must be validated for quality and completeness.
     
     **Action Required**: Run the analyze-plan prompt first:
     - Use: `analyze-plan` with issue {{ISSUE_NUMBER}}
     - This will validate the plan sections, test coverage, and feasibility
     - Any issues will be flagged for refinement
     
     Once analysis is complete and any recommended updates are made:
     - Return here to run `work-ticket`
     
     **Why?** Plan analysis catches:
     - Missing or ambiguous acceptance criteria
     - Incomplete test coverage
     - Infeasible implementation steps
     - Unresolved risks
     
     Skipping analysis increases bug risk and rework during implementation.
     ```
   - **Do NOT proceed further**. Terminate this session.

4. **If analysis comment DOES exist:**
   - Check for CRITICAL issues in the analysis. If any exist, direct user to address them:
     ```
     ⚠️  PLAN HAS CRITICAL ISSUES
     
     The plan analysis identified critical issues that must be resolved before work can begin:
     
     {{CRITICAL_ISSUES_SUMMARY}}
     
     Please address these in the plan comment, then re-run `analyze-plan` to confirm resolution.
     ```
   - If no CRITICAL issues: proceed to Phase 0 below.

---

## Mode Guard

Confirm:
- Issue exists in GitHub repository (fetch via GitHub MCP)
- User intends implementation (not planning)
- Plan comment exists and has passed analysis
- Issue is marked as `in-progress`

(See `.github/prompts/includes/branch-commit-guidance.md` for naming & commit rules.)

---

## Pre-Implementation Check: Decomposition Detection

**CRITICAL DECISION POINT**: Before proceeding to Phase 0, check if this issue is decomposed.

1. Fetch the plan comment from the issue.
2. Search plan for references to sub-issues (look for "Sub-issues:" or "Slice" references in Section 10 "Handoff & Next Steps").
3. **If sub-issues ARE mentioned in the plan:**
   - Extract the sub-issue numbers from the plan comment.
   - Use GitHub MCP `issue_read` to verify each sub-issue exists.
   - Output the following message:
     ```
     ℹ️  DECOMPOSED ISSUE DETECTED
     
     Issue #{{ISSUE_NUMBER}} is decomposed into {{COUNT}} slices:
     
     {{SUB_ISSUE_LIST}}
     
     **Workflow**:
     For each sub-issue, you will run the complete workflow:
     1. clarify-ticket → clarify-ticket with the sub-issue
     2. plan-ticket → plan-ticket with the sub-issue (if not already planned)
     3. analyze-plan → analyze-plan with the sub-issue (if not already analyzed)
     4. work-ticket → work-ticket with the sub-issue
     
     **Execution Order** (per plan dependencies):
     {{DEPENDENCY_ORDER}}
     
     Ready to start with sub-issue #{{FIRST_SUB_ISSUE}}?
     ```
   - Await user confirmation.
   - If user confirms: proceed to Sub-Issue Iteration Loop (see section below).
   - If user declines: terminate session.

4. **If sub-issues are NOT mentioned:**
   - This is a single-issue workflow.
   - Proceed to Phase 0 (Setup & Plan Review).

---

## Sub-Issue Iteration Loop

**Only executed if decomposition detected and user confirmed.**

For each sub-issue in dependency order:

1. **Output iteration header**:
   ```
   🔄 Starting work on sub-issue slice:
   
   #{{SUB_ISSUE_NUMBER}}: {{SUB_ISSUE_TITLE}}
   
   Slice: {{SLICE_NUMBER}} of {{TOTAL_SLICES}}
   Dependencies: {{LIST_PREDECESSORS}}
   ```

2. **Check sub-issue status**:
   - Fetch sub-issue using GitHub MCP `issue_read` method `get`.
   - Verify sub-issue has `in-progress` label (if not: add it).

3. **Run sub-issue clarification check**:
   - Search sub-issue comments for `## Clarifications` section.
   - If missing: output message to run `clarify-ticket` with sub-issue first.
   - If exists: proceed to planning check.

4. **Run sub-issue planning check**:
   - Search sub-issue comments for plan comment (section 1 header).
   - If missing: output message to run `plan-ticket` with sub-issue first.
   - If exists: proceed to analysis check.

5. **Run sub-issue analysis check**:
   - Search sub-issue comments for `## Plan Analysis` comment.
   - If missing: output message to run `analyze-plan` with sub-issue first.
   - If exists with CRITICAL issues: output message to resolve and re-run `analyze-plan`.
   - If analysis exists and no CRITICAL issues: proceed to Phase 0 for sub-issue work.

6. **Execute Phase 0 (Setup & Plan Review) for sub-issue**:
   - Fetch sub-issue plan comment.
   - Extract plan sections (1, 3, 5, 7).
   - Summarize for user confirmation.
   - Upon confirmation: prepare workspace for sub-issue branch.

7. **Execute Phases 1-8 (see below) for sub-issue**:
   - Run complete RED → GREEN → Refactor → Docs → Quality → Acceptance → Commit & PR workflow.
   - Upon completion: mark sub-issue as done.
   - Add comment to sub-issue: "Slice work completed. PR: {{PR_LINK}}"

8. **Move to next sub-issue**:
   - If more sub-issues remain in the dependency order: loop back to step 1.
   - If all sub-issues complete:
     ```
     ✅ All slices completed!
     
     Sub-issues:
     {{LIST_ALL_SUB_ISSUES_WITH_PR_LINKS}}
     
     Next steps:
     1. Parent issue is tracking overall coordination
     2. All slice PRs are ready for review
     3. Merge slices in dependency order
     ```
   - Terminate loop.

---

## Phase 0: Setup & Plan Review (Single-Issue or Per Sub-Issue)

0.1 Fetch GitHub issue via GitHub MCP `issue_read` method `get`:
   - Extract: issue number, repository (owner/repo), title, description, labels, branch assignment.
   - Validate issue exists and is marked `in-progress`.

0.2 Locate and parse the plan comment:
   - Search issue comments for the implementation plan (10 sections).
   - Extract Sections 1 (Summary), 3 (Acceptance Criteria), 5 (Implementation Plan), 7 (File-Level Change List).

0.3 Summarize for confirmation:
   ```
   Starting implementation of issue #{{ISSUE_NUMBER}}: {{TITLE}}
   
   Acceptance Criteria:
   {{AC_SUMMARY}}
   
   File changes:
   {{FILE_CHANGES_SUMMARY}}
   
   Branch: {{BRANCH_NAME}}
   
   Ready to begin?
   ```
   - Await user confirmation (affirmative response: "yes", "ok", "proceed", "ready").

0.4 Prepare workspace:
   - Ensure clean git status (`git status` shows no uncommitted changes).
   - Switch to the issue branch (already created during find-next-ticket or plan-ticket):
     `git switch <prefix>/#{{ISSUE_NUMBER}}-short-kebab-summary` (or slice branch for sub-issues)
   - Pull latest: `git pull --rebase origin main`
   - Create feature branch for work if needed (e.g., `<prefix>/#{{ISSUE_NUMBER}}-dev`)

---

## Phase 1: Test-Driven Development (RED)

Extract test plan from Section 8 of plan comment. Create tests following this order:

1.1 **Unit tests** (nominal + boundary + error paths)
   - File: `tests/Unit/{{Feature}}Test.php` (or appropriate test directory)
   - Ensure tests FAIL initially (RED)

1.2 **Integration tests** (with mocks/containers)
   - File: `tests/Feature/{{Feature}}Test.php` (or integration directory)
   - Include database interactions, service calls
   - Ensure tests FAIL initially

1.3 **Contract/API tests** (if applicable)
   - Validate OpenAPI spec compliance
   - Error codes and response formats
   - Ensure tests FAIL initially

1.4 **Regression tests** (from historical issues/ACs)
   - File: `tests/Regression/{{Feature}}Test.php`
   - Ensure tests FAIL initially

1.5 **Verify all new tests FAIL**:
   - Run: `php artisan test` (or project test command)
   - All new tests must fail (proves test validity)
   - Document test count: `{{UNIT_COUNT}}` unit, `{{INTEGRATION_COUNT}}` integration, `{{CONTRACT_COUNT}}` contract

---

## Phase 2: Implement (GREEN)

Follow implementation order from Section 5. For each step:

2.1 **Domain layer** (Data Transfer Objects, Models, Entities)
   - File: `app/Models/{{Entity}}.php` + relationships
   - Add fillable attributes, timestamps, casts as needed

2.2 **Service layer** (Business logic interfaces + implementations)
   - File: `app/Services/{{Feature}}Service.php`
   - Implement methods referenced in tests

2.3 **Data layer** (Repositories, queries, indexes)
   - File: `app/Repositories/{{Feature}}Repository.php` (if used)
   - Include query optimization, eager loading

2.4 **Controller/API layer** (HTTP handlers, validation)
   - File: `app/Http/Controllers/{{Feature}}Controller.php`
   - Add validation, authorization, error handling

2.5 **Configuration** (env vars, validation strategy)
   - File: `.env.example` + `config/` files
   - Add validation logic with sensible defaults

2.6 **Migrations** (backward-compatible schema changes)
   - File: `database/migrations/YYYY_MM_DD_HHMMSS_{{change}}.php`
   - Include rollback logic
   - Test `php artisan migrate` + `migrate:rollback`

2.7 **Feature flags** (runtime control, default OFF)
   - Wire flag checks from Section 4 into code
   - Confirm default is OFF (or justified in plan)
   - File: `config/features.php` (or appropriate feature flag config)

2.8 **Iterate tests to GREEN**:
   - Run: `php artisan test` repeatedly
   - Fix implementation until all tests pass
   - Document iterations

2.9 **Refactor pass** (no behavior change)
   - Extract common logic
   - Improve naming, reduce duplication
   - Simplify conditionals
   - Ensure tests still pass after refactor

---

## Phase 3: Docs & Artifacts

3.1 **Update README / module docs**
   - If new public API: document usage
   - If new feature: add configuration examples

3.2 **Update CHANGELOG**
   - File: `CHANGELOG.md`
   - Add entry describing the feature/fix

3.3 **Update runbooks / dashboards / alerts** (if applicable)
   - Document any new operational concerns
   - Add dashboard panels if needed
   - Configure alerts for new feature flags

3.4 **Schema/API artifact updates** (if schema changed)
   - Update OpenAPI spec: `docs/api/openapi.yaml`
   - Update type definitions
   - Validate schema drift: `php artisan schema:validate` (or project equivalent)

---

## Phase 4: Quality Gates

| Gate | Command / Action | Pass Criteria |
|------|------------------|---------------|
| Build & Unit | `php artisan test` | All tests green |
| Feature Flags | Review flag defaults | All new flags default OFF or justified |
| Code Style | Project linter (if configured) | No blocking issues |
| Type Safety | Static analysis (if configured) | No errors |
| Schema Drift | Check migrations are backward-compatible | No regressions |
| Security/Input | Review validation & authorization | No secrets, safe validation |
| Test Coverage | Compare to baseline (if tracked) | No unjustified drop |

Failures → fix root cause; never dilute or skip tests.

---

## Phase 5: Acceptance Verification

5.1 **Load acceptance criteria** from Section 3 of plan comment.

5.2 **Map each AC to tests**:
   - For each AC: list which test(s) verify it.
   - Document in comment: `AC mapping: AC#1 → unit test X, integration test Y`

5.3 **Execute negative & error path spot checks**:
   - Manually test edge cases not captured by automated tests
   - Verify error messages are user-friendly
   - Check rollback procedures work as documented

5.4 **Document any deviations**:
   - If an AC cannot be met as written: request plan update via comment
   - Never silently deviate; always justify or fix plan

---

## Phase 6: Commit & PR

6.1 **Stage changes**:
   - `git add .`

6.2 **Commit with conventional format** (sign commits):
   - `git commit -S -m "feat({{scope}}): #{{ISSUE_NUMBER}} {{concise summary}}"`
   - Use `fix`, `chore`, `refactor`, `docs`, `test` as appropriate
   - Reference issue number in commit message

6.3 **Push to branch**:
   - `git push -u origin <prefix>/#{{ISSUE_NUMBER}}-short-kebab-summary`

6.4 **Create or update PR**:
   - Title: `#{{ISSUE_NUMBER}}: {{PLAN_SUMMARY}}`
   - Description: Include plan section references, test summary, risk mitigation, rollout strategy
   - Link to GitHub issue: "Resolves #{{ISSUE_NUMBER}}"
   - Link to plan: "Plan: [comment link to plan comment]"

6.5 **Request reviewers**:
   - Use CODEOWNERS file to identify required reviewers
   - Request domain experts and maintainers

6.6 **Add PR comment to issue**:
   - Use GitHub MCP `add_issue_comment` to link PR: "PR opened: {{PR_LINK}}"

---

## Phase 7: Handoff Summary (Output)

Output a summary upon work completion:

```
✅ IMPLEMENTATION COMPLETE

Issue: #{{ISSUE_NUMBER}}: {{TITLE}}

Summary:
- Files changed: {{COUNT}} ({{KEY_FILES}})
- New tests: {{UNIT_COUNT}} unit, {{INTEGRATION_COUNT}} integration, {{CONTRACT_COUNT}} contract, {{REGRESSION_COUNT}} regression
- Feature flags: {{FLAG_LIST}} (all default OFF)
- All ACs verified: {{AC_VERIFICATION_SUMMARY}}

PR: {{PR_LINK}}
Branch: {{BRANCH_NAME}}

Next Steps:
1. PR review by {{REVIEWER_LIST}}
2. Address review feedback (or re-run work-ticket to iterate)
3. Merge to main
4. Deploy per rollout plan (Section 9): {{ROLLOUT_SUMMARY}}

Key Metrics:
- Test coverage change: {{COVERAGE_DELTA}}
- Risk mitigations applied: {{MITIGATION_COUNT}}
- Outstanding risks: {{RISK_SUMMARY}}
```

---

## Error Matrix & Recovery

| Issue | Action | Recovery |
|-------|--------|----------|
| Missing plan section | STOP; request fix | Re-run plan-ticket or analyze-plan |
| All tests pass in RED | Strengthen tests | Make tests more specific, rewrite RED tests |
| Build fail | Fix latest change or revert | Debug error, fix, retest |
| Test coverage drop | Justify or add tests | Add tests to restore coverage |
| Feature flag not OFF | Fix default | Update config/features.php or test |
| Sub-issue analysis has CRITICAL | STOP sub-issue work | Re-run analyze-plan with sub-issue, fix plan |
| Git merge conflict | Resolve | Use git tools, re-run tests after resolve |
| PR feedback | Iterate | Make changes, commit, push, wait for re-review |

After 2 failed remediation attempts on same issue, escalate to user with full context.

---

## Verification Checklist

- [ ] Plan analysis passed (no CRITICAL issues)
- [ ] Issue/sub-issue marked as `in-progress`
- [ ] All clarifications exist (if decomposed)
- [ ] All plans exist and analyzed (if decomposed)
- [ ] Workspace clean, branch prepared
- [ ] RED tests created and failing
- [ ] GREEN tests passing
- [ ] Refactor pass completed
- [ ] All ACs verified
- [ ] Docs & artifacts updated
- [ ] Quality gates all passing
- [ ] Conventional commits signed
- [ ] PR created with full context
- [ ] CODEOWNERS reviewers requested
- [ ] Issue linked to PR
- [ ] Handoff summary generated

---

## Success Criteria

- All RED tests pass in GREEN phase
- All acceptance criteria verified
- PR open with full context and linked to issue
- Reviewers assigned from CODEOWNERS
- Branch prepared per conventions
- No quality gate failures

---

## Working Rules

- **Strict TDD**: RED → GREEN → Refactor with no exceptions
- **No scope creep**: Stay within plan; request plan update if needed
- **Reuse patterns**: Cite reused modules and follow project conventions
- **Convention over config**: Follow CONTRIBUTING.md; override plan if needed
- **Test all new logic**: No production code without tests
- **Feature flags by default**: New behavior behind flag unless explicitly low-risk
- **Signed commits**: All commits must be cryptographically signed (`-S` flag)
- **Decomposed workflow**: For sub-issues, run full clarify → plan → analyze → work cycle per sub-issue

---

## References

- Shared guidance: `.github/prompts/includes/branch-commit-guidance.md`
- Plan schema (optional validation aid): `.github/prompts/includes/plan-file-structure.schema.json`
- Project conventions: `CONTRIBUTING.md` & `docs/design/`
