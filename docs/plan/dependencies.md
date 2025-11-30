# Dependency Graph and Critical Path Analysis

This document details all dependencies between issues to enable optimal parallel execution.

---

## Critical Path

The longest dependency chain that determines minimum project completion time:

```
M0-1 (PHP) → M1-1 (Laravel) → M1-2 (DB Config) → M3-1 (Classifications) →
M3-8 (Recipes) → M3-9 (Pivots) → M3-14 (Recipe Model) → M4-1 (Search) →
M5-1 (Controller) → M5-6 (Routes) → M6-1 (Layout) → M6-6 (Recipe Card) →
M7-1 (Recipe Index) → M9-1 (Interactivity) → M14-6 (Performance Audit) →
M16-10 (Final Testing)
```

**Critical Path Duration**: ~40-50 hours with sequential execution
**With Parallelization**: ~20-25 hours (assuming 5-6 agents)

---

## Dependency Table

| Issue | Title | Depends On | Blocks | Priority | Effort |
|-------|-------|------------|--------|----------|--------|
| **MILESTONE 0** |||||
| M0-1 | PHP Verification | None | M1-1, M0-6 | P1 | Small |
| M0-2 | Node.js Verification | None | M2-1, M0-6 | P1 | Small |
| M0-3 | Composer Verification | None | M1-1 | P1 | Small |
| M0-4 | Database Setup | None | M1-2, M3-1 | P1 | Medium |
| M0-5 | Git Setup | None | M1-3 | P1 | Small |
| M0-6 | Dev Environment | M0-1, M0-2 | M1-1 | P2 | Medium |
| M0-7 | Editor Setup | None | None | P3 | Small |
| M0-8 | System Documentation | M0-1 through M0-6 | None | P3 | Small |
| **MILESTONE 1** |||||
| M1-1 | Laravel Install | M0-1, M0-3 | M1-2, M1-3, M1-4, M1-5, M1-6, M2-1, M3-1 | P1 | Small |
| M1-2 | Database Config | M1-1, M0-4 | M3-1 | P1 | Small |
| M1-3 | Git Init | M1-1, M0-5 | None | P1 | Small |
| M1-4 | App Config | M1-1 | None | P2 | Small |
| M1-5 | Project Docs | M1-1 | None | P2 | Small |
| M1-6 | Error Logging | M1-1 | M13-10 | P2 | Small |
| **MILESTONE 2** |||||
| M2-1 | Vite Config | M1-1, M0-2 | M2-2, M2-4 | P1 | Small |
| M2-2 | Tailwind Install | M2-1 | M2-3, M2-5, M6-1, M7-1 | P1 | Medium |
| M2-3 | Test Builds | M2-2 | M10-1 | P1 | Small |
| M2-4 | Alpine.js Install | M2-1 | M9-1 | P1 | Small |
| M2-5 | Base Layout | M2-1, M2-2, M2-4 | M6-1 | P2 | Small |
| M2-6 | Frontend Docs | M2-2, M2-4 | None | P3 | Small |
| **MILESTONE 3** |||||
| M3-1 | Classifications Table | M1-2 | M3-8, M3-14 | P1 | Small |
| M3-2 | Sources Table | M1-2 | M3-8, M3-15 | P1 | Small |
| M3-3 | Meals Table | M1-2 | M3-9, M3-17 | P1 | Small |
| M3-4 | Preparations Table | M1-2 | M3-10, M3-18 | P1 | Small |
| M3-5 | Courses Table | M1-2 | M3-11, M3-19 | P1 | Small |
| M3-6 | Cookbooks Table | M1-2 | M3-12, M3-16 | P1 | Small |
| M3-8 | Recipes Table | M3-1, M3-2 | M3-9, M3-10, M3-11, M3-12, M3-14 | P1 | Medium |
| M3-9 | Recipe-Meals Pivot | M3-8, M3-3 | M3-14 | P1 | Small |
| M3-10 | Recipe-Prep Pivot | M3-8, M3-4 | M3-14 | P1 | Small |
| M3-11 | Recipe-Courses Pivot | M3-8, M3-5 | M3-14 | P1 | Small |
| M3-12 | Cookbook-Recipes Pivot | M3-8, M3-6 | M3-14, M3-16 | P1 | Small |
| M3-13 | Database Indexes | M3-8, M3-9, M3-10, M3-11, M3-12 | M4-2 | P2 | Medium |
| M3-14 | Recipe Model | M3-8, M3-9, M3-10, M3-11, M3-12 | M4-1, M5-1, M11-6, M12-6 | P1 | Medium |
| M3-15 | Classification Model | M3-1 | M3-14 | P2 | Small |
| M3-16 | Source Model | M3-2 | M3-14 | P2 | Small |
| M3-17 | Meal Model | M3-3, M3-9 | M3-14 | P2 | Small |
| M3-18 | Preparation Model | M3-4, M3-10 | M3-14 | P2 | Small |
| M3-19 | Course Model | M3-5, M3-11 | M3-14 | P2 | Small |
| M3-20 | Cookbook Model | M3-6, M3-12, M3-14 | M5-3, M8-1 | P2 | Medium |
| **MILESTONE 4** |||||
| M4-1 | Search Scope | M3-14 | M5-1, M12-8 | P1 | Small |
| M4-2 | Full-Text Test | M3-13 | None | P2 | Small |
| **MILESTONE 5** |||||
| M5-1 | RecipeController Index | M3-14, M4-1 | M5-2, M5-6, M7-1, M12-2, M13-2 | P1 | Medium |
| M5-2 | RecipeController Show | M5-1 | M5-6, M7-2, M12-3 | P1 | Small |
| M5-3 | CookbookController Index | M3-20 | M5-4, M5-7, M8-1, M12-4 | P1 | Small |
| M5-4 | CookbookController Show | M5-3 | M5-7, M8-2, M12-5 | P1 | Small |
| M5-5 | SearchRecipeRequest | M5-1 | M13-3 | P2 | Small |
| M5-6 | Recipe Routes | M5-1, M5-2 | M7-1 | P1 | Small |
| M5-7 | Cookbook Routes | M5-3, M5-4 | M8-1 | P1 | Small |
| M5-8 | Default Route | M5-6 | None | P2 | Small |
| M5-9 | Controller Tests | M5-1 through M5-4 | M12-16 | P2 | Medium |
| **MILESTONE 6** |||||
| M6-1 | Base Layout | M2-5 | M6-2 through M6-10, M7-1 | P1 | Small |
| M6-2 | Button Component | M6-1 | M7-1 | P2 | Small |
| M6-3 | Input Component | M6-1 | M7-1 | P2 | Small |
| M6-4 | Select Component | M6-1 | M6-8 | P2 | Small |
| M6-5 | Card Component | M6-1 | M6-6, M7-2 | P1 | Small |
| M6-6 | Recipe Card | M6-5 | M7-1 | P1 | Small |
| M6-7 | Pagination Component | M6-1 | M7-1 | P1 | Small |
| M6-8 | Sort Controls | M6-4 | M7-1, M9-2 | P1 | Small |
| M6-9 | Navigation | M6-1 | M9-1 | P1 | Small |
| M6-10 | Component Docs | M6-2 through M6-9 | None | P3 | Small |
| **MILESTONE 7** |||||
| M7-1 | Recipe Index View | M6-6, M6-7, M6-8, M5-6 | M9-4, M14-6 | P1 | Medium |
| M7-2 | Recipe Show View | M6-5, M5-2 | M14-7 | P1 | Small |
| M7-3 | Style Recipe Index | M7-1 | M14-6 | P2 | Small |
| M7-4 | Style Recipe Show | M7-2 | M14-7 | P2 | Small |
| M7-5 | Test Recipe Views | M7-1 through M7-4 | M14-1 | P2 | Small |
| **MILESTONE 8** |||||
| M8-1 | Cookbook Index | M5-7 | M8-3, M14-8 | P1 | Small |
| M8-2 | Cookbook Show | M5-4, M7-1 | M8-3, M14-8 | P1 | Small |
| M8-3 | Style Cookbooks | M8-1, M8-2 | M14-8 | P2 | Small |
| M8-4 | Test Cookbooks | M8-1 through M8-3 | M14-10 | P2 | Small |
| **MILESTONE 9** |||||
| M9-1 | Mobile Menu | M6-9, M2-4 | M14-10 | P1 | Small |
| M9-2 | Sort Toggle | M6-8 | None | P2 | Small |
| M9-3 | Display Count | M6-4 | None | P2 | Small |
| M9-4 | Search Enhancement | M7-1 | None | P2 | Small |
| M9-5 | Hover Effects | M6-6 | None | P3 | Small |
| M9-6 | Test Interactivity | M9-1 through M9-5 | M14-10 | P2 | Small |
| **MILESTONE 10** |||||
| M10-1 | Production Build | M2-3 | M16-5 | P1 | Small |
| M10-2 | Test Build | M10-1 | M14-5 | P1 | Small |
| M10-3 | Asset Versioning | M10-1 | M14-5 | P2 | Small |
| M10-4 | Build Docs | M10-1 through M10-3 | M16-6 | P3 | Small |
| **MILESTONE 11** |||||
| M11-1 | ClassificationSeeder | M3-15 | M11-8 | P1 | Small |
| M11-2 | SourceSeeder | M3-16 | M11-8 | P1 | Small |
| M11-3 | MealSeeder | M3-17 | M11-8 | P1 | Small |
| M11-4 | PreparationSeeder | M3-18 | M11-8 | P1 | Small |
| M11-5 | CourseSeeder | M3-19 | M11-8 | P1 | Small |
| M11-6 | RecipeFactory | M3-14 | M11-8 | P1 | Medium |
| M11-7 | CookbookFactory | M3-20 | M11-8 | P1 | Small |
| M11-8 | DatabaseSeeder | M11-1 through M11-7 | M11-9, M12-2 through M12-5 | P1 | Small |
| M11-9 | Test Seeding | M11-8 | None | P2 | Small |
| M11-10 | Seeding Docs | M11-9 | M16-6 | P3 | Small |
| **MILESTONE 12** |||||
| M12-1 | Configure Pest | M1-2 | M12-2 through M12-16 | P1 | Small |
| M12-2 | RecipeIndexTest | M5-1, M11-8 | M12-16 | P1 | Medium |
| M12-3 | RecipeShowTest | M5-2, M11-8 | M12-16 | P1 | Small |
| M12-4 | CookbookIndexTest | M5-3, M11-8 | M12-16 | P1 | Small |
| M12-5 | CookbookShowTest | M5-4, M11-8 | M12-16 | P1 | Small |
| M12-6 | RecipeModelTest | M3-14 | M12-16 | P1 | Medium |
| M12-7 | CookbookModelTest | M3-20 | M12-16 | P1 | Small |
| M12-8 | SearchTest | M4-1 | M12-16 | P1 | Small |
| M12-9-12 | Other Model Tests | M3-15 through M3-19 | M12-16 | P2 | Small each |
| M12-13 | N+1 Query Test | M5-1, M5-2 | M12-16 | P1 | Small |
| M12-14 | DB Transaction Test | M3-1 through M3-12 | M12-16 | P2 | Small |
| M12-15 | Code Coverage | M12-1 through M12-14 | M12-16, M15-6 | P1 | Small |
| M12-16 | Full Test Suite | M12-15 | M15-1 | P1 | Small |
| **MILESTONE 13** |||||
| M13-1 | Security Headers | M1-1 | M13-12, M16-11 | P1 | Small |
| M13-2 | Rate Limiting | M5-1 | M13-12 | P1 | Small |
| M13-3 | Form Validation | M5-1 | M13-12 | P1 | Small |
| M13-4 | CSRF Test | M7-1 | M13-12 | P1 | Small |
| M13-5 | HTTPS Enforcement | M1-4 | M13-12, M16-11 | P1 | Small |
| M13-6 through M13-9 | Error Views | M6-1 | M13-12 | P1 | Small each |
| M13-10 | Exception Handler | M1-6 | M13-12 | P1 | Small |
| M13-11 | Error Monitoring | M1-1 | M16-9 | P3 | Medium |
| M13-12 | Security Testing | M13-1 through M13-10 | M16-11 | P1 | Medium |
| **MILESTONE 14** |||||
| M14-1 | Accessibility | M7-1 through M8-3 | M14-6 through M14-8 | P1 | Medium |
| M14-2 | Skip Navigation | M6-9 | M14-1 | P2 | Small |
| M14-3 | Query Performance | M3-13, M5-1 | M14-11 | P1 | Medium |
| M14-4 | Result Caching | M11-1 through M11-5 | M14-11 | P2 | Small |
| M14-5 | Asset Optimization | M10-1 | M14-6 through M14-8 | P1 | Small |
| M14-6 | Lighthouse Recipe Index | M7-3, M14-1 | M14-11, M14-12 | P1 | Medium |
| M14-7 | Lighthouse Recipe Show | M7-4, M14-1 | M14-11, M14-12 | P1 | Small |
| M14-8 | Lighthouse Cookbooks | M8-3, M14-1 | M14-11, M14-12 | P1 | Small |
| M14-9 | Browser Testing | M7-1 through M8-3 | M14-12 | P1 | Medium |
| M14-10 | Responsive Testing | M7-3, M8-3 | M14-12 | P1 | Medium |
| M14-11 | Performance Docs | M14-6 through M14-10 | M16-6 | P2 | Small |
| M14-12 | Fix Issues | M14-6 through M14-10 | M16-11 | P1 | Large |
| **MILESTONE 15** |||||
| M15-1 | GitHub Actions | M12-16 | M15-8 | P1 | Medium |
| M15-2 | PHPStan Config | M1-1 | M15-1, M15-4 | P1 | Small |
| M15-3 | Pint Config | M1-1 | M15-1, M15-4 | P1 | Small |
| M15-4 | Pre-commit Hooks | M15-2, M15-3 | None | P3 | Small |
| M15-5 | Dependabot | M1-1 | None | P2 | Small |
| M15-6 | Coverage Reporting | M12-15 | M15-1 | P2 | Small |
| M15-7 | Deployment Auto | M15-1 | M16-12 | P1 | Medium |
| M15-8 | Test CI/CD | M15-1 through M15-7 | M16-11 | P1 | Medium |
| **MILESTONE 16** |||||
| M16-1 | Backup Strategy | M1-2 | M16-2, M16-9 | P1 | Medium |
| M16-2 | Test Backup | M16-1 | M16-3 | P1 | Small |
| M16-3 | Disaster Recovery | M16-2 | M16-8 | P1 | Medium |
| M16-4 | Staging Environment | M1-1 | M16-12 | P1 | Medium |
| M16-5 | Update README | M1-1, M2-6, M14-11 | M16-10 | P1 | Medium |
| M16-6 | DEVELOPMENT.md | All milestones | M16-10 | P1 | Medium |
| M16-7 | DEPLOYMENT.md | M15-7, M16-1 | M16-10 | P1 | Medium |
| M16-8 | DISASTER_RECOVERY.md | M16-3 | M16-10 | P1 | Small |
| M16-9 | .env.example | M1-2, M13-11, M16-1 | M16-10 | P1 | Small |
| M16-10 | Test Fresh Install | M16-5 through M16-9 | M16-11 | P1 | Medium |
| M16-11 | Deployment Checklist | M16-6 through M16-10 | M16-12 | P1 | Medium |
| M16-12 | Deploy to Staging | M16-4, M16-11 | M16-13 | P1 | Large |
| M16-13 | Post-Deploy Verify | M16-12 | M16-14 | P1 | Medium |
| M16-14 | Production Deploy | M16-13 | M16-15 | P1 | Large |
| M16-15 | Production Verify | M16-14 | None | P1 | Medium |

---

## Blocking Analysis

**Most Blocking Issues** (block the most other issues):
1. M1-1 (Laravel Install) - Blocks 11 issues
2. M3-8 (Recipes Table) - Blocks 9 issues
3. M3-14 (Recipe Model) - Blocks 7 issues
4. M6-1 (Base Layout) - Blocks 10 issues
5. M2-1 (Vite Config) - Blocks 3 issues

**Most Blocked Issues** (have the most dependencies):
1. M16-15 (Production Verify) - Depends on M16-14
2. M16-14 (Production Deploy) - Depends on M16-13
3. M16-13 (Post-Deploy Verify) - Depends on M16-12
4. M3-14 (Recipe Model) - Depends on 6 issues
5. M16-10 (Test Fresh Install) - Depends on 5 issues

---

## Parallel Execution Waves

### Wave 1: Foundation (M0)
**6 agents in parallel**:
- Agent 1: M0-1 → M0-6
- Agent 2: M0-2
- Agent 3: M0-3
- Agent 4: M0-4
- Agent 5: M0-5
- Agent 6: M0-7
- Any: M0-8

### Wave 2: Laravel Setup (M1)
**1 agent sequential, then 4 parallel**:
- Agent 1: M1-1 → M1-2
- Then parallel: M1-3, M1-4, M1-5, M1-6

### Wave 3: Frontend (M2)
**2-3 agents**:
- Agent 1: M2-1 → M2-2 → M2-5
- Agent 2: Wait for M2-1 → M2-4
- Agent 3: Wait for M2-2 → M2-3
- Any: M2-6

### Wave 4-8: Database (M3) + Search (M4)
**6 agents, multiple waves**:
- See M3 details in phase-3 document
- M4-1 starts as soon as M3-14 complete
- M4-2 starts after M3-13

### Wave 9-13: Controllers & Views (M5-M8)
**High parallelization**:
- M5 controllers can start as dependencies complete
- M6 components parallel after M6-1
- M7, M8 views parallel after controllers and components ready

### Wave 14-16: Enhancements (M9-M11)
**Maximum parallelization**:
- All of M9, M10, M11 can proceed simultaneously
- ~12-15 issues across 5-6 agents

### Wave 17: Testing (M12)
**High parallelization**:
- M12-1 first, then 15-20 test files in parallel

### Wave 18-20: Quality (M13-M15)
**Moderate parallelization**:
- M13 security issues mostly parallel
- M14 performance/accessibility sequential testing
- M15 CI/CD mostly parallel

### Wave 21: Deployment (M16)
**Sequential with some parallel**:
- Docs can be parallel
- Deployment must be sequential

---

## Recommendations for Parallel Execution

1. **Start Strong**: M0 can have all 6 agents working simultaneously
2. **Database Phase**: M3 has highest parallelization potential (20 issues, many independent)
3. **Component Library**: M6 components can be built by 4-5 agents simultaneously
4. **Testing Phase**: M12 allows 5-6 agents writing different test files
5. **If Blocked**: Move agents to later milestones while waiting for blockers
   - Example: If waiting for M3-14, start M11 seeders or M13 security setup

---

## Visual Dependency Graph

```
M0-1,2,3,4,5,6,7 (Parallel)
    ↓
M1-1 → M1-2 → M3-1,2,3,4,5,6 (Parallel)
             ↓
          M3-8 (Recipes)
             ↓
M3-9,10,11,12 (Parallel Pivots)
             ↓
    M3-14,15,16,17,18,19,20 (Parallel Models)
             ↓
          M4-1 (Search)
             ↓
       M5-1,3 (Controllers)
             ↓
    M5-2,4,6,7,8 (Routes & Show)
             ↓
M2-1 → M2-2 → M6-1 → M6-2,3,4,5,6,7,8,9 (Parallel Components)
                  ↓
            M7-1,M7-2 (Recipe Views)
                  ↓
            M8-1,M8-2 (Cookbook Views)
                  ↓
        M9-1,2,3,4,5,6 (Parallel Interactivity)
        M10-1,2,3,4 (Parallel Assets)
        M11-1,2,3,4,5,6,7,8,9 (Parallel Seeding)
                  ↓
     M12-1 → M12-2,3,4,5,6,7,8,9... (Parallel Tests) → M12-16
                  ↓
        M13-1,2,3... (Parallel Security)
        M14-1,2,3... (Sequential Performance)
        M15-1,2,3... (Parallel CI/CD)
                  ↓
    M16-1→M16-2→M16-3... (Sequential Deployment)
```

This graph shows the critical path and points where parallelization is possible.
