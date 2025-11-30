---
description: Determine the single next GitHub issue that can safely be started (critical-path first). Returns ONLY the issue number or, if none are startable, an explanation of blockers.
---

# find-next-ticket Prompt

Goal: Identify exactly one GitHub issue (number only) in laravel-recipes-2025 that is the next logical item to pick up, respecting issue priority and blocking relationships, with zero side effects (read-only). If no item is startable, output a concise blocker explanation instead of an issue number.

## Output Contract (STRICT)
- If a startable issue exists: Present the issue to user for confirmation before proceeding.
- If none are startable: output a short human explanation listing the earliest blocked task and its blocking predecessors (numbers + statuses). Do NOT fabricate issue numbers.
- Upon user confirmation: Mark issue as in-progress and remind user to run clarify-ticket next.
- Never modify GitHub issues without explicit confirmation flow (see User Confirmation section below).

## Read-Only Data Acquisition
Use GitHub MCP search (GraphQL or REST API) queries ONLY. Never assume statuses—always fetch.

Fetch all open issues in laravel-recipes-2025:
  repo:dougis-org/laravel-recipes-2025 is:open type:issue

Fetch individual issue details (fields): number, state, title, priority, labels, body (for linked issues), created, updated.

## Dependency Derivation
Treat GitHub issue links (via issue body mentions or linked issues) of type "blocks" as authoritative:
- If A "blocks" B (indicated by "blocked by #A" in issue body or GitHub linked issues), then B requires A state = closed before starting.
These explicit blocking relationships define the work sequencing — no implicit dependencies are assumed.

## Status Rules
A predecessor is considered satisfied ONLY if state == "closed". (Do NOT treat "in progress" or other states as done.) Conservative rule prevents premature parallel starts.
Eligible (startable) candidate criteria (updated):
- Issue state exactly "open" (ignore any custom labels indicating in-progress state — they are considered in flight and not startable)
- All explicit + implicit predecessors satisfied (state = closed)
- Issue should be tracked as a feature or task (not blocked by labels)

Removed previous fallback of returning earliest in-progress item; now only pure open items are emitted.

## Selection Algorithm
1. Fetch all open issues in the repository.
2. For each open issue, collect its predecessor set:
   - Explicit blocking relationships (indicated by "blocked by #" pattern in issue body or GitHub linked issues) → add those issue numbers.
3. Filter to only issues with all predecessors satisfied (state = closed or no predecessors).
4. Among ready candidates, sort by GitHub priority (highest first), then by issue creation date (oldest first).
5. Return the first (highest priority) startable issue number.
6. If no startable issues exist:
   - Construct explanation:
     - Identify the highest-priority open issue that is blocked.
     - List its blocking predecessors (numbers + their current states).
     - Output concise sentence (no markdown formatting).

## Tie-Breakers
Sort by GitHub priority (highest first), then by issue creation date (oldest first) to ensure deterministic ordering.

---

## User Confirmation Flow

When a startable issue is identified:

1. **Present the Issue to User**:
   - Fetch full issue details using GitHub MCP `issue_read` method `get`.
   - Display to user:
     ```
     Next startable issue:
     
     #{{ISSUE_NUMBER}}: {{ISSUE_TITLE}}
     
     {{ISSUE_DESCRIPTION_FIRST_100_CHARS}}...
     
     Priority: {{PRIORITY_LABEL}}
     Assignees: {{ASSIGNEES}}
     
     Ready to pick this up?
     ```
   - Await user confirmation (affirmative response: "yes", "ok", "proceed", "accept", "ready").

2. **If User Confirms** ("yes" / "ok" / "proceed" / "accept" / "ready"):
   - Use GitHub MCP `issue_write` method `update` to update the issue:
     - Set state to "open" (already open, but ensure no other changes)
     - Add label `in-progress` (if not already present)
   - Use GitHub MCP `add_issue_comment` to add a comment:
     ```
     Issue marked as in-progress. Starting work on this issue.
     ```
   - Output:
     ```
     ✅ Issue #{{ISSUE_NUMBER}} marked as in-progress.
     
     **Next Step**: Before planning, run the clarify-ticket prompt to ensure all details and edge cases are defined:
     
     Use: `clarify-ticket` with issue #{{ISSUE_NUMBER}}
     
     This will:
     - Identify any underspecified areas
     - Ask up to 5 targeted clarification questions
     - Record all Q&A in the issue itself
     
     Once clarifications are complete, proceed to: `plan-ticket` with issue #{{ISSUE_NUMBER}}
     ```

3. **If User Declines** or provides ambiguous response:
   - Ask: "Skip this issue and find the next one?"
   - If user confirms skip:
     - Re-run the selection algorithm, excluding the declined issue (treat as internally filtered).
     - Present the next startable issue.
   - If user cancels:
     - Output: "Issue selection cancelled. Run `find-next-ticket` again when ready."

---

## Validation & Safety
- Never transition or comment.
- Do not guess states; if a needed issue fetch fails, treat that predecessor as blocking and provide explanation.
- If GitHub API unavailable: output explanation: "No selection; GitHub API unavailable (reason)." (No number.)

## Examples
Scenario A: #5 closed; #6 open with no blocking issues → Return `6`.
Scenario B: #5 in progress; #6 open and blocked by #5 → Explain: "#6 blocked by #5 (in progress)".
Scenario C: #10 open with higher priority than #15, both with all predecessors satisfied → Return `10`.
Scenario D: All open issues each have at least one unresolved predecessor → Explain the highest-priority blocked issue and its blockers.

## Execution Steps (Implementation Guidance)
1. Fetch all open issues from the repository.
2. Build a dependency map from issue links (blockers per issue number).
3. Identify all startable issues (open state, all predecessors closed or none).
4. Sort by priority (highest first), then by creation date (oldest first).
5. Identify the first issue and present to user per User Confirmation Flow (above).
6. Upon user confirmation: mark issue as in-progress and remind user to run clarify-ticket.
7. If no startable issues exist: output explanation per Output Contract.
8. Emit output per contract.

## Final Output Enforcement
Before emitting: validate output string and flow.
- If issue was selected and user confirmed: output confirmation message with next steps (clarify-ticket).
- If issue was selected but user declined: recursively identify next issue and present again.
- If no startable issues exist: output explanation per blocker discovery.
- Never emit raw issue numbers anymore; always follow the User Confirmation Flow.
