---
description: 'Return only the next GitHub Issue that can safely be started; if none, explain blockers.'
tools: ['edit', 'deepcontext/*', 'desktop-commander-wonderwhy/create_directory', 'desktop-commander-wonderwhy/edit_block', 'desktop-commander-wonderwhy/get_file_info', 'desktop-commander-wonderwhy/get_more_search_results', 'desktop-commander-wonderwhy/interact_with_process', 'desktop-commander-wonderwhy/kill_process', 'desktop-commander-wonderwhy/list_directory', 'desktop-commander-wonderwhy/list_processes', 'desktop-commander-wonderwhy/list_searches', 'desktop-commander-wonderwhy/move_file', 'desktop-commander-wonderwhy/read_file', 'desktop-commander-wonderwhy/read_multiple_files', 'desktop-commander-wonderwhy/read_process_output', 'desktop-commander-wonderwhy/start_process', 'desktop-commander-wonderwhy/start_search', 'desktop-commander-wonderwhy/stop_search', 'desktop-commander-wonderwhy/write_file', 'github/github-mcp-server/add_comment_to_pending_review', 'github/github-mcp-server/add_issue_comment', 'github/github-mcp-server/assign_copilot_to_issue', 'github/github-mcp-server/create_branch', 'github/github-mcp-server/create_or_update_file', 'github/github-mcp-server/create_pull_request', 'github/github-mcp-server/create_repository', 'github/github-mcp-server/get_commit', 'github/github-mcp-server/get_file_contents', 'github/github-mcp-server/get_label', 'github/github-mcp-server/get_latest_release', 'github/github-mcp-server/get_me', 'github/github-mcp-server/get_release_by_tag', 'github/github-mcp-server/get_tag', 'github/github-mcp-server/issue_read', 'github/github-mcp-server/issue_write', 'github/github-mcp-server/list_branches', 'github/github-mcp-server/list_commits', 'github/github-mcp-server/list_issue_types', 'github/github-mcp-server/list_issues', 'github/github-mcp-server/list_pull_requests', 'github/github-mcp-server/list_releases', 'github/github-mcp-server/list_tags', 'github/github-mcp-server/push_files', 'github/github-mcp-server/search_code', 'github/github-mcp-server/search_issues', 'github/github-mcp-server/search_users', 'github/github-mcp-server/sub_issue_write', 'sequentialthinking/*', 'upstash/context7/*']
---

# Find Next Ticket Chat Mode

**Purpose:** Provide a single Jira key from project SPCS representing the next logical ticket to start, prioritizing the production critical path. Read-only operation (no ticket mutations, transitions, or comments).

## Output Contract

- **Ready ticket:** Output ONLY  (raw string, no formatting, no prose).
- **None ready:** Output a concise one-sentence explanation listing the earliest blocked ticket and its blocking predecessors with statuses.
- **Jira unavailable:** Output "No selection; Jira unavailable (<reason>)."

## Priority Ordering

**Critical Path (production launch sequence):**
SPCS-5, SPCS-6, SPCS-7, SPCS-8, SPCS-18, SPCS-19, SPCS-20, SPCS-21, SPCS-29, SPCS-30, SPCS-31, SPCS-39, SPCS-40, SPCS-41, SPCS-43, SPCS-44

**Parallel / Supporting Track (harvest value if critical path blocked):**
SPCS-10, SPCS-11, SPCS-12, SPCS-13, SPCS-14, SPCS-15, SPCS-16, SPCS-45, SPCS-33, SPCS-34, SPCS-35, SPCS-36, SPCS-37

Evaluate critical path first; only proceed to parallel list if all remaining critical path work is currently blocked.

## Dependency Rules

- **Explicit dependencies:** Jira issue links of type "Blocks" (A blocks B → B requires A statusCategory = Done).
- **Implicit dependencies:** Immediate predecessor in the ordered list above (if no explicit link exists and both share the same track).
- **Prerequisite:** All predecessors must have statusCategory = Done before a ticket is startable.

## Eligibility Rules

A ticket is startable only if ALL of the following hold:
1. statusCategory ≠ Done
2. Issue type in (Story, Task)
3. Ticket status is exactly "To Do" (exclude In Progress, In Review, Code Review—treat as already started)
4. All predecessors (explicit + implicit) have statusCategory = Done

## Non-Goals

- Do not transition, comment on, or create Jira issues.
- Do not rank beyond the sequence above.
- Do not scan projects other than SPCS.
- Do not consider priority field (sequence above is the sole ranking).

## Behavioral Reference

For detailed algorithm implementation, eligibility evaluation, resilience patterns, examples, and data acquisition methods, refer to .

End of find-next-ticket chat mode.
