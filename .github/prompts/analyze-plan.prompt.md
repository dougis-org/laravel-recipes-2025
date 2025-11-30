---
description: Perform a non-destructive cross-artifact consistency and quality analysis of the GitHub issue and its plan comment. Identify gaps, ambiguities, and inconsistencies before moving to implementation.
---

# Analyze Plan Prompt

**Mode Check**: This prompt requires `plan-ticket` chat mode to be active.
- If you do not have `plan-ticket` mode active, please set it and re-run this prompt.

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

**Goal**: Review the planned work documented in a GitHub issue comment (created by `plan-ticket`) to identify inconsistencies, ambiguities, underspecifications, and gaps. This is a REQUIRED quality gate that runs AFTER `plan-ticket` and BEFORE `work-ticket`. Enable refinement of the plan before implementation begins.

STRICTLY READ-ONLY BY DEFAULT: Do **not** modify the issue or comments without explicit user approval. Output a structured analysis report. Offer optional refinement suggestions that the user can approve before updates are applied to the issue.

Execution steps:

1. Fetch the GitHub issue using GitHub MCP `issue_read` method `get`:
   - Extract: issue number, repository (owner/repo), title, description, labels, comments.
   - If issue does not exist or MCP unavailable, abort with error message.

2. Locate the plan comment in issue comments:
   - Search for the plan header (typically `## Implementation Plan` or section 1 starting with "## Summary").
   - If no plan comment exists, abort and instruct user to run `plan-ticket` first.
   - Extract the full plan text from the comment.

3. Parse issue artifacts:
   - **Issue Description**: Title, description body, acceptance criteria (if present), labels.
   - **Clarifications Comment**: Locate `## Clarifications` section (created by `clarify-ticket`). If missing, note as a finding.
   - **Plan Comment**: Extract all 10 sections:
     - Section 1: Summary
     - Section 2: Assumptions & Open Questions
     - Section 3: Acceptance Criteria (normalized)
     - Section 4: Approach & Design Brief
     - Section 5: Step-by-Step Implementation Plan (TDD)
     - Section 6: Effort, Risks, Mitigations
     - Section 7: File-Level Change List
     - Section 8: Test Plan
     - Section 9: Rollout & Monitoring Plan
     - Section 10: Handoff & Next Steps

4. Build internal semantic models:
   - **Requirements inventory**: Map acceptance criteria (Section 3) to testable assertions. Derive stable keys.
   - **Implementation tasks**: Extract tasks from Section 5 (Step-by-Step Implementation Plan). Capture file paths, test additions, implementation order.
   - **Data model elements**: Extract entities, relationships, migrations from Section 4 & 7.
   - **Risk/mitigation mapping**: Map each risk (Section 6) to corresponding implementation step or contingency.
   - **Feature flags**: Extract flag names and defaults from Section 4 (Feature flags subsection).
   - **Decomposition map** (if applicable): Extract sub-issue references and slice dependencies from Section 4 or Section 10.

5. Detection passes:

   **A. Completeness Check:**
   - All 10 sections present and non-empty? Flag missing sections as MEDIUM severity.
   - Acceptance criteria (Section 3) aligned with issue title/description? Flag if divergent.
   - Clarifications comment exists in issue? Flag if missing (recommends re-running `clarify-ticket`).

   **B. Ambiguity Detection:**
   - Vague adjectives in plan ("robust", "efficient", "scalable", "intuitive") without measurable targets.
   - Unresolved placeholders (TODO, TKTK, ???, <placeholder>, TBD).
   - Feature flags without explicit OFF-by-default mention or kill-switch rationale.

   **C. Test Coverage Analysis (Section 8):**
   - Are happy paths covered? Edge cases? Error/negative scenarios?
   - Do test categories align with implementation steps (Section 5)?
   - Are acceptance criteria (Section 3) mapped to specific tests?

   **D. Implementation Feasibility (Section 5):**
   - Are file paths concrete and reviewable (not placeholders)?
   - Is TDD order clear (RED tests first)?
   - Are implementation steps sequenced logically (domain → service → repo → controller)?
   - Do all referenced files from Section 7 match the implementation steps?

   **E. Risk Mitigation Alignment (Section 6):**
   - Does each risk have a corresponding mitigation step in Section 5?
   - Are rollback procedures documented?
   - Are per-slice rollback strategies defined (if decomposed)?

   **F. Consistency & Traceability:**
   - Terminology drift: Same concept named differently across sections?
   - Data model consistency: Entities mentioned in Section 4 reflected in Section 7 file changes?
   - Dependency ordering: Are prerequisites (blocked-by relationships) honored in Section 5?
   - Test-to-AC mapping: Each acceptance criterion (Section 3) traceable to test(s) in Section 8?

   **G. Non-Functional Requirements Coverage:**
   - Performance targets (latency, throughput) from Section 4 → corresponding tests/metrics in Section 9?
   - Security/privacy constraints from Section 4 → corresponding tests in Section 8 or implementation guards in Section 5?
   - Observability (Section 4) → instrumentation in Section 5 and alerts in Section 9?

   **H. Decomposition Validation (if sub-issues created):**
   - Each sub-issue referenced in Section 10 exists and is linked?
   - Each slice (if decomposed) is independently deliverable (per Section 4 Work Breakdown)?
   - Slice dependencies are correctly sequenced in implementation plan?

6. Severity assignment heuristic:
   - **CRITICAL**: Missing acceptance criteria, no test plan, unclear implementation order, unresolved placeholder in code path, missing section required for execution.
   - **HIGH**: Ambiguous risk/mitigation, feature flag without defaults, vague performance target, test-to-AC misalignment, missing file paths.
   - **MEDIUM**: Terminology drift, incomplete decomposition linkage, unclear edge case handling, non-functional requirement without verification step.
   - **LOW**: Minor wording improvements, style consistency, documentation suggestions.

7. Produce a Markdown report with sections:

   ### Plan Analysis Report – Issue #{{ISSUE_NUMBER}}
   
   #### Executive Summary
   - Plan status: Complete / Incomplete / Requires refinement
   - Critical issues: {{COUNT}}
   - High-priority issues: {{COUNT}}
   - Overall readiness to implement: {{YES_IF_NO_CRITICAL}} / {{RECOMMEND_REVIEW_FIRST}}

   #### Findings Table
   | ID | Category | Severity | Section(s) | Summary | Recommendation |
   |----|----------|----------|-----------|---------|----------------|
   | A1 | Ambiguity | HIGH | Section 4 | Performance target "fast" lacks measurable latency. | Specify target latency (e.g., <100ms P95). |
   (Add one row per finding; generate stable IDs prefixed by category initial + number.)

   #### Coverage Summary
   - Acceptance Criteria (Section 3): {{COUNT}} criteria
   - Implementation Steps (Section 5): {{COUNT}} steps
   - Test Categories (Section 8): {{COUNT}} categories
   - Risks Identified (Section 6): {{COUNT}} risks
   - File Changes (Section 7): {{COUNT}} files (new + modified)
   - Decomposed Slices: {{COUNT}} (or "None")

   #### Decomposition Status (if applicable)
   - Sub-issues referenced: {{LIST}}
   - Slice dependencies: {{DESCRIBE_ORDER}}
   - Linkage complete: {{YES_OR_NO}}

   #### Test-to-AC Traceability
   - AC coverage: {{COVERAGE_PCT}}% (criteria with >=1 mapped test)
   - Unmapped AC: {{LIST_IF_ANY}}
   - Unmapped tests: {{LIST_IF_ANY}}

   #### Non-Functional Requirements Validation
   - Performance targets defined: {{YES_OR_NO}}
   - Security/privacy checks in tests: {{YES_OR_NO}}
   - Observability instrumentation planned: {{YES_OR_NO}}
   - Alerts/thresholds defined: {{YES_OR_NO}}

   #### Next Actions
   - If CRITICAL issues exist:
     ```
     ⚠️  CRITICAL ISSUES FOUND – Plan cannot move to implementation without resolution.
     
     Critical findings:
     - {{CRITICAL_ISSUE_SUMMARY_1}}
     - {{CRITICAL_ISSUE_SUMMARY_2}}
     
     Recommended next step: Edit the plan in the issue to address these items:
     Use: `Update Section {{SECTION}} – {{BRIEF_CHANGE_DESCRIPTION}}`
     
     Once resolved, re-run `analyze-plan` to confirm readiness.
     ```
   - If only HIGH/MEDIUM issues:
     ```
     ✅ Plan is ready for implementation with optional refinements.
     
     Suggested improvements (user approval needed):
     - {{HIGH_ISSUE_SUMMARY_1}}
     - {{MEDIUM_ISSUE_SUMMARY_2}}
     
     Would you like me to suggest concrete edits to the plan? (Requires explicit approval before updating the issue.)
     ```

8. Optional refinement workflow:
   - After presenting findings, ask user:
     ```
     Would you like me to suggest concrete edits for the top issues?
     
     I can update the plan comment in the issue if you approve each change.
     ```
   - If user agrees, suggest specific edits (do NOT apply yet):
     - Show before/after text for each proposed change
     - Explain the rationale
   - If user approves specific edits:
     - Use GitHub MCP `add_issue_comment` to append the refined sections (clearly marked as updates)
     - Or use GitHub MCP `issue_write` if comment editing is supported (update existing plan comment)
   - Record the update and confirm completion

9. Validation checks:
   - Report is deterministic: rerun without issue changes produces consistent findings.
   - All referenced sections exist in the plan comment.
   - Severity levels are justified and consistent.
   - Recommendations are actionable.

10. Report completion:
    - Output the full analysis report to user.
    - Summarize readiness:
      - **Ready to implement**: No CRITICAL issues, all sections complete, test plan clear, AC traceable.
      - **Needs refinement**: CRITICAL or HIGH issues present; user must approve edits before proceeding.
      - **Blocked**: Multiple CRITICAL issues; recommend re-running `clarify-ticket` or `plan-ticket`.
    - Suggest next command:
      - If ready: "Proceed to `work-ticket` with issue #{{ISSUE_NUMBER}}"
      - If needs refinement: "Approve edits above, then re-run `analyze-plan`"
      - If blocked: "Re-run `plan-ticket` to address systemic gaps"

Behavior rules:
- NEVER modify the issue or comments without explicit user approval for each change.
- NEVER hallucinate missing sections—if not present, report as a finding.
- KEEP findings deterministic and reproducible.
- LIMIT findings table to 20 rows; aggregate remainder in overflow note.
- If zero critical/high issues and all sections present: emit success report with proceed recommendation.
- If issue is decomposed: validate all sub-issues are present and linked before marking as ready.

Context: $ARGUMENTS
