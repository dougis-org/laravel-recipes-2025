---
description: Identify underspecified areas in a GitHub issue by asking up to 5 highly targeted clarification questions and encoding answers back into the issue.
---

# Clarify Ticket Prompt

**Mode Check**: This prompt requires `plan-ticket` chat mode to be active.
- If you do not have `plan-ticket` mode active, please set it and re-run this prompt.

The user input to you can be provided directly by the agent or as a command argument - you **MUST** consider it before proceeding with the prompt (if not empty).

User input:

$ARGUMENTS

**Goal**: Detect and reduce ambiguity or missing decision points in the GitHub issue and record the clarifications directly as a comment within the issue.

Note: This clarification workflow is expected to run (and be completed) BEFORE invoking `plan-ticket`. If the user explicitly states they are skipping clarification (e.g., exploratory spike), you may proceed, but must warn that downstream rework risk increases.

Execution steps:

1. Fetch the GitHub issue using GitHub MCP `issue_read` method `get`:
   - Extract: issue number, repository (owner/repo), title, description, labels, assignees, linked issues, existing comments.
   - If issue does not exist or MCP unavailable, abort and instruct user to provide valid GitHub issue URL or number.

2. Load the issue description and existing comments. Perform a structured ambiguity & coverage scan using this taxonomy. For each category, mark status: Clear / Partial / Missing. Produce an internal coverage map used for prioritization (do not output raw map unless no questions will be asked).

   Functional Scope & Behavior:
   - Core user goals & success criteria
   - Explicit out-of-scope declarations
   - User roles / personas differentiation

   Domain & Data Model:
   - Entities, attributes, relationships
   - Identity & uniqueness rules
   - Lifecycle/state transitions
   - Data volume / scale assumptions

   Interaction & UX Flow:
   - Critical user journeys / sequences
   - Error/empty/loading states
   - Accessibility or localization notes

   Non-Functional Quality Attributes:
   - Performance (latency, throughput targets)
   - Scalability (horizontal/vertical, limits)
   - Reliability & availability (uptime, recovery expectations)
   - Observability (logging, metrics, tracing signals)
   - Security & privacy (authN/Z, data protection, threat assumptions)
   - Compliance / regulatory constraints (if any)

   Integration & External Dependencies:
   - External services/APIs and failure modes
   - Data import/export formats
   - Protocol/versioning assumptions

   Edge Cases & Failure Handling:
   - Negative scenarios
   - Rate limiting / throttling
   - Conflict resolution (e.g., concurrent edits)

   Constraints & Tradeoffs:
   - Technical constraints (language, storage, hosting)
   - Explicit tradeoffs or rejected alternatives

   Terminology & Consistency:
   - Canonical glossary terms
   - Avoided synonyms / deprecated terms

   Completion Signals:
   - Acceptance criteria testability
   - Measurable Definition of Done style indicators

   Misc / Placeholders:
   - TODO markers / unresolved decisions
   - Ambiguous adjectives ("robust", "intuitive") lacking quantification

   For each category with Partial or Missing status, add a candidate question opportunity unless:
   - Clarification would not materially change implementation or validation strategy
   - Information is better deferred to planning phase (note internally)

3. Generate (internally) a prioritized queue of candidate clarification questions (maximum 5). Do NOT output them all at once. Apply these constraints:
    - Maximum of 5 total questions across the whole session.
    - Each question must be answerable with EITHER:
       * A short multiple‑choice selection (2–5 distinct, mutually exclusive options), OR
       * A one-word / short‑phrase answer (explicitly constrain: "Answer in <=5 words").
    - Only include questions whose answers materially impact architecture, data modeling, task decomposition, test design, UX behavior, operational readiness, or compliance validation.
    - Ensure category coverage balance: attempt to cover the highest impact unresolved categories first; avoid asking two low-impact questions when a single high-impact area (e.g., security posture) is unresolved.
    - Exclude questions already answered, trivial stylistic preferences, or plan-level execution details (unless blocking correctness).
    - Favor clarifications that reduce downstream rework risk or prevent misaligned acceptance tests.
    - If more than 5 categories remain unresolved, select the top 5 by (Impact * Uncertainty) heuristic.

4. Sequential questioning loop (interactive):
    - Present EXACTLY ONE question at a time.
    - For multiple‑choice questions render options as a Markdown table:

       | Option | Description |
       |--------|-------------|
       | A | <Option A description> |
       | B | <Option B description> |
       | C | <Option C description> | (add D/E as needed up to 5)
       | Short | Provide a different short answer (<=5 words) | (Include only if free-form alternative is appropriate)

    - For short‑answer style (no meaningful discrete options), output a single line after the question: `Format: Short answer (<=5 words)`.
    - After the user answers:
       * Validate the answer maps to one option or fits the <=5 word constraint.
       * If ambiguous, ask for a quick disambiguation (count still belongs to same question; do not advance).
       * Once satisfactory, record it in working memory (do not yet write to disk) and move to the next queued question.
    - Stop asking further questions when:
       * All critical ambiguities resolved early (remaining queued items become unnecessary), OR
       * User signals completion ("done", "good", "no more"), OR
       * You reach 5 asked questions.
    - Never reveal future queued questions in advance.
    - If no valid questions exist at start, immediately report no critical ambiguities.

5. Integration after EACH accepted answer (incremental update approach):
    - Maintain in-memory representation of the issue (loaded once at start) plus the raw issue description and comments.
    - For the first integrated answer in this session:
       * Use GitHub MCP `add_issue_comment` to start a new clarifications thread with a header:
         ```
         ## Clarifications – Session {{YYYY-MM-DD}}
         ```
    - After each subsequent accepted answer, append to the clarifications comment (via GitHub MCP `add_issue_comment` for each new answer, or batch update via single comprehensive comment):
       * Append a bullet line: `- Q: <question> → A: <final answer>`.
    - If needed, create a follow-up comment to update issue description with refined acceptance criteria, data model details, or non-functional requirements (use GitHub MCP `issue_write` method `update`):
       * Update the issue description to incorporate clarifications materially affecting scope, user stories, or acceptance criteria.
       * Preserve original description structure; patch in clarified sections inline or add a note `[Clarified per session {{YYYY-MM-DD}}]`.
    - Record answers as close to the categorized section they address (in description update or as annotation in comment).
    - Preserve formatting: do not reorder issue description sections; keep heading hierarchy intact.
    - Keep each inserted clarification minimal and testable (avoid narrative drift).

6. Validation (performed after EACH write plus final pass):
   - Clarifications comment contains exactly one bullet per accepted answer (no duplicates).
   - Total asked (accepted) questions ≤ 5.
   - Updated issue description sections contain no lingering vague placeholders the new answers were meant to resolve.
   - No contradictory earlier statement remains (scan for now-invalid alternative choices removed).
   - Markdown structure valid in issue description and comment.
   - Terminology consistency: same canonical term used across all updated issue sections.

7. Report completion (after questioning loop ends or early termination):
   - Number of questions asked & answered.
   - Issue number & repository reference.
   - Sections touched in issue description (list section names).
   - Coverage summary table listing each taxonomy category with Status: Resolved (was Partial/Missing and addressed), Deferred (exceeds question quota or better suited for planning), Clear (already sufficient), Outstanding (still Partial/Missing but low impact).
   - Link to clarifications comment thread in issue.
   - If any Outstanding or Deferred remain, recommend whether to proceed to `plan-ticket` or run `clarify-ticket` again later post-plan.
   - Suggested next command.

Behavior rules:
- If no meaningful ambiguities found (or all potential questions would be low-impact), respond: "No critical ambiguities detected worth formal clarification." and suggest proceeding to `plan-ticket`.
- If issue does not exist or cannot be fetched, abort and instruct user to provide valid issue.
- Never exceed 5 total asked questions (clarification retries for a single question do not count as new questions).
- Avoid speculative tech stack questions unless the absence blocks functional clarity.
- Respect user early termination signals ("stop", "done", "proceed").
- If no questions asked due to full coverage, output a compact coverage summary (all categories Clear) then suggest advancing to `plan-ticket`.
- If quota reached with unresolved high-impact categories remaining, explicitly flag them under Deferred with rationale.

Context for prioritization: $ARGUMENTS
