---
description: Find the next GitHub issue to work on (read-only)
---

# Find Next Ticket Command

## Mode Requirements
Before executing this command, set the `find-next-ticket` chat mode which is defined in `.github/chatmodes/find-next-ticket.chatmode.md`.

## Instructions
Follow the detailed instructions in `.github/prompts/find-next-ticket.prompt.md`.

## Guidelines from Chat Mode
- Tool allowlist: GitHub MCP tools for read-only operations
- Priority ordering: Critical path first, then parallel track
- Output contract: Return ONLY the issue number or blocker explanation
- No side effects: Read-only operation (no issue mutations, transitions, or comments)
- User confirmation flow required before marking issue as in-progress

## Execution Steps
1. Verify `find-next-ticket` chat mode is active
2. Fetch all open issues from repository
3. Apply dependency and eligibility rules
4. Return single next startable issue number OR blocker explanation
5. If issue found, present to user for confirmation
6. Upon user confirmation: mark as in-progress and suggest running `/clarify-ticket`
