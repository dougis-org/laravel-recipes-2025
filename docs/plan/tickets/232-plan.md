### 1) Summary

- Ticket: #232
- One-liner: Initialize repository for trunk-based delivery: add/update `.gitignore`, create initial commit artifacts, enforce main branch protection, and add `docs/development/git-workflow.md` and PR template to document branch & PR expectations.
- Related milestone(s): Milestone 1 - Project Setup
- Out of scope:
  - CI provider configuration beyond branch protection (e.g., full Actions workflow creation)
  - Repository license selection (assume existing project license)

---

### 2) Assumptions & Open Questions

- Assumptions:
  - Repo already contains the Laravel project files; no destructive history rewrite required.
  - GitHub is the hosting provider (issue exists in GitHub repo and branch protections are supported).
  - Defaults for `.gitignore` should follow Laravel community conventions referenced by `docs/plan/phase-1-project-setup.md` and `docs/plan/phase-10-asset-pipeline.md`.
  - Branch protection will require at minimum: require PR reviews, require status checks (left unset until CI is present), and disallow force pushes.
- Open questions (blocking -> need answers):
  1. Should branch protection enforce a specific set of required status checks now, or leave the checks list empty until CI workflows are in place? (Recommendation: configure review and push protections now; add status checks when CI exists.)

---

### 3) Acceptance Criteria (normalized)

1. Repository contains an appropriate Laravel `.gitignore` that excludes vendor, node_modules, build artifacts, environment files, and storage/logs as documented in `docs/plan/phase-1-project-setup.md`.
2. An initial commit exists containing project files and `.gitignore` and the commit history has at least one commit on `main`.
3. `main` branch protection is configured to prevent force-pushes, requires at least one approving review before merge, and disallows branch deletion.
4. `docs/development/git-workflow.md` exists and documents trunk-based delivery, branch naming, PR process, and basic merge expectations consistent with `docs/plan/README.md` and `docs/CONTRIBUTING.md`.
5. A PR template `.github/pull_request_template.md` exists describing required checklist items for PRs (e.g., tests, changelog, CI green, reviewers).

---

### 4) Approach & Design Brief

- Current state (key code paths):
  - Repo already contains project scaffolding and planning docs (`docs/plan/*`) referencing trunk-based delivery.
  - No PR template or explicit `docs/development/git-workflow.md` in repo as of search results.
- Proposed changes (high-level):
  - Add/update `.gitignore` with Laravel defaults.
  - Ensure repository has an initial commit and updated `main` with protection rules.
  - Add `docs/development/git-workflow.md` with sections: overview, branching strategy (trunk-based delivery), PR checklist, branch naming, hotfixes, release notes.
  - Add `.github/pull_request_template.md` with a standard checklist.
  - Configure GitHub branch protection rules on `main` (via GitHub UI or API) requiring approved PR reviews and disallowing force pushes and deletions.
- Data model / schema: None
- APIs & contracts: None
- Feature flags: Not applicable (configuration task only)
- Config (env vars): Not applicable
- External deps: GitHub API for branch protection configuration (no new code deps)
- Backward compatibility: Non-destructive; updates to `.gitignore` and docs only. Branch protection is additive.
- Observability: Create a simple audit note in the `docs/development/git-workflow.md` to record when protections were applied (date, actor).
- Security & privacy: Ensure `.gitignore` excludes `.env` and other secrets; recommend scanning repository for committed secrets (not in this ticket but noted).
- Alternatives considered:
  - Delay branch protection until CI status checks are present — chosen to apply minimal protection (reviews + no force push) now.

---

### 5) Step-by-Step Implementation Plan (TDD)

Phased steps (RED → GREEN → REFACTOR):

0. Preparation
   - Branch: `chore/232-initialize-git-repo` (created for planning)

1. Test additions first (intent: validate artifacts and docs exist). Files:
   - (Unit / Integration-esque smoke tests)
     - (New) `tests/Feature/GitSetupTest.php`: tests that `docs/development/git-workflow.md` and `.github/pull_request_template.md` exist in repository and `.gitignore` contains expected Laravel entries (this is a repository-level compliance test; will pass after changes).
     - Data providers: `tests/Fixtures/git_setup/expected_gitignore_entries.json` listing expected patterns.

2. Implementation (make tests pass):
   - Update or create `.gitignore` at repo root with Laravel defaults. Use contents referenced in `docs/plan/phase-1-project-setup.md`.
   - Create `docs/development/git-workflow.md` with sections: overview, branching strategy (trunk-based delivery), PR checklist, branch naming, hotfixes, release notes.
   - Create `.github/pull_request_template.md` with a checklist (tests, description, linked issue, reviewer(s), changelog entry if needed).
   - Ensure there is an initial commit on `main` (already present in repo or create one if missing). If missing, create initial commit and push to `main`.
   - Configure GitHub branch protection rules for `main` to require at least 1 approving review, disallow force pushes, and prevent deletion (use GitHub API or UI).

3. Refactor pass
   - Validate docs formatting, shorten sections into templates (include code blocks and examples), and update `CONTRIBUTING.md` to link to the new `docs/development/git-workflow.md`.

4. Pre-PR Duplication & Complexity Review (MANDATORY)
   - Confirm no duplicate git-workflow docs exist; consolidate `docs/plan/phase-1-project-setup.md` references to canonical file.
   - Run static quality checks on new docs (spelling, markdownlint) and tests (phpunit).
   - Codacy/linters: run analysis and resolve findings (docs won't usually have Codacy issues; tests need to pass).

5. Docs & artifact updates
   - Update `docs/plan/phase-1-project-setup.md` or add a link to `docs/development/git-workflow.md`.
   - Add a short note to CHANGELOG or `docs/BUILD_PLAN_UPDATE_SUMMARY.md` referencing ticket #232.

Notes on tests:
- Tests are repository-level smoke checks; these are quick, deterministic, and indicate successful completion of the task.

---

### 6) Effort, Risks, Mitigations

- Effort: Small (S) — modifications are limited to docs and configuration.
- Risks:
  1. Overly strict branch protection (e.g., requiring CI status checks that don't exist) could block contributors. Mitigation: only enable review and no-force-push protections now and add status checks when CI is available.
  2. Sensitive files accidentally committed before `.gitignore` updated. Mitigation: Scan repository history for secrets (recommend running a secret-scan tool after changes).
  3. Duplicate or conflicting documentation. Mitigation: Consolidate docs and link canonical file.

---

### 7) File-Level Change List

- `.gitignore`: update with Laravel defaults (modify existing or add new)
- (New) `docs/development/git-workflow.md`: document trunk-based delivery, branch naming, PR process, and audit note
- (New) `.github/pull_request_template.md`: PR checklist template
- (New) `tests/Feature/GitSetupTest.php`: repository-level smoke tests asserting presence & contents
- (Modify) `docs/CONTRIBUTING.md`: add link to `docs/development/git-workflow.md` (if not already linked)
- (Modify) `docs/BUILD_PLAN_UPDATE_SUMMARY.md`: add brief change note referencing #232 (if project changelog practice exists)

---

### 8) Test Plan

Parameterized Test Strategy
- Use JSON fixture `tests/Fixtures/git_setup/expected_gitignore_entries.json` with keys/regexes to validate `.gitignore` content (vendor/, node_modules/, .env, storage/, /public/build etc.).
- `tests/Feature/GitSetupTest.php` will iterate entries and assert file presence/regex match.

Test Coverage by Category:
- Happy paths: test confirms existence of files and matching `.gitignore` entries (parameterized source above).
- Edge/error cases: test that missing entries fail (intentional during RED stage).
- Regression: include CI job to run `php artisan test` after merge.
- Contract: Markdown lint or basic parsing to ensure docs render.
- Performance: Not applicable.
- Security/privacy: Validate `.env` is listed in `.gitignore` and add a note to run a secret scan.
- Manual QA checklist:
  - Open `docs/development/git-workflow.md`, verify content and links
  - Verify PR template appears in new PR UI
  - Verify branch protection settings on GitHub UI/API

---

### 9) Rollout & Monitoring Plan

- Flags: Not applicable (configuration only).
- Deployment steps:
  1. Merge PR into `main` (with at least one approval).
  2. Immediately apply or verify branch protection via GitHub UI/API to prevent regressions.
- Dashboards & key metrics: Not applicable; add audit note to docs to record who applied protections and when.
- Alerts: Not applicable.
- Success metrics / KPIs:
  - PR template present and used.
  - `docs/development/git-workflow.md` reviewed & accepted by maintainers.
  - Branch protection actively prevents force-push & requires reviewer approval.
- Rollback procedure:
  - To remove protection changes, revert branch protection via GitHub UI/API and push a follow-up commit to docs documenting the rollback.

---

### 10) Handoff Package

- Jira/GitHub link: https://github.com/dougis-org/laravel-recipes-2025/issues/232
- Branch & PR name: `chore/232-initialize-git-repo` (PR: `chore/232-initialize-git-repo` → `main`)
- Plan file path: `docs/plan/tickets/232-plan.md`
- Key commands:
  - Run tests: `php artisan test` or `vendor/bin/phpunit`
  - Lint markdown: `markdownlint .` (if available)
  - Apply branch protection via API: (documented steps in the PR description)
- Known gotchas:
  - Ensure not to enable required status checks until a CI provider with stable check names exists.

---

### 11) Traceability Map

| Criterion # | Requirement | Milestone | Task(s) | Flag(s) | Test(s) |
| --- | --- | --- | --- | --- | --- |
| 1 | REQ-232-IGNORE | M1 | Update `.gitignore` | n/a | `tests/Feature/GitSetupTest::test_gitignore_contains_expected_entries` |
| 2 | REQ-232-INITIAL-COMMIT | M1 | Ensure initial commit exists / verify history | n/a | `tests/Feature/GitSetupTest::test_initial_commit_exists` (manual verification) |
| 3 | REQ-232-BRANCH-PROTECTION | M1 | Configure `main` branch protection | n/a | Manual verification via GitHub UI/API |
| 4 | REQ-232-GIT-WORKFLOW-DOC | M1 | Add `docs/development/git-workflow.md` | n/a | `tests/Feature/GitSetupTest::test_workflow_doc_exists` |
| 5 | REQ-232-PR-TEMPLATE | M1 | Add `.github/pull_request_template.md` | n/a | `tests/Feature/GitSetupTest::test_pr_template_exists` |
