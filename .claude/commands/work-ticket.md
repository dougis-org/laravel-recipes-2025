---
description: Execute an approved implementation plan with TDD workflow
---

# Work Ticket Command

## Mode Requirements
Before executing this command, set the `work-ticket` chat mode which is defined in `.github/chatmodes/work-ticket.chatmode.md`.

## Instructions
Follow the detailed instructions in `.github/prompts/work-ticket.prompt.md`.

## Guidelines from Chat Mode
- Strict TDD enforcement: RED → GREEN → Refactor
- Quality gates must pass before PR creation
- Signed commits required (-S flag)
- Supports decomposed sub-issues with full workflow iteration
- Feature flags default to OFF for new runtime behavior

## Pre-Work Gate
**CRITICAL**: Before implementation, verify that `/analyze-plan` has been run:
- Check for `## Plan Analysis` comment in issue
- If missing: STOP and run `/analyze-plan` first
- If analysis has CRITICAL issues: STOP and require resolution
- If exists with no CRITICAL issues: Proceed to implementation

## Decomposition Detection
Before Phase 0, check if issue is decomposed:
- If sub-issues exist: Execute Sub-Issue Iteration Loop
  - For each sub-issue: run `/clarify-ticket` → `/plan-ticket` → `/analyze-plan` → `/work-ticket`
- If single issue: Execute Phase 0-7 implementation workflow

## Execution Phases
**Phase 0**: Setup & Plan Review
**Phase 1**: Test-Driven Development (RED)
**Phase 2**: Implement (GREEN)
**Phase 3**: Docs & Artifacts
**Phase 4**: Quality Gates
**Phase 5**: Acceptance Verification
**Phase 6**: Commit & PR
**Phase 7**: Handoff Summary

## Quality Gates
All gates must pass before PR creation:
- ✅ All tests pass
- ✅ Test coverage meets threshold
- ✅ Feature flags default OFF
- ✅ Code style compliant
- ✅ Schema migrations valid
- ✅ Security review complete
- ✅ All ACs verified

## Execution Steps
1. Verify `work-ticket` chat mode is active
2. Check for analyze-plan completion (REQUIRED)
3. Detect decomposition (sub-issues vs single issue)
4. Execute implementation workflow (Phase 0-7)
5. Create signed commits with conventional format
6. Create PR with full context
7. Update issue with execution summary

## Next Steps
After implementation complete:
- PR review by assigned reviewers
- Address review feedback
- Merge to main
- Deploy per rollout plan
