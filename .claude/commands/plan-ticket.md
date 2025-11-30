---
description: Create a detailed TDD implementation plan for a GitHub issue
---

# Plan Ticket Command

## Mode Requirements
Before executing this command, set the `plan-ticket` chat mode which is defined in `.github/chatmodes/plan-ticket.chatmode.md`.

## Instructions
Follow the detailed instructions in `.github/prompts/plan-ticket.prompt.md`.

## Guidelines from Chat Mode
- Output: 10-section implementation plan with TDD-first approach
- No production code implementation in this mode
- Plans must be deterministic and test-driven
- Feature flags default to OFF unless justified
- Decomposition decision required for all tickets
- Context7 MCP for dependency version resolution

## Pre-Planning Gate
**CRITICAL**: Before planning, verify that `/clarify-ticket` has been run:
- Check for `## Clarifications` section in issue comments
- If missing: STOP and run `/clarify-ticket` first
- If exists: Proceed to planning

## Execution Steps
1. Verify `plan-ticket` chat mode is active
2. Check for clarifications (REQUIRED before planning)
3. Fetch GitHub issue and verify branch creation
4. Assess decomposition need (split into sub-issues if applicable)
5. Scan repository for patterns and context
6. Construct 10-section plan
7. Publish plan as issue comment(s) via GitHub MCP
8. Output next steps message

## Next Steps
After plan is complete, proceed to `/analyze-plan` with the same issue.
