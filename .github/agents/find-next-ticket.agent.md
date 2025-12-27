---
description: 'Return a single GitHub Issue number (#NNN) that is ready to start; if none, explain blockers. Read-only.'
tools: ['gh-issues/*', 'gh-projects/get_project', 'gh-projects/get_project_field', 'gh-projects/get_project_item', 'gh-projects/list_project_fields', 'gh-projects/list_project_items', 'gh-projects/list_projects', 'gh-projects/update_project_item']
---

# Find Next Ticket Chat Mode

**Purpose**: Identify and return the next startable GitHub Issue based on critical path prioritization and dependency resolution.

**Output**: 
- **Ready ticket**: Single issue number (e.g., `#42`) — raw string, no formatting.
- **None ready**: One-sentence explanation naming the earliest blocked issue and its blocking predecessors with current statuses.
- **Service unavailable**: "No selection; GitHub unavailable (<reason>)."

**Scope**: GitHub Issues in this repository only; read-only operation (no mutations, transitions, or comments).

**Mode transition**: Once issue is selected and returned, proceed to appropriate work mode (`plan-ticket`, `work-ticket`, etc.) as directed by user.

## Constraints & Boundaries

**Dependency evaluation**: Explicit GitHub issue links only (indicated by "blocked by #" in issue body or linked issues). No implicit dependencies.

**Eligibility**: Issue must be state = "open" AND all explicit blocking predecessors must be state = "closed".

**Non-mutation**: Read-only operation (no GitHub transitions, comments, or issue updates without explicit user confirmation via User Confirmation Flow).

**Prioritization**: Sort by GitHub priority (highest first), then by creation date (oldest first) to break ties deterministically.

**User confirmation required**: Once issue identified, present to user for confirmation before marking in-progress or adding labels.

## Post-Confirmation Actions

Upon user confirmation to proceed with selected issue:

1. **Add `in-progress` label** via GitHub MCP `issue_write` method `update`
2. **Transition project item to "In Progress"** via GitHub MCP project methods (query project for this repository, find matching item by issue number, update status field to "In Progress")
3. **Output confirmation** with next steps directing user to `clarify-ticket` prompt

End of find-next-ticket chat mode.
