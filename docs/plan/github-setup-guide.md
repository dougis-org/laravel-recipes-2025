# GitHub Setup Guide

**Purpose**: Step-by-step guide to create GitHub milestones and issues for the Laravel Recipes project.

**Approach**: Manual creation using `gh` CLI for flexibility and control. While this could be automated, manual creation allows for review and adjustment as needed.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup GitHub CLI](#setup-github-cli)
3. [Create Repository Labels](#create-repository-labels)
4. [Create Milestones](#create-milestones)
5. [Create Issues](#create-issues)
6. [Issue Templates](#issue-templates)
7. [Automation Helpers](#automation-helpers)
8. [Best Practices](#best-practices)

---

## Prerequisites

### Required Tools
- **GitHub CLI (`gh`)**: Install from https://cli.github.com/
- **Git**: Already installed
- **GitHub Account**: With access to create issues/milestones

### Verify Installation
```bash
gh --version
gh auth status
```

If not authenticated:
```bash
gh auth login
```

---

## Setup GitHub CLI

### Configure Repository

```bash
# Verify current repository
gh repo view

# Set default repository (optional)
gh repo set-default
```

### Test Access

```bash
# List existing issues
gh issue list

# List existing milestones
gh api repos/:owner/:repo/milestones

# Create repository if needed
# gh repo create laravel-recipes-2025 --public
```

---

## Create Repository Labels

Labels should be created before issues. Run once per repository.

### Script: Create All Labels

```bash
#!/bin/bash
# File: scripts/create-labels.sh

# Phase labels
for i in {0..16}; do
  gh label create "phase-$i" \
    --description "Phase $i tasks" \
    --color "0E8A16" || true
done

# Type labels
gh label create "type:setup" --description "Setup and configuration" --color "1D76DB" || true
gh label create "type:feature" --description "New feature" --color "0052CC" || true
gh label create "type:docs" --description "Documentation" --color "5319E7" || true
gh label create "type:testing" --description "Testing and QA" --color "FBCA04" || true
gh label create "type:optimization" --description "Performance optimization" --color "FF6B6B" || true

# Priority labels
gh label create "P1" --description "Critical priority" --color "D73A4A" || true
gh label create "P2" --description "High priority" --color "FF9500" || true
gh label create "P3" --description "Normal priority" --color "0075CA" || true

# Effort labels
gh label create "effort:small" --description "< 1 hour" --color "C2E0C6" || true
gh label create "effort:medium" --description "1-2 hours" --color "FEF2C0" || true
gh label create "effort:large" --description "> 2 hours" --color "F9D0C4" || true

# Status labels
gh label create "status:ready" --description "Ready to start" --color "0E8A16" || true
gh label create "status:in-progress" --description "Work in progress" --color "FBCA04" || true
gh label create "status:blocked" --description "Blocked by dependency" --color "D73A4A" || true
gh label create "status:review" --description "In review" --color "5319E7" || true

echo "✅ Labels created successfully"
```

### Run Label Creation

```bash
chmod +x scripts/create-labels.sh
./scripts/create-labels.sh
```

---

## Create Milestones

### Milestone Template

```bash
gh api repos/:owner/:repo/milestones \
  -X POST \
  -f title="Milestone N - Description" \
  -f description="Goal and summary" \
  -f due_on="2025-MM-DD"
```

### Script: Create All Milestones

```bash
#!/bin/bash
# File: scripts/create-milestones.sh

# Milestone 0
gh api repos/:owner/:repo/milestones -X POST \
  -f title="Milestone 0 - Prerequisites & System Requirements" \
  -f description="Verify and document system prerequisites for Laravel 12 development" \
  -f state="open"

# Milestone 1
gh api repos/:owner/:repo/milestones -X POST \
  -f title="Milestone 1 - Project Setup" \
  -f description="Initialize Laravel 12 project with dependencies and configuration" \
  -f state="open"

# Milestone 2
gh api repos/:owner/:repo/milestones -X POST \
  -f title="Milestone 2 - Frontend Stack" \
  -f description="Set up Vite, Tailwind CSS 4+, and Alpine.js 3.14+" \
  -f state="open"

# Milestone 3
gh api repos/:owner/:repo/milestones -X POST \
  -f title="Milestone 3 - Database & Models" \
  -f description="Create all migrations, models, and relationships" \
  -f state="open"

# Milestone 4
gh api repos/:owner/:repo/milestones -X POST \
  -f title="Milestone 4 - Search" \
  -f description="Implement recipe search functionality" \
  -f state="open"

# Milestone 5
gh api repos/:owner/:repo/milestones -X POST \
  -f title="Milestone 5 - Controllers & Routing" \
  -f description="Create controllers and routes for recipes and cookbooks" \
  -f state="open"

# Milestone 6
gh api repos/:owner/:repo/milestones -X POST \
  -f title="Milestone 6 - Layout & Components" \
  -f description="Create base layout and reusable Blade components" \
  -f state="open"

# Milestone 7
gh api repos/:owner/:repo/milestones -X POST \
  -f title="Milestone 7 - Recipe Views" \
  -f description="Create recipe listing and detail views" \
  -f state="open"

# Milestone 8
gh api repos/:owner/:repo/milestones -X POST \
  -f title="Milestone 8 - Cookbook Views" \
  -f description="Create cookbook listing and detail views" \
  -f state="open"

# Milestone 9
gh api repos/:owner/:repo/milestones -X POST \
  -f title="Milestone 9 - Interactivity" \
  -f description="Add Alpine.js interactive features" \
  -f state="open"

# Milestone 10
gh api repos/:owner/:repo/milestones -X POST \
  -f title="Milestone 10 - Asset Pipeline" \
  -f description="Optimize production build and asset versioning" \
  -f state="open"

# Milestone 11
gh api repos/:owner/:repo/milestones -X POST \
  -f title="Milestone 11 - Database Seeding" \
  -f description="Create seeders and factories for all models" \
  -f state="open"

# Milestone 12
gh api repos/:owner/:repo/milestones -X POST \
  -f title="Milestone 12 - Testing" \
  -f description="Comprehensive PHPUnit/Pest test suite" \
  -f state="open"

# Milestone 13
gh api repos/:owner/:repo/milestones -X POST \
  -f title="Milestone 13 - Security & Error Handling" \
  -f description="Security hardening and error page creation" \
  -f state="open"

# Milestone 14
gh api repos/:owner/:repo/milestones -X POST \
  -f title="Milestone 14 - Performance & Accessibility" \
  -f description="WCAG compliance and performance optimization" \
  -f state="open"

# Milestone 15
gh api repos/:owner/:repo/milestones -X POST \
  -f title="Milestone 15 - CI/CD Pipeline" \
  -f description="GitHub Actions workflow and code quality tools" \
  -f state="open"

# Milestone 16
gh api repos/:owner/:repo/milestones -X POST \
  -f title="Milestone 16 - Documentation & Deployment" \
  -f description="Comprehensive documentation and deployment setup" \
  -f state="open"

echo "✅ Milestones created successfully"
```

### Run Milestone Creation

```bash
chmod +x scripts/create-milestones.sh
./scripts/create-milestones.sh
```

### Get Milestone Numbers

After creating milestones, get their numbers:

```bash
gh api repos/:owner/:repo/milestones | jq -r '.[] | "\(.number): \(.title)"'
```

Output example:
```
1: Milestone 0 - Prerequisites & System Requirements
2: Milestone 1 - Project Setup
3: Milestone 2 - Frontend Stack
...
```

---

## Create Issues

### Issue Creation Command

```bash
gh issue create \
  --title "M0-1: Verify PHP Installation and Extensions" \
  --body "$(cat issue-body.md)" \
  --label "phase-0,type:setup,P1,effort:small,status:ready" \
  --milestone 1
```

### Issue Body Template

```markdown
## Story
As a developer
I want to verify PHP 8.5+ is installed with all required extensions
So that Laravel 12 can run without errors

## Acceptance Criteria
- [ ] PHP version 8.5 or higher verified
- [ ] All required extensions installed:
  - [ ] BCMath, Ctype, Fileinfo, JSON, Mbstring, OpenSSL, PDO, Tokenizer, XML
- [ ] Created documentation file: `docs/setup/php-setup.md`

## Files to Create/Modify
- `docs/setup/php-setup.md` (create)

## Dependencies
**Depends On**: None
**Blocks**: M1-1 (Laravel installation)

## Testing
\`\`\`bash
php -v
php -m | grep -i mbstring
\`\`\`

## References
- Phase file: `docs/plan/phase-0-prerequisites.md`
- Issue: M0-1
```

---

## Issue Templates

### Template: Small Setup Task

```markdown
## Story
As a [role]
I want [feature]
So that [benefit]

## Acceptance Criteria
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Files to Create/Modify
- `path/to/file.ext` (create/modify)

## Dependencies
**Depends On**: [Issue numbers or "None"]
**Blocks**: [Issue numbers or "None"]

## Testing
\`\`\`bash
# Commands to verify
\`\`\`

## References
- Phase: [phase number]
- Docs: `docs/plan/phase-X-name.md`
```

### Template: Feature Implementation

```markdown
## Story
As a [user type]
I want [feature]
So that [benefit]

## Acceptance Criteria
### Functionality
- [ ] Feature requirement 1
- [ ] Feature requirement 2

### Code Quality
- [ ] Tests written and passing
- [ ] Code follows Laravel conventions
- [ ] No N+1 queries

### Documentation
- [ ] Inline comments for complex logic
- [ ] Updated relevant docs

## Implementation Notes
[Optional: Technical approach, gotchas, etc.]

## Files to Create/Modify
- `app/Models/Example.php` (create)
- `database/migrations/xxx.php` (create)
- `tests/Feature/ExampleTest.php` (create)

## Dependencies
**Depends On**: M3-1, M3-2
**Blocks**: M5-1, M7-2

## Testing
\`\`\`bash
php artisan test --filter=ExampleTest
\`\`\`

## References
- Phase: Milestone 3 - Database & Models
- Docs: `docs/plan/phase-3-database-models.md`
```

---

## Automation Helpers

### Helper: Create Issue from Phase File

For each issue in a phase file, create using this template:

```bash
#!/bin/bash
# create-issue.sh - Helper to create single issue

MILESTONE=$1
ISSUE_ID=$2
TITLE=$3
PHASE=$4
TYPE=$5
PRIORITY=$6
EFFORT=$7

gh issue create \
  --title "$ISSUE_ID: $TITLE" \
  --body-file "issues/$ISSUE_ID.md" \
  --label "phase-$PHASE,$TYPE,$PRIORITY,$EFFORT,status:ready" \
  --milestone "$MILESTONE"
```

Usage:
```bash
./create-issue.sh 1 "M0-1" "Verify PHP Installation" 0 "type:setup" "P1" "effort:small"
```

### Bulk Issue Creation

Create a CSV file with all issues:

```csv
milestone,id,title,phase,type,priority,effort,depends_on,blocks
1,M0-1,Verify PHP Installation,0,type:setup,P1,effort:small,None,M1-1
1,M0-2,Verify Node.js Installation,0,type:setup,P1,effort:small,None,M1-1
...
```

Then process with a script:

```bash
#!/bin/bash
# bulk-create-issues.sh

while IFS=, read -r milestone id title phase type priority effort depends blocks; do
  # Skip header
  [[ "$milestone" == "milestone" ]] && continue

  # Create issue body
  cat > /tmp/issue-body.md <<EOF
## Issue: $id

**Dependencies**:
- Depends On: $depends
- Blocks: $blocks

See \`docs/plan/phase-$phase-*.md\` for full details.
EOF

  # Create issue
  gh issue create \
    --title "$id: $title" \
    --body-file /tmp/issue-body.md \
    --label "phase-$phase,$type,$priority,$effort,status:ready" \
    --milestone "$milestone"

  echo "✅ Created $id"
  sleep 1  # Rate limiting
done < issues.csv
```

---

## Best Practices

### 1. Start Small
- Create Milestone 0 and its issues first
- Test the workflow
- Adjust templates as needed
- Then bulk create remaining milestones

### 2. Use Consistent Naming
- Issue titles: `M#-#: Description`
- Labels: Lowercase, hyphen-separated
- Milestones: "Milestone # - Description"

### 3. Include Dependencies in Body
Since GitHub doesn't have native dependency tracking:
- List dependencies in issue body
- Use labels to mark blockers: `status:blocked`
- Reference by issue number in comments

### 4. Link to Phase Docs
Every issue should reference its phase file:
```markdown
## References
- Docs: `docs/plan/phase-3-database-models.md`
- Section: M3-8
```

### 5. Use Projects for Visualization
Create a GitHub Project to visualize:
- Column per milestone
- Drag issues between columns
- Filter by label

```bash
# Create project
gh project create --title "Laravel Recipes Development" --owner @me
```

### 6. Automate Status Updates
Use GitHub Actions to:
- Auto-add `status:in-progress` when PR created
- Auto-add `status:review` when PR ready
- Auto-close issue when PR merged

---

## Quick Start Commands

### Complete Setup (Run in Order)

```bash
# 1. Create labels
./scripts/create-labels.sh

# 2. Create milestones
./scripts/create-milestones.sh

# 3. Get milestone numbers
gh api repos/:owner/:repo/milestones | jq -r '.[] | "\(.number): \(.title)"'

# 4. Create issues for Milestone 0 (manual or scripted)
# ... create each issue ...

# 5. Verify
gh issue list --milestone 1
gh issue list --label "phase-0"
```

### Helpful Commands

```bash
# List all labels
gh label list

# List all milestones
gh api repos/:owner/:repo/milestones | jq -r '.[] | .title'

# List issues in milestone
gh issue list --milestone "Milestone 0 - Prerequisites"

# Search issues
gh issue list --label "P1" --label "status:ready"

# Update issue
gh issue edit 123 --add-label "status:in-progress"

# Close issue
gh issue close 123 --comment "Completed in PR #456"
```

---

## Troubleshooting

### API Rate Limiting
If you hit rate limits:
```bash
# Check rate limit status
gh api rate_limit

# Add sleep between issue creation
sleep 2
```

### Authentication Issues
```bash
# Re-authenticate
gh auth logout
gh auth login

# Verify permissions
gh auth status
```

### Milestone Not Found
```bash
# List milestones with numbers
gh api repos/:owner/:repo/milestones

# Use milestone number, not title
gh issue create --milestone 1  # Use number, not name
```

---

## Summary

**Manual Approach Benefits:**
- ✅ Full control over each issue
- ✅ Review before creating
- ✅ Adjust on the fly
- ✅ Learn GitHub CLI

**For 180 Issues:**
- **Manual creation**: ~4-6 hours (with copy-paste)
- **Scripted creation**: ~1-2 hours (with preparation)

**Recommendation**:
1. Start with manual creation for Milestone 0 (8 issues)
2. Refine process based on learnings
3. Create helper scripts for remaining milestones
4. Bulk create with scripts once process proven

---

## Next Steps

After issues are created:

1. **Assign to project board**
2. **Set up branch protection** for main
3. **Configure automation** (labels, auto-close)
4. **Brief the team** on workflow
5. **Start with Milestone 0** following `docs/plan/parallel-work-strategy.md`

**Ready to begin!** 🚀
