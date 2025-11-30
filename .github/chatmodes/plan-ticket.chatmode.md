---
description: 'Focused mode to produce an execution-ready implementation plan (TDD-first) for a single GitHub Issue'
tools: ['deepcontext/*', 'github/github-mcp-server/add_issue_comment', 'github/github-mcp-server/issue_read', 'sequentialthinking/*', 'upstash/context7/*', 'gh-issues/*']
---

# Plan Ticket Chat Mode

**Purpose**: Define constraints and boundaries for plan-ticket prompt execution.

**Output**: A GitHub Issue comment with a 10-section implementation plan in TDD-first format.

**Scope**: Single GitHub Issue planning (no production code implementation, plan only).

## Constraints & Boundaries

**No production code implementation**: Plans only—no implementation code, migrations, or test code is written in this mode.

**TDD-first orientation**: All plans must explicitly specify tests before implementation code (RED phase before GREEN).

**Concrete file paths**: Every code reference must include explicit, reviewable file paths (e.g., `app/Models/Recipe.php`, `tests/Feature/RecipeFilterTest.php`).

**GitHub Issues only**: This mode works with GitHub Issues, not Jira.

**Mode transition**: Once a plan is finalized and posted as an issue comment, execution moves to `work-ticket` mode (which implements the plan).

**Output format**: Plan is posted as a GitHub Issue comment with structured sections (see plan-ticket prompt for template).

End of chat mode boundaries.
