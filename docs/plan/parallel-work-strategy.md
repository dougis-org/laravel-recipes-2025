# Parallel Work Strategy

**Goal**: Maximize development velocity by coordinating 5-6 AI agents working simultaneously on the Laravel Recipes project.

**Key Principle**: Keep all agents productive by enabling them to find available work when blocked, rather than waiting idle.

---

## Table of Contents

1. [Agent Coordination Model](#agent-coordination-model)
2. [Finding Available Work](#finding-available-work)
3. [Handling Blockers](#handling-blockers)
4. [Wave-Based Execution](#wave-based-execution)
5. [Critical Path Awareness](#critical-path-awareness)
6. [Communication Protocol](#communication-protocol)
7. [Conflict Resolution](#conflict-resolution)
8. [Phase-by-Phase Strategies](#phase-by-phase-strategies)
9. [Example Scenarios](#example-scenarios)

---

## Agent Coordination Model

### Optimal Team Size
- **Target**: 5-6 concurrent agents
- **Minimum**: 3 agents (below this, parallelization benefits diminish)
- **Maximum**: 8 agents (above this, coordination overhead increases)

### Agent Roles
Agents are **homogeneous** - any agent can work on any task. However, for efficiency:

1. **Critical Path Agent**: Focuses on blocking issues (M1-1, M3-8, M3-14, M6-1)
2. **Parallel Agents (4-5)**: Work on independent tasks in current wave
3. **Flexible Agent**: Ready to switch milestones if blocked

### Work Assignment Strategy

**Priority Order for Selecting Tasks:**
1. **Unblocked tasks in current milestone** (finish what you started)
2. **Unblocked tasks in next milestone** (prepare the path)
3. **Tasks in different milestone** (avoid idle time)
4. **Documentation tasks** (always available, low dependency)

---

## Finding Available Work

### Quick Reference Guide

When looking for available work, use this decision tree:

```
1. Are there unblocked tasks in my current milestone?
   YES → Pick highest priority unblocked task
   NO → Go to step 2

2. Are there unblocked tasks in the next milestone?
   YES → Start next milestone task
   NO → Go to step 3

3. Are there unblocked tasks in ANY milestone?
   YES → Jump to that milestone
   NO → Pick documentation/testing task

4. Still no available work?
   → Review dependencies.md for recently completed blockers
   → Check if any "Blocks" have been resolved
```

### Using dependencies.md

The `docs/plan/dependencies.md` file is your source of truth. For each task:

```markdown
| Issue | Depends On | Blocks | Priority | Effort |
|-------|-----------|--------|----------|--------|
| M3-8  | M3-1-M3-7 | M3-14  | P1       | medium |
```

**To find available work:**
1. Find issues with `Depends On: None` or all dependencies completed
2. Check `Priority` (P1 > P2 > P3)
3. Check `Effort` (prefer small for quick wins, medium for substantial progress)

### GitHub Project Board

Once milestones are created in GitHub:

```bash
# List available issues
gh issue list --label "ready" --label "phase-3" --limit 20

# Filter by size
gh issue list --label "ready" --label "effort:small"

# Find next critical path item
gh issue list --label "ready" --label "P1" --label "phase-3"
```

---

## Handling Blockers

### When You're Blocked

**DO:**
✅ **Switch milestones immediately** - Don't wait
✅ **Document the blocker** - Update issue or leave comment
✅ **Find related work** - Look for tasks in the same domain
✅ **Work on documentation** - Always available
✅ **Work on testing** - Can often be prepared early

**DON'T:**
❌ Wait for blocker to resolve
❌ Try to work around dependencies
❌ Start unrelated work without updating status

### Example: Blocked Scenario

**Situation**: You're working on M5-1 (RecipeController) but M4-1 (Search scope) is incomplete.

**Actions:**
1. Mark M5-1 as `blocked` with comment: "Waiting for M4-1 (Search scope)"
2. Check dependencies.md for other unblocked M5 tasks → M5-3 (CookbookController) is available
3. Start M5-3 instead
4. If M5-3 also blocked, jump to M6 (Layout & Components)

### Common Blockers and Workarounds

| Blocker | Workaround |
|---------|-----------|
| Model not created | Jump to different milestone |
| Migration pending | Work on frontend/components |
| Controller incomplete | Work on views (use mock data) |
| Frontend component missing | Work on backend/models |
| All current milestone blocked | Jump to M11 (Seeding) or M13 (Security) |

---

## Wave-Based Execution

Each milestone has waves of parallelizable work. Execute waves sequentially, but parallelize within waves.

### Wave Execution Pattern

```
Wave 1 (All agents parallel)
  ├─ Agent 1: Task A
  ├─ Agent 2: Task B
  ├─ Agent 3: Task C
  └─ Wait for all to complete

Wave 2 (All agents parallel)
  ├─ Agent 1: Task D (depends on A)
  ├─ Agent 2: Task E (depends on B)
  └─ Wait for all to complete

Wave 3 (Sequential)
  └─ Agent 1: Task F (depends on D+E)
```

### Example: Phase 3 (Database Models)

**Wave 1** - Lookup Tables (6 agents parallel):
- Agent 1: M3-1 (Classifications)
- Agent 2: M3-2 (Sources)
- Agent 3: M3-3 (Meals)
- Agent 4: M3-4 (Preparations)
- Agent 5: M3-5 (Courses)
- Agent 6: M3-6 (Cookbooks)

**Wave 2** - Main Table (1 agent, others jump to M2 or M6):
- Agent 1: M3-8 (Recipes table)
- Agents 2-6: Work on M2 (Frontend) or M6 (Components)

**Wave 3** - Pivot Tables (4 agents parallel):
- Agent 1: M3-9 (Recipe-Meals)
- Agent 2: M3-10 (Recipe-Preparations)
- Agent 3: M3-11 (Recipe-Courses)
- Agent 4: M3-12 (Cookbook-Recipes)

---

## Critical Path Awareness

### Critical Path Items

These issues block the most work - prioritize them:

1. **M1-1** (Laravel Install) - Blocks 11 issues
2. **M3-8** (Recipes Table) - Blocks 9 issues
3. **M3-14** (Recipe Model) - Blocks 7 issues
4. **M6-1** (Base Layout) - Blocks 10 issues
5. **M5-1** (RecipeController) - Blocks 3 issues

### Critical Path Strategy

**Assign your best/fastest agent to critical path items.**

```
Agent Assignment:
├─ Agent 1 (Critical Path): M1-1 → M3-8 → M3-14 → M6-1 → M5-1
└─ Agents 2-6 (Parallel): Work on non-blocking tasks
```

**Impact:**
- Agent 1 completing M3-8 unblocks 9 tasks for other agents
- Agent 1 completing M6-1 unblocks all component work
- This maximizes overall throughput

---

## Communication Protocol

### Agent Status Updates

Each agent should maintain awareness of:
1. **Current task** (issue number and title)
2. **Status** (in_progress, blocked, completed)
3. **ETA** (estimated completion time)
4. **Blockers** (what they're waiting for)

### Recommended Status Format

```markdown
## Agent Status Board

**Agent 1**: M3-8 (Recipes Migration) - In Progress - ETA: 30min
**Agent 2**: M6-2 (Button Component) - Completed - Moving to M6-3
**Agent 3**: M5-1 (RecipeController) - Blocked by M4-1 - Switching to M5-3
**Agent 4**: M11-6 (RecipeFactory) - In Progress - ETA: 45min
**Agent 5**: M2-2 (Tailwind CSS) - In Progress - ETA: 1hr
```

### Issue Labels for Coordination

Use GitHub labels to coordinate:

```
status:ready        → Available for pickup
status:in-progress  → Agent working on it
status:blocked      → Waiting on dependency
status:review       → Ready for review
status:complete     → Merged and done
```

---

## Conflict Resolution

### File Conflicts

**Prevention:**
- Different agents work on different files
- Avoid 2+ agents in same milestone when possible
- Use wave-based approach to minimize conflicts

**When conflicts occur:**
1. First agent to push wins
2. Second agent rebases and resolves conflicts
3. Focus on different files next time

### Merge Conflicts

**Small conflicts** (imports, formatting):
- Resolve immediately and push

**Large conflicts** (logic changes):
- Coordinate with other agent
- Consider splitting the file
- One agent handles the merge

---

## Phase-by-Phase Strategies

### Phase 0 - Prerequisites (8 tasks, 2-4 hours)

**Optimal: 6 agents parallel**

```
Agent 1: M0-1 (PHP verification)
Agent 2: M0-2 (Node.js verification)
Agent 3: M0-3 (Composer verification)
Agent 4: M0-4 (Database setup)
Agent 5: M0-5 (Git setup)
Agent 6: M0-6 (VS Code setup)
```

All tasks independent - perfect parallelization.

### Phase 1 - Project Setup (6 tasks, 2-3 hours)

**Sequential start, then parallel:**

```
Wave 1: Agent 1: M1-1 (Laravel install)
Wave 2 (parallel):
  ├─ Agent 1: M1-2 (Database config)
  ├─ Agent 2: M1-3 (Git init)
  ├─ Agent 3: M1-4 (App config)
  ├─ Agent 4: M1-5 (Documentation)
  └─ Agent 5: M1-6 (Logging setup)
```

### Phase 2 - Frontend Stack (6 tasks, 3-4 hours)

**Sequential start, then parallel:**

```
Wave 1: Agent 1: M2-1 (Vite config)
Wave 2 (parallel):
  ├─ Agent 1: M2-2 (Tailwind CSS)
  └─ Agent 2: M2-4 (Alpine.js)
Wave 3: Agent 1: M2-3 (Test builds)
Wave 4 (parallel):
  ├─ Agent 1: M2-5 (Base layout)
  └─ Agent 2: M2-6 (Documentation)
```

### Phase 3 - Database Models (20 tasks, 8-12 hours)

**4 waves, excellent parallelization:**

See [Wave-Based Execution](#wave-based-execution) section above.

**Key strategy**: While Wave 2 (M3-8 Recipes table) is running, other agents should:
- Jump to M2 (Frontend) if incomplete
- Jump to M6 (Components) to prepare
- Jump to M11 (Seeding) to create seeders

### Phase 4 - Search (2 tasks, 2-3 hours)

**Mostly sequential:**

```
Agent 1: M4-1 (Search scope)
Agent 2: M4-2 (Performance testing) - optional, can run parallel
Agents 3-6: Work on M5 or M6
```

### Phase 5 - Controllers (9 tasks, 6-8 hours)

**3 waves:**

```
Wave 1 (parallel):
  ├─ Agent 1: M5-1 (RecipeController index)
  └─ Agent 2: M5-3 (CookbookController index)

Wave 2 (parallel):
  ├─ Agent 1: M5-2 (RecipeController show)
  ├─ Agent 2: M5-4 (CookbookController show)
  ├─ Agent 3: M5-5 (Form request)
  ├─ Agent 4: M5-6 (Recipe routes)
  └─ Agent 5: M5-7 (Cookbook routes)

Wave 3 (parallel):
  ├─ Agent 1: M5-8 (Default route)
  └─ Agent 2: M5-9 (Tests)
```

### Phase 6 - Components (10 tasks, 8-10 hours)

**Sequential start (M6-1), then 4-5 parallel:**

```
Wave 1: Agent 1: M6-1 (Base layout) - CRITICAL PATH

Wave 2 (all parallel):
  ├─ Agent 1: M6-2 (Button)
  ├─ Agent 2: M6-3 (Input)
  ├─ Agent 3: M6-4 (Select)
  ├─ Agent 4: M6-5 (Card)
  └─ Agent 5: M6-7 (Pagination)

Wave 3 (parallel):
  ├─ Agent 1: M6-6 (Recipe card) - depends on M6-5
  ├─ Agent 2: M6-8 (Sort controls) - depends on M6-4
  └─ Agent 3: M6-9 (Navigation)

Wave 4: Agent 1: M6-10 (Documentation)
```

### Phase 7-11 - Similar Patterns

Follow the wave strategies outlined in each phase file. General rules:
- **Views/Frontend**: 2-3 agents max (many dependencies)
- **Interactivity**: 5-6 agents (very parallel)
- **Seeding**: 5 agents in wave 1, then sequential
- **Testing**: 1-2 agents (often sequential)

---

## Example Scenarios

### Scenario 1: Project Kickoff

**Team**: 6 agents
**Phase**: M0 (Prerequisites)

```
9:00 AM - All agents start M0 tasks in parallel
├─ Agent 1: M0-1 (PHP)      ├─ 30 min → ✅ Done 9:30
├─ Agent 2: M0-2 (Node.js)  ├─ 30 min → ✅ Done 9:30
├─ Agent 3: M0-3 (Composer) ├─ 30 min → ✅ Done 9:30
├─ Agent 4: M0-4 (Database) ├─ 45 min → ✅ Done 9:45
├─ Agent 5: M0-5 (Git)      ├─ 20 min → ✅ Done 9:20
└─ Agent 6: M0-6 (VS Code)  └─ 30 min → ✅ Done 9:30

9:45 AM - M0 complete, move to M1
Agent 1: M1-1 (Laravel install) - CRITICAL PATH
Agents 2-6: Wait or start M2-6 (documentation prep)

10:30 AM - M1-1 complete, unblocks M1-2 through M1-6
├─ Agent 1: M1-2 (Database config)
├─ Agent 2: M1-3 (Git init)
├─ Agent 3: M1-4 (App config)
├─ Agent 4: M1-5 (Documentation)
└─ Agent 5: M1-6 (Logging)

11:30 AM - M1 complete, move to M2
```

**Result**: M0 and M1 completed in 2.5 hours with 6 agents vs. 6-8 hours solo.

### Scenario 2: Agent Blocked Mid-Phase

**Situation**: Agent 3 working on M5-1 (RecipeController), but M4-1 incomplete.

```
Agent 3 Actions:
1. Check dependencies.md → M5-1 depends on M4-1 ❌
2. Mark M5-1 as blocked in GitHub
3. Check other M5 tasks → M5-3 available ✅
4. Start M5-3 (CookbookController index)
5. Complete M5-3
6. Check M4-1 status → Still in progress
7. Jump to M6 (Components) → M6-2 available ✅
8. Start M6-2 (Button component)
```

**Result**: Agent 3 stayed productive by switching tasks rather than waiting.

### Scenario 3: Critical Path Bottleneck

**Situation**: M3-8 (Recipes table) blocking 9 issues, all agents waiting.

```
Current State:
├─ Agent 1: M3-8 (Recipes table) - In Progress
└─ Agents 2-6: Waiting for M3-8 to complete?

❌ WRONG APPROACH: Wait idle

✅ RIGHT APPROACH: Jump milestones
├─ Agent 2: Jump to M2-2 (Tailwind CSS)
├─ Agent 3: Jump to M6-1 (Base layout) - also critical
├─ Agent 4: Jump to M11-1 (ClassificationSeeder)
├─ Agent 5: Jump to M11-2 (SourceSeeder)
└─ Agent 6: Jump to M13-6 (Error views)

When M3-8 completes:
→ Agents return to M3 for wave 3 (pivot tables)
```

**Result**: All agents productive, M3-8 doesn't create idle time.

---

## Best Practices Summary

### DO ✅
- Start each day with dependencies.md review
- Always have 2-3 backup tasks identified
- Jump milestones when blocked
- Focus on critical path items
- Communicate status clearly
- Complete small tasks quickly for momentum
- Work on documentation when truly blocked

### DON'T ❌
- Wait idle for blockers
- Work on tasks with unmet dependencies
- Start work without checking dependencies
- Ignore priority labels
- Work on same files as another agent
- Skip testing for speed
- Create merge conflicts unnecessarily

### Success Metrics

Track these to optimize parallelization:
- **Agent Utilization**: % time agents actively working (target: >85%)
- **Blocking Time**: Average time waiting on blockers (target: <10%)
- **Critical Path Progress**: Issues completed per day on critical path
- **Parallel Efficiency**: Actual completion time vs. theoretical minimum

---

## Tools and Resources

### Essential Files
- `docs/plan/dependencies.md` - Dependency tracking
- `docs/plan/README.md` - Project overview
- Each `docs/plan/phase-*.md` - Detailed phase plans

### GitHub Commands
```bash
# Find available work
gh issue list --label "status:ready" --label "P1"

# Mark issue in progress
gh issue edit <number> --add-label "status:in-progress"

# Mark issue blocked
gh issue edit <number> --add-label "status:blocked"

# Find issues you can help unblock
gh issue list --label "status:blocked"
```

### Quick Decision Matrix

| Situation | Action |
|-----------|--------|
| Current task blocked | Switch to different task in same milestone |
| All current milestone blocked | Jump to next milestone |
| All milestones blocked | Work on documentation/testing |
| Critical path item available | Drop current work and pick it up |
| Small task vs. medium task | Prefer small for quick wins |
| P1 vs. P2 tasks | Always prefer P1 |

---

## Conclusion

Successful parallel execution requires:
1. **Awareness** of dependencies and blockers
2. **Flexibility** to switch tasks/milestones
3. **Communication** of status and progress
4. **Focus** on critical path items
5. **Efficiency** through proper task selection

With 5-6 well-coordinated agents following this strategy, the ~180 issues can be completed in **~80-110 hours of wall-clock time** vs. the ~130 hours of sequential work - a **20-40% improvement** through parallelization.

**Remember**: An idle agent is wasted capacity. When blocked, find available work immediately.
