## Summary

<!-- Brief description of what this PR accomplishes -->

**Closes**: #<!-- Issue number -->

---

## Type of Change

- [ ] Feature
- [ ] Bugfix
- [ ] Refactor
- [ ] Documentation
- [ ] Performance improvement
- [ ] Dependency update
- [ ] Other (please describe)

---

## Implementation Plan Reference

<!-- Link to the plan comment in the associated issue -->

**Plan**: [Link to plan comment](#)

**Key Sections**:
- **Acceptance Criteria**: #AC1, #AC2, #AC3 (from plan Section 3)
- **Test Coverage**: Unit tests, integration tests, edge cases (from plan Section 8)
- **Rollout Strategy**: [Brief summary from plan Section 9]

---

## Changes Made

### Files Modified

<!-- List key files changed with brief description -->

- `path/to/File1.php`: Description of changes
- `path/to/File2.php`: Description of changes
- `tests/Feature/Test1.php`: New test coverage

### Database Changes

<!-- If applicable, list migrations -->

- [ ] No database schema changes
- [ ] Migration(s): `YYYY_MM_DD_HHMMSS_description.php`

### Feature Flags

<!-- List any new feature flags and their defaults -->

- [ ] No feature flags added
- [ ] Flags added: `feature.flag.name` (default: OFF)

---

## Quality Assurance

- [ ] All acceptance criteria verified (manual spot checks)
- [ ] All tests passing: `php artisan test`
- [ ] Test coverage: <!--percentage or "meets threshold"-->
- [ ] Code follows Laravel conventions (per AGENTS.md)
- [ ] No new security or privacy concerns introduced
- [ ] Documentation updated (README, CHANGELOG, inline code comments)

---

## Risk Assessment

### Risks Identified

<!-- From plan Section 6 -->

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Risk 1 | High/Med/Low | Mitigation strategy |

### Rollback Plan

<!-- How to safely revert this change -->

**Rollback Steps**:
1. Revert commit or merge revert PR
2. Run: `php artisan migrate:rollback` (if schema changes)
3. Disable feature flag: `feature.flag.name` (if applicable)

---

## Reviewer Notes

<!-- Any important context for reviewers -->

- [ ] This is a breaking change (requires major version bump)
- [ ] This requires deployment coordination
- [ ] This depends on another PR: #[link to dependent PR]

---

## Testing Instructions

### Prerequisites

- [ ] Database migrated to latest
- [ ] Environment configured per `.env.example`
- [ ] Feature flags configured (see Feature Flags section)

### Manual Testing Steps

1. [Describe key user flows to test]
2. [Any edge cases to verify]
3. [Error conditions to confirm]

### Automated Tests

```bash
# Run all tests
php artisan test

# Run specific test file
php artisan test tests/Feature/NewFeatureTest.php

# Run with coverage
php artisan test --coverage
```

---

## Checklist

- [ ] Code review completed
- [ ] Tests passing on CI/CD
- [ ] Documentation complete
- [ ] No console errors or warnings
- [ ] Ready for merge and deployment

