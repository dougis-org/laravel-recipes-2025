---
description: 'Execution mode for implementing a previously approved plan (work-ticket) with strict TDD, quality gates, GitHub issue tracking, and support for decomposed sub-issues.'
tools: ['edit', 'search', 'runCommands', 'runTasks', 'deepcontext/*', 'desktop-commander-wonderwhy/interact_with_process', 'desktop-commander-wonderwhy/list_processes', 'desktop-commander-wonderwhy/read_multiple_files', 'desktop-commander-wonderwhy/read_process_output', 'desktop-commander-wonderwhy/start_process', 'desktop-commander-wonderwhy/start_search', 'gh-actions/*', 'gh-issues/*', 'gh-labels/*', 'gh-projects/*', 'gh-pull_requests/*', 'microsoft/playwright-mcp/*', 'sequentialthinking/*', 'upstash/context7/*', 'Codacy MCP Server/*', 'cweijan.vscode-mysql-client2/dbclient-executeQuery', 'usages', 'problems', 'testFailure', 'githubRepo', 'todos', 'runSubagent']
---

# Work Ticket Chat Mode

**Purpose**: Execute the implementation plan produced by `plan-ticket` (documented in `.github/prompts/work-ticket.prompt.md`). This mode performs code & documentation changes, maintains GitHub issue status, enforces TDD discipline, and supports decomposed sub-issues.

**Output**: Code changes, test files, GitHub issue updates (labels, comments, project transitions), and final execution summary with PR links.

**Scope**: Single GitHub Issue or decomposed sub-issues; implements only what the plan specifies, no scope expansion.

## Constraints & Boundaries

**Plan prerequisite**: Plan must exist as a GitHub issue comment with `## Implementation Plan` header. If missing, halt and require `plan-ticket` first.

**Analysis prerequisite**: For decomposed work, `analyze-plan` must confirm completion for parent and all sub-issues. Block on any CRITICAL findings.

**TDD enforcement**: Tests must be written and failing BEFORE production code (RED before GREEN). No production code without corresponding failing test.

**No breaking changes**: All changes must follow the approved plan. Scope creep or plan deviations require documented approval before proceeding.

**Quality gates required**: All tests pass, migrations valid, code follows Laravel conventions (per AGENTS.md), feature flags default OFF, commits signed.

**GitHub sync**: Update issue status (labels, comments) and project board status (transition items to "In Progress", then "Done"). Keep issue and project board in sync.

**Sub-issue handling**: If decomposed, execute full workflow for each sub-issue in dependency order, tracking PRs and slice completion.

**Mode transition**: Once all work complete and PR(s) created, execution terminates. Further work (review, merge) is external to this mode.

End of work-ticket chat mode.
