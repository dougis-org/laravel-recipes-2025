---
description: Determine the single next SPCS Jira ticket that can safely be started (critical-path first). Returns ONLY the ticket key or, if none are startable, an explanation of blockers.
---

# find-next-ticket Prompt

Goal: Identify exactly one Jira issue (key only) in project SPCS that is the next logical item to pick up, prioritizing the production critical path, with zero side effects (read-only). If no item is startable, output a concise blocker explanation instead of a key.

## Output Contract (STRICT)
- If a startable ticket exists: OUTPUT ONLY the ticket key (e.g., `SPCS-19`) and NOTHING else (no backticks, no prose).
- If none are startable: output a short human explanation listing the earliest blocked task and its blocking predecessors (keys + statuses). Do NOT fabricate keys.
- Never modify Jira issues, add comments, or transition statuses.

## Priority Model
1. Critical Path (must protect production launch date). Ordered list:
   SPCS-5, SPCS-6, SPCS-7, SPCS-8,
   SPCS-18, SPCS-19, SPCS-20, SPCS-21,
   SPCS-29, SPCS-30, SPCS-31,
   SPCS-39, SPCS-40, SPCS-41,
   SPCS-43, SPCS-44
2. Parallel / Supporting Track (only if ENTIRE critical path remaining work is currently blocked):
   SPCS-10, SPCS-11, SPCS-12, SPCS-13, SPCS-14, SPCS-15, SPCS-16,
   SPCS-45,
   (Post-Production) SPCS-33, SPCS-34, SPCS-35, SPCS-36, SPCS-37

Rationale: Advance production path first; if all critical-path candidates are blocked (waiting on code review merge or predecessor completion), harvest available parallel value.

## Read-Only Data Acquisition
Use Jira MCP search (JQL) queries ONLY. Never assume statuses—always fetch.

Fetch candidates:
JQL 1 (open work):
  project = SPCS AND statusCategory != Done AND issueType in (Story, Task)
JQL 2 (optionally narrower for performance):
  project = SPCS AND key in ( <ALL_KEYS_FROM_PRIORITY_LIST> )

Fetch individual issues (fields): key, status, statusCategory, issuetype, summary, issuelinks, priority, updated.

## Dependency Derivation
Treat Jira issue links of type "Blocks" as authoritative:
- If A "blocks" B, then B requires A statusCategory = Done before starting.
If no explicit link exists for a sequential pair in the ordered lists above, IMPLICITLY treat the immediate predecessor in that list as a dependency. (This enforces linear sequencing where explicit links might not yet be present.)

## Status Rules
A predecessor is considered satisfied ONLY if statusCategory == Done. (Do NOT treat In Review / Code Review as done.) Conservative rule prevents premature parallel starts.
Eligible (startable) candidate criteria (updated):
- Issue status exactly "To Do" (ignore In Progress / In Review / Code Review entirely — they are considered in flight and not startable)
- All explicit + implicit predecessors satisfied (statusCategory = Done)
- Issue type in (Story, Task)

Removed previous fallback of returning earliest In Progress item; now only pure To Do items are emitted.

## Selection Algorithm
1. Build ordered evaluation list = Critical Path list followed by Parallel list.
2. For each key in that list:
   a. Retrieve its issue object; if missing (not found), skip but record a warning for possible reporting (only if no candidate found).
   b. Collect predecessor set:
      - Explicit inward links of type "is blocked by" (other end of Blocks) → add those keys.
      - If issue has an earlier neighbor in its priority list, add that as implicit predecessor (unless already satisfied by explicit link set).
   c. Fetch each predecessor's statusCategory.
   d. If ANY predecessor missing or not Done → this issue is blocked → record (issue, blocking set) for potential explanation.
   e. Else if issue statusCategory in (To Do/Selected/Backlog) → mark as ready candidate; STOP scan and output key.
3. If no ready candidate found among critical path, evaluate whether ALL unresolved critical-path items were blocked; if yes, continue scanning parallel list with same procedure (still respecting their own implicit sequencing and explicit links).
4. Remove previous In Progress fallback: if no To Do candidate exists, proceed directly to explanation.
5. Construct explanation:
   - Choose the earliest To Do issue in evaluation order that is blocked OR, if none remain To Do, explain that all remaining work is already in progress/review.
   - List its blocking predecessors (keys + their statuses) when applicable.
   - Output concise sentence (no markdown formatting).

## Tie-Breakers
If multiple ready items appear simultaneously (should not happen due to STOP rule): choose the one with the smallest index in ordered list. Ignore priority field unless two parallel-track items both fully unblocked while critical path still globally blocked; then prefer higher Jira priority (if available) else earliest index.

## Validation & Safety
- Never transition or comment.
- Do not guess statuses; if a needed issue fetch fails, treat that predecessor as blocking and provide explanation.
- If Jira MCP unavailable: output explanation: "No selection; Jira unavailable (reason)." (No key.)

## Examples
Scenario A: SPCS-5 Done; SPCS-6 To Do → Return `SPCS-6`.
Scenario B: SPCS-5 In Review; SPCS-6 To Do → Blocked (explain SPCS-6 blocked by SPCS-5 In Review).
Scenario C: All remaining critical path tasks each blocked; SPCS-10 To Do with all its explicit predecessors satisfied → Return `SPCS-10`.
Scenario D: SPCS-18 In Progress; all earlier tasks Done; no other To Do tasks ready → Return `SPCS-18`.

## Execution Steps (Implementation Guidance)
1. Expand ordered key arrays (two Python lists or shell arrays) internally for dependency checks.
2. Bulk search to map key → issue object.
3. Build adjacency map from issue links (blockers per key).
4. Apply algorithm; short-circuit on first ready key.
5. Emit output per contract.

## Final Output Enforcement
Before emitting: validate output string.
- If regex ^SPCS-\d+$ matches → OK.
- Else explanation path is assumed.

Return ONLY the final output string.
