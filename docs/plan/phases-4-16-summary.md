# Milestones 4-16 - Quick Reference

This document provides a quick breakdown of phases 4-16. For detailed issue breakdowns like phases 0-3, each issue should follow the same pattern with story, acceptance criteria, files, testing, dependencies, and blocks.

---

## Milestone 4 - Search (2-3 issues, 2-3 hours)

**M4-1**: Add Search Scope to Recipe Model
- Add `scopeSearch()` method to Recipe model
- Search on name and ingredients fields
- Test search functionality
- **Depends**: M3-14 | **Blocks**: M5-1

**M4-2**: Test Full-Text Search (MySQL only)
- Test full-text index from M3-13
- Compare performance with LIKE vs full-text
- Document findings
- **Depends**: M3-13

---

## Milestone 5 - Controllers & Routing (8-10 issues, 6-8 hours)

**M5-1**: Create RecipeController with Index Method
- Create controller with index()
- Implement sorting (name, date_added)
- Implement pagination
- Add eager loading
- **Depends**: M3-14, M4-1 | **Blocks**: M7-1

**M5-2**: Add RecipeController Show Method
- Add show() method to controller
- Eager load all relationships
- Handle 404 for missing recipes
- **Depends**: M5-1 | **Blocks**: M7-2

**M5-3**: Create CookbookController with Index
- Create controller with index()
- Load cookbooks with recipe count
- **Depends**: M3-20 | **Blocks**: M8-1

**M5-4**: Add CookbookController Show Method
- Add show() with ordered recipes
- **Depends**: M5-3 | **Blocks**: M8-2

**M5-5**: Create SearchRecipeRequest Form Request
- Validate search parameters
- Rules for sortField, sortOrder, displayCount
- **Depends**: M5-1 | **Blocks**: None

**M5-6**: Define Routes for Recipes
- Resource routes for recipes (index, show)
- **Depends**: M5-1, M5-2 | **Blocks**: M7-1

**M5-7**: Define Routes for Cookbooks
- Resource routes for cookbooks
- **Depends**: M5-3, M5-4 | **Blocks**: M8-1

**M5-8**: Create Default Route Redirect
- Redirect `/` to `/recipes` with default params
- **Depends**: M5-6

**M5-9**: Write Controller Tests
- Feature tests for all controller methods
- Test sorting, pagination, search
- **Depends**: M5-1-M5-4

---

## Milestone 6 - Layout & Components (10-12 issues, 8-10 hours)

**M6-1**: Create Base App Layout
- Update `resources/views/layouts/app.blade.php`
- Include meta tags, Vite directives
- Create content section
- **Depends**: M2-5 | **Blocks**: M6-2-M6-10, M7-1

**M6-2**: Create Button Component
- `resources/views/components/button.blade.php`
- Variants: primary, secondary, danger
- **Depends**: M6-1

**M6-3**: Create Input Component
- Form input with label and error display
- **Depends**: M6-1

**M6-4**: Create Select Component
- Dropdown select with options
- **Depends**: M6-1

**M6-5**: Create Card Component
- Card with header, body, footer slots
- **Depends**: M6-1

**M6-6**: Create Recipe Card Component
- Display recipe summary for grid
- **Depends**: M6-5 | **Blocks**: M7-1

**M6-7**: Create Pagination Component
- Tailwind-styled pagination links
- **Depends**: M6-1 | **Blocks**: M7-1

**M6-8**: Create Sort Controls Component
- Dropdowns for sort field and direction
- **Depends**: M6-4 | **Blocks**: M7-1

**M6-9**: Create Navigation Component
- Header with logo and menu
- Mobile menu structure (interactivity in M9)
- **Depends**: M6-1

**M6-10**: Document Component Library
- Create `docs/COMPONENTS.md`
- Usage examples for each component
- **Depends**: M6-2-M6-9

---

## Milestone 7 - Recipe Views (4-6 issues, 4-6 hours)

**M7-1**: Create Recipe Index View
- Grid layout with search, sort, pagination
- Use recipe card component
- **Depends**: M6-6, M6-7, M6-8, M5-6 | **Blocks**: None

**M7-2**: Create Recipe Show View
- Full recipe display with all fields
- Display relationships (meals, courses, etc.)
- **Depends**: M6-5, M5-2 | **Blocks**: None

**M7-3**: Style Recipe Index with Tailwind
- Responsive grid (1/2/3/4 columns)
- Search form styling
- **Depends**: M7-1

**M7-4**: Style Recipe Show with Tailwind
- Card layout for sections
- Nutrition info display
- **Depends**: M7-2

**M7-5**: Test Recipe Views End-to-End
- Manual testing all view features
- Responsive testing
- **Depends**: M7-1-M7-4

---

## Milestone 8 - Cookbook Views (4-6 issues, 3-4 hours)

**M8-1**: Create Cookbook Index View
- List/grid of cookbooks with recipe counts
- **Depends**: M5-7 | **Blocks**: None

**M8-2**: Create Cookbook Show View
- Display cookbook with ordered recipes
- **Depends**: M5-4, M7-1 (recipe card)

**M8-3**: Style Cookbook Views
- Consistent with recipe views
- **Depends**: M8-1, M8-2

**M8-4**: Test Cookbook Views
- Verify recipe ordering (classification, name)
- **Depends**: M8-1-M8-3

---

## Milestone 9 - Interactivity (6-8 issues, 4-6 hours)

**M9-1**: Add Mobile Menu Toggle
- Alpine.js component for menu
- **Depends**: M6-9, M2-4 | **Blocks**: None

**M9-2**: Add Sort Direction Toggle
- Interactive sort buttons
- **Depends**: M6-8

**M9-3**: Add Display Count Selector
- Dropdown with auto-submit
- **Depends**: M6-4

**M9-4**: Add Search Form Enhancement
- Clear button, active state
- **Depends**: M7-1

**M9-5**: Add Hover Effects to Cards
- Tailwind hover states
- **Depends**: M6-6

**M9-6**: Test All Interactive Features
- Manual testing of Alpine.js features
- **Depends**: M9-1-M9-5

---

## Milestone 10 - Asset Pipeline (4-5 issues, 3-4 hours)

**M10-1**: Optimize Production Build
- Configure Vite for production
- Minification, tree-shaking
- **Depends**: M2-3 | **Blocks**: M16-5

**M10-2**: Test Production Build
- Run `npm run build`
- Verify asset sizes
- **Depends**: M10-1

**M10-3**: Configure Asset Versioning
- Verify manifest.json created
- Test cache busting
- **Depends**: M10-1

**M10-4**: Document Build Process
- Update docs with build commands
- **Depends**: M10-1-M10-3

---

## Milestone 11 - Seeding (10-12 issues, 6-8 hours)

**M11-1**: Create ClassificationSeeder
- Seed common classifications
- **Depends**: M3-15

**M11-2**: Create SourceSeeder
- Seed common sources
- **Depends**: M3-16

**M11-3**: Create MealSeeder
- Seed meal types
- **Depends**: M3-17

**M11-4**: Create PreparationSeeder
- Seed preparation methods
- **Depends**: M3-18

**M11-5**: Create CourseSeeder
- Seed course types
- **Depends**: M3-19

**M11-6**: Create RecipeFactory
- Factory for generating test recipes
- **Depends**: M3-14

**M11-7**: Create CookbookFactory
- Factory for cookbooks
- **Depends**: M3-20

**M11-8**: Update DatabaseSeeder
- Call all seeders in order
- Create test data
- **Depends**: M11-1-M11-7

**M11-9**: Test Seeding
- Run `migrate:fresh --seed`
- Verify data in database and UI
- **Depends**: M11-8

**M11-10**: Create Seeding Documentation
- Document how to seed database
- **Depends**: M11-9

---

## Milestone 12 - Testing (15-20 issues, 12-16 hours)

**M12-1**: Configure Pest/PHPUnit
- Install Pest 2.34+
- Configure test environment
- **Depends**: M1-2

**M12-2**: Create RecipeIndexTest
- Test sorting, pagination, search
- **Depends**: M5-1, M11-8

**M12-3**: Create RecipeShowTest
- Test recipe detail display
- **Depends**: M5-2, M11-8

**M12-4**: Create CookbookIndexTest
- Test cookbook listing
- **Depends**: M5-3, M11-8

**M12-5**: Create CookbookShowTest
- Test recipe ordering in cookbook
- **Depends**: M5-4, M11-8

**M12-6**: Create RecipeModelTest
- Test scopes and relationships
- **Depends**: M3-14

**M12-7**: Create CookbookModelTest
- Test recipe ordering relationship
- **Depends**: M3-20

**M12-8**: Create SearchTest
- Test search scope functionality
- **Depends**: M4-1

**M12-9-12**: Create Tests for All Models
- One test file per model
- **Depends**: M3-15-M3-19

**M12-13**: Test N+1 Query Prevention
- Verify eager loading works
- **Depends**: M5-1, M5-2

**M12-14**: Test Database Transactions
- Test foreign key constraints
- Test cascade deletes
- **Depends**: M3-1-M3-12

**M12-15**: Configure Code Coverage
- Set up coverage reporting
- Target >80% coverage
- **Depends**: M12-1-M12-14

**M12-16**: Run Full Test Suite
- All tests passing
- Coverage report generated
- **Depends**: M12-15

---

## Milestone 13 - Security & Error Handling (12-15 issues, 8-10 hours)

**M13-1**: Configure Security Headers
- CSP, HSTS, X-Frame-Options, etc.
- **Depends**: M1-1

**M13-2**: Implement Rate Limiting
- Configure throttle middleware
- Custom limits for search
- **Depends**: M5-1

**M13-3**: Create Form Request Validation
- Validation for all user inputs
- **Depends**: M5-1

**M13-4**: Verify CSRF Protection
- Test on all forms
- **Depends**: M7-1

**M13-5**: Configure HTTPS Enforcement
- Middleware for production
- **Depends**: M1-4

**M13-6**: Create 404 Error View
- **Depends**: M6-1

**M13-7**: Create 500 Error View
- **Depends**: M6-1

**M13-8**: Create 419 Error View
- **Depends**: M6-1

**M13-9**: Create 429 Error View
- **Depends**: M6-1

**M13-10**: Configure Exception Handler
- Proper logging and error responses
- **Depends**: M1-6

**M13-11**: Set Up Error Monitoring (Optional)
- Install Flare or Sentry
- **Depends**: M1-1

**M13-12**: Security Testing
- Test CSRF, XSS, SQL injection
- **Depends**: M13-1-M13-10

---

## Milestone 14 - Performance & Accessibility (12-15 issues, 10-14 hours)

**M14-1**: Implement WCAG Accessibility
- Alt text, semantic HTML, ARIA labels
- **Depends**: M7-1-M7-4, M8-1-M8-3

**M14-2**: Add Skip Navigation Link
- For keyboard users
- **Depends**: M6-9

**M14-3**: Verify Database Query Performance
- EXPLAIN queries, verify indexes used
- **Depends**: M3-13, M5-1

**M14-4**: Implement Query Result Caching
- Cache classifications, sources, etc.
- **Depends**: M11-1-M11-5

**M14-5**: Optimize Asset Loading
- Verify minification, compression
- **Depends**: M10-1

**M14-6**: Run Lighthouse Audit - Recipe Index
- Target >90 all metrics
- **Depends**: M7-3, M14-1

**M14-7**: Run Lighthouse Audit - Recipe Show
- Target >90 all metrics
- **Depends**: M7-4, M14-1

**M14-8**: Run Lighthouse Audit - Cookbook Pages
- Target >90 all metrics
- **Depends**: M8-3, M14-1

**M14-9**: Browser Compatibility Testing
- Test Chrome, Firefox, Safari, Edge
- **Depends**: M7-1-M8-3

**M14-10**: Responsive Design Testing
- All breakpoints (320px to 2560px)
- **Depends**: M7-3, M8-3

**M14-11**: Performance Benchmark Documentation
- Document actual vs target metrics
- **Depends**: M14-6-M14-10

**M14-12**: Fix Any Performance/Accessibility Issues
- Address findings from audits
- **Depends**: M14-6-M14-10

---

## Milestone 15 - CI/CD Pipeline (8-10 issues, 6-8 hours)

**M15-1**: Create GitHub Actions Workflow
- `.github/workflows/laravel.yml`
- **Depends**: M12-16

**M15-2**: Configure PHPStan
- `phpstan.neon` configuration
- **Depends**: M1-1

**M15-3**: Configure Laravel Pint
- `pint.json` configuration
- **Depends**: M1-1

**M15-4**: Add Pre-commit Hooks (Optional)
- Run linting before commit
- **Depends**: M15-2, M15-3

**M15-5**: Configure Dependabot
- `.github/dependabot.yml`
- **Depends**: M1-1

**M15-6**: Add Code Coverage Reporting
- Codecov or Coveralls
- **Depends**: M12-15

**M15-7**: Configure Deployment Automation
- GitHub Actions or Forge
- **Depends**: M15-1

**M15-8**: Test CI/CD Pipeline
- Create test PR, verify all checks
- **Depends**: M15-1-M15-7

---

## Milestone 16 - Documentation & Deployment (15-18 issues, 10-14 hours)

**M16-1**: Configure Database Backup Strategy
- Install spatie/laravel-backup or manual scripts
- **Depends**: M1-2

**M16-2**: Test Backup and Restore
- Verify backups work
- **Depends**: M16-1

**M16-3**: Create Disaster Recovery Plan
- Document recovery procedures
- **Depends**: M16-2

**M16-4**: Configure Staging Environment
- Separate environment for testing
- **Depends**: M1-1

**M16-5**: Update README.md
- Comprehensive project documentation
- **Depends**: M1-1, M2-6, M14-11

**M16-6**: Create DEVELOPMENT.md
- Development workflow and commands
- **Depends**: All previous milestones

**M16-7**: Create DEPLOYMENT.md
- Deployment procedures and requirements
- **Depends**: M15-7, M16-1

**M16-8**: Create DISASTER_RECOVERY.md
- Recovery procedures
- **Depends**: M16-3

**M16-9**: Create Comprehensive .env.example
- All environment variables documented
- **Depends**: M1-2, M13-11, M16-1

**M16-10**: Test Fresh Installation
- Clone and set up from scratch
- **Depends**: M16-5-M16-9

**M16-11**: Create Production Deployment Checklist
- All deployment requirements
- **Depends**: M16-6-M16-10

**M16-12**: Deploy to Staging
- First deployment test
- **Depends**: M16-4, M16-11

**M16-13**: Run Post-Deployment Verification
- Test all features in staging
- **Depends**: M16-12

**M16-14**: Production Deployment
- Deploy to production environment
- **Depends**: M16-13

**M16-15**: Production Verification
- Verify all features work in production
- **Depends**: M16-14

---

## Effort Summary

| Milestone | Issues | Estimated Hours | Parallel Agents | Completion Time |
|-----------|--------|----------------|-----------------|-----------------|
| M0 | 8 | 2-4 | 6 | 2-4 hours |
| M1 | 6 | 2-3 | 3 | 2-3 hours |
| M2 | 6 | 3-4 | 3 | 3-4 hours |
| M3 | 20 | 8-12 | 6 | 8-12 hours |
| M4 | 2-3 | 2-3 | 2 | 2-3 hours |
| M5 | 8-10 | 6-8 | 3-4 | 6-8 hours |
| M6 | 10-12 | 8-10 | 4-5 | 8-10 hours |
| M7 | 4-6 | 4-6 | 3-4 | 4-6 hours |
| M8 | 4-6 | 3-4 | 2-3 | 3-4 hours |
| M9 | 6-8 | 4-6 | 3-4 | 4-6 hours |
| M10 | 4-5 | 3-4 | 2-3 | 3-4 hours |
| M11 | 10-12 | 6-8 | 4-5 | 6-8 hours |
| M12 | 15-20 | 12-16 | 5-6 | 12-16 hours |
| M13 | 12-15 | 8-10 | 4-5 | 8-10 hours |
| M14 | 12-15 | 10-14 | 4-5 | 10-14 hours |
| M15 | 8-10 | 6-8 | 3-4 | 6-8 hours |
| M16 | 15-18 | 10-14 | 4-5 | 10-14 hours |
| **Total** | **~150-180** | **~90-130** | **5-6** | **80-110 hours** |

**Note**: Completion time with 5-6 parallel agents assumes optimal task distribution and minimal blocking. Actual time will vary based on task dependencies and agent efficiency.
