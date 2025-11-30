---
description: Review and validate a GitHub issue plan for quality and completeness
---

# Analyze Plan Command

## Mode Requirements
Before executing this command, set the `plan-ticket` chat mode which is defined in `.github/chatmodes/plan-ticket.chatmode.md`.

## Instructions
Follow the detailed instructions in `.github/prompts/analyze-plan.prompt.md`.

## Guidelines from Chat Mode
- This is a quality gate that runs AFTER `/plan-ticket` and BEFORE `/work-ticket`
- STRICTLY READ-ONLY by default (no modifications without user approval)
- Output structured analysis report with severity levels
- Optional refinement suggestions require explicit user approval

## Pre-Analysis Gate
**CRITICAL**: Before analyzing, verify that `/plan-ticket` has been run:
- Check for plan comment with 10 sections in issue
- If missing: STOP and run `/plan-ticket` first
- If exists: Proceed to analysis

## Execution Steps
1. Verify `plan-ticket` chat mode is active
2. Fetch GitHub issue and locate plan comment
3. Parse all 10 plan sections
4. Run detection passes:
   - Completeness Check
   - Ambiguity Detection
   - Test Coverage Analysis
   - Implementation Feasibility
   - Risk Mitigation Alignment
   - Consistency & Traceability
   - Non-Functional Requirements Coverage
   - Decomposition Validation (if applicable)
5. Assign severity levels (CRITICAL, HIGH, MEDIUM, LOW)
6. Generate Markdown analysis report
7. Publish analysis as issue comment
8. Suggest next steps based on findings

## Next Steps
- If CRITICAL issues: Fix plan, re-run `/analyze-plan`
- If no CRITICAL issues: Proceed to `/work-ticket` with the same issue
