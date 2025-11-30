---
description: Identify and resolve ambiguities in a GitHub issue before planning
---

# Clarify Ticket Command

## Mode Requirements
Before executing this command, set the `plan-ticket` chat mode which is defined in `.github/chatmodes/plan-ticket.chatmode.md`.

## Instructions
Follow the detailed instructions in `.github/prompts/clarify-ticket.prompt.md`.

## Guidelines from Chat Mode
- This is a planning preparation step (uses plan-ticket mode)
- Maximum 5 clarification questions allowed
- Each question must be answerable with multiple-choice OR short phrase (≤5 words)
- Questions prioritized by impact on architecture, data modeling, and testing
- Sequential questioning loop (one question at a time)
- Updates issue with clarifications comment after each answer

## Execution Steps
1. Verify `plan-ticket` chat mode is active
2. Fetch the GitHub issue using GitHub MCP
3. Perform ambiguity scan across taxonomy categories
4. Generate prioritized clarification questions (max 5)
5. Present questions one at a time
6. After each answer, update issue comment incrementally
7. Output coverage summary and recommend next steps

## Next Steps
After clarifications are complete, proceed to `/plan-ticket` with the same issue.
