# Claude Code Slash Commands

This directory contains slash commands that map to the GitHub Copilot prompts and chat modes defined in `.github/prompts/` and `.github/chatmodes/`.

## Available Commands

### 1. `/find-next-ticket`
**Purpose**: Find the next GitHub issue to work on (read-only)
**Mode**: `find-next-ticket`
**Prompt**: `.github/prompts/find-next-ticket.prompt.md`
**Chat Mode**: `.github/chatmodes/find-next-ticket.chatmode.md`

Identifies the next logical GitHub issue to start based on priority, dependencies, and blockers.

**Output**: Issue number OR blocker explanation

### 2. `/clarify-ticket`
**Purpose**: Resolve ambiguities in a GitHub issue before planning
**Mode**: `plan-ticket`
**Prompt**: `.github/prompts/clarify-ticket.prompt.md`
**Chat Mode**: `.github/chatmodes/plan-ticket.chatmode.md`

Asks up to 5 targeted clarification questions to reduce ambiguity before creating an implementation plan.

**Output**: Clarifications comment added to GitHub issue

### 3. `/plan-ticket`
**Purpose**: Create detailed TDD implementation plan
**Mode**: `plan-ticket`
**Prompt**: `.github/prompts/plan-ticket.prompt.md`
**Chat Mode**: `.github/chatmodes/plan-ticket.chatmode.md`

Generates a comprehensive 10-section implementation plan with TDD approach, decomposition analysis, and file-level change lists.

**Output**: Plan comment added to GitHub issue

### 4. `/analyze-plan`
**Purpose**: Quality gate - validate plan before implementation
**Mode**: `plan-ticket`
**Prompt**: `.github/prompts/analyze-plan.prompt.md`
**Chat Mode**: `.github/chatmodes/plan-ticket.chatmode.md`

Reviews plan for completeness, ambiguities, test coverage, feasibility, and consistency. Identifies CRITICAL/HIGH/MEDIUM/LOW severity issues.

**Output**: Analysis report comment added to GitHub issue

### 5. `/work-ticket`
**Purpose**: Execute implementation with TDD workflow
**Mode**: `work-ticket`
**Prompt**: `.github/prompts/work-ticket.prompt.md`
**Chat Mode**: `.github/chatmodes/work-ticket.chatmode.md`

Implements the approved plan using strict TDD (RED → GREEN → Refactor), runs quality gates, and creates PR.

**Output**: Implementation code, tests, docs, and PR

## Standard Workflow

The complete workflow for a GitHub issue follows this sequence:

```
1. /find-next-ticket
   ↓ (returns issue #N)
   ↓ (user confirms)

2. /clarify-ticket #N
   ↓ (asks clarification questions)
   ↓ (records answers in issue)

3. /plan-ticket #N
   ↓ (creates 10-section plan)
   ↓ (plan added as issue comment)

4. /analyze-plan #N
   ↓ (validates plan quality)
   ↓ (identifies issues)

5. /work-ticket #N
   ↓ (implements plan with TDD)
   ↓ (creates PR)
```

## Quality Gates

Each command has specific quality gates:

### `/find-next-ticket` Gates
- Issue is not already `in-progress`
- All dependencies are satisfied (state = closed)
- Issue state is exactly "open"

### `/clarify-ticket` Gates
- Issue exists in GitHub
- Maximum 5 questions asked
- Each answer recorded incrementally

### `/plan-ticket` Gates
- **CRITICAL**: Clarifications must exist (run `/clarify-ticket` first)
- All 10 plan sections must be complete
- Decomposition decision documented
- Branch created

### `/analyze-plan` Gates
- **CRITICAL**: Plan must exist (run `/plan-ticket` first)
- All 10 sections validated
- CRITICAL issues must be resolved before proceeding

### `/work-ticket` Gates
- **CRITICAL**: Analysis must be complete (run `/analyze-plan` first)
- No CRITICAL issues in analysis
- All tests pass (TDD enforcement)
- Feature flags default OFF
- Signed commits required

## Decomposition Support

For complex issues, the workflow supports decomposition into sub-issues:

```
1. /plan-ticket #N
   ↓ (detects complexity)
   ↓ (proposes decomposition)
   ↓ (creates sub-issues #N-1, #N-2, #N-3)

2. For each sub-issue:
   /clarify-ticket #N-1
   /plan-ticket #N-1
   /analyze-plan #N-1
   /work-ticket #N-1

   (repeat for #N-2, #N-3, etc.)

3. All slice PRs merged in dependency order
```

## Chat Mode Configuration

Each command requires its associated chat mode to be active:

- **find-next-ticket mode**: Read-only GitHub operations, dependency analysis
- **plan-ticket mode**: Planning with decomposition, no implementation
- **work-ticket mode**: TDD implementation, quality gates, PR creation

## References

### Prompt Files
- `.github/prompts/find-next-ticket.prompt.md`
- `.github/prompts/clarify-ticket.prompt.md`
- `.github/prompts/plan-ticket.prompt.md`
- `.github/prompts/analyze-plan.prompt.md`
- `.github/prompts/work-ticket.prompt.md`

### Chat Mode Files
- `.github/chatmodes/find-next-ticket.chatmode.md`
- `.github/chatmodes/plan-ticket.chatmode.md`
- `.github/chatmodes/work-ticket.chatmode.md`

### Shared Guidance
- `.github/prompts/includes/branch-commit-guidance.md`
- `.github/prompts/includes/plan-file-structure.schema.json`

## Usage Examples

### Start new work
```
/find-next-ticket
```

### Clarify issue #42
```
/clarify-ticket #42
```

### Plan issue #42
```
/plan-ticket #42
```

### Analyze plan for issue #42
```
/analyze-plan #42
```

### Implement issue #42
```
/work-ticket #42
```

## Notes

- All commands use GitHub MCP server for issue operations
- Desktop Commander MCP for file operations and process execution
- Context7 MCP for dependency version resolution
- Sequential Thinking MCP for complex reasoning when needed
