# AI Agent Instructions - Laravel Recipe Manager

This document provides centralized guidelines for all AI coding agents (GitHub Copilot, Claude, and other AI assistants) working on the Laravel Recipe Manager project.

## Purpose

These guidelines ensure AI agents understand the project architecture, coding standards, and development workflow. AI agents should follow these instructions when implementing features, fixes, improvements, and architectural changes.

For human developer information, see `/docs/CONTRIBUTING.md`.

## Project Overview

**Clean Laravel Project**: A modern Laravel 12 recipe management application built with current best practices. The application displays recipes and cookbooks with many-to-many relationships through pivot tables.

**Core Entities**: Recipes, Cookbooks, Classifications, Courses, Meals, and Preparations.

**Tech Stack & Version Requirements**: See `/docs/design/TECH-STACK.md` for comprehensive version requirements, frontend/backend stack details, and architectural patterns.

**Application Architecture**: See `/docs/design/DATA.md` for comprehensive data model, entity relationships, database structure, and migration patterns.

## AI Agent Guidelines

### When Implementing Features
1. Follow Laravel 12 conventions and best practices
2. Use modern Eloquent relationship patterns - access relationships as properties, not through method calls
3. Implement validation using Form Request classes in `app/Http/Requests/`
4. Create Blade templates with Alpine.js interactivity and Tailwind CSS styling
5. Write tests for new features in `tests/Feature/` or `tests/Unit/`
6. Use Laravel Scout or native Eloquent query scopes for search functionality
7. Preserve existing query parameter patterns (`sortField`, `sortOrder`, `displayCount`)

### Code Organization
- **Models**: Place in `app/Models/` with relationships defined as methods
- **Controllers**: Place in `app/Http/Controllers/` with resource-based routing
- **Requests**: Validation logic in `app/Http/Requests/` classes
- **Views**: Create in `resources/views/` with appropriate subdirectories
- **Components**: Reusable UI in `resources/views/components/`
- **Tests**: Feature tests in `tests/Feature/`, unit tests in `tests/Unit/`
- **Migrations**: Database changes in `database/migrations/`

### When Working with Data
- Reference `/docs/design/DATA.md` for entity relationships and constraints
- Use `belongsToMany()` for many-to-many relationships with explicit pivot tables
- Always define `protected $fillable = []` on models for mass assignment
- Include timestamps on models (`public $timestamps = true;`)
- Use foreign key constraints in migrations

### Frontend Implementation
- Use Tailwind CSS 4+ utility classes (no Bootstrap)
- Use Alpine.js 3.x for lightweight interactivity
- Leverage Blade components for reusable UI elements
- Build assets with Vite: `npm run dev` or `npm run build`
- Keep frontend code modern and performant

### Testing & Quality
- Always write tests for new features
- Use PHPUnit 10+ or Pest 2.0+ syntax
- Run tests before considering work complete: `php artisan test`
- Follow Laravel conventions for better maintainability
- Use type hints and meaningful variable names

### Documentation Reference
When uncertain about patterns, check:
1. `/docs/design/DATA.md` - Data model and relationships
2. `/docs/design/TECH-STACK.md` - Technology versions and specifications
3. `/docs/CONTRIBUTING.md` - Developer workflow and setup
4. Existing code in the project - Follow established patterns

### When Creating Migrations
- Use consistent timestamp-based naming: `YYYY_MM_DD_HHMMSS_action.php`
- Define foreign keys with `$table->foreign()` and cascading deletes where appropriate
- Consider pivot tables for many-to-many relationships
- Reference `/docs/design/DATA.md` for expected schema

### Error Handling
- Use Laravel's exception handling patterns
- Return appropriate HTTP status codes
- Provide meaningful error messages for debugging
- Log errors appropriately via `Log` facade

### Performance Considerations
- Use eager loading with `with()` to avoid N+1 queries
- Index frequently queried columns in migrations
- Use query scopes for common filtering patterns
- Leverage caching where appropriate

## Code Quality Standards

### Code Style
- Follow PSR-12 coding standard
- Use meaningful variable and function names
- Keep methods focused and under 50 lines where possible
- Document complex logic with inline comments

### Type Safety
- Use strict types: `declare(strict_types=1);` at the top of all PHP files
- Add return type hints to all methods
- Add parameter type hints to all methods
- Use type unions where appropriate: `int|null`

### Documentation
- Add PHPDoc comments to all classes and public methods
- Document method parameters and return types
- Include usage examples for complex classes
- Keep README and inline docs current with code changes

## Project-Specific Patterns

### Query Parameters
Preserve existing query parameter patterns across controllers:
- `sortField`: Name of field to sort by (e.g., `name`, `date_added`)
- `sortOrder`: Sort direction (`asc` or `desc`)
- `displayCount`: Records per page (`20`, `30`, or `all`)
- `search`: Search query string (for full-text search)

### Model Relationships
- Always use explicit pivot table names in `belongsToMany()` relationships
- Load relationships eagerly with `with()` in controllers
- Define relationship methods in models for reusability
- Use query scopes for common filtering patterns

### Form Validation
- Create dedicated Form Request classes for each action
- Validate both on client-side (Alpine/JavaScript) and server-side (Form Request)
- Provide clear, user-friendly validation error messages
- Reference `/docs/design/DATA.md` for business rule validation

### View Templates
- Use Blade components for reusable UI elements
- Leverage Alpine.js for client-side interactivity
- Build CSS with Tailwind utility classes
- Organize templates by resource: `resources/views/recipes/`, `resources/views/cookbooks/`

## External References

### Legacy Project
The modern Laravel 12 application builds upon patterns from a legacy Laravel 5.2 project. For artifact reuse guidance, see:
- **GitHub**: [github.com/dougis-org/laravel-recipes-update](https://github.com/dougis-org/laravel-recipes-update)
- **Local Reference**: `/home/doug/dev/laravel-recipes-update/`
- **Reuse Guide**: See `/docs/BUILD_PLAN.md` sections on "Legacy Artifact Adaptation Guide"

### Documentation Files
- **BUILD_PLAN.md**: Comprehensive implementation plan with 15 phases
- **BUILD_PLAN_UPDATE_SUMMARY.md**: Summary of artifact reuse percentages
- **DATA.md**: Complete entity relationships and schema documentation
- **TECH-STACK.md**: Technology versions and architectural decisions

## Common Commands

### Development
```bash
# Start development server
php artisan serve

# Watch assets for changes
npm run dev

# Build production assets
npm run build

# Clear application cache
php artisan optimize:clear

# Interactive shell (Tinker)
php artisan tinker
```

### Database
```bash
# Run migrations
php artisan migrate

# Fresh migration with seeding
php artisan migrate:fresh --seed

# Create new migration
php artisan make:migration create_table_name
```

### Testing
```bash
# Run all tests
php artisan test

# Run specific test file
php artisan test tests/Feature/RecipeControllerTest.php

# Run with verbose output
php artisan test --verbose

# Run tests with code coverage
php artisan test --coverage
```

### Code Quality
```bash
# Check code style (if Pint configured)
./vendor/bin/pint

# Run static analysis (if PHPStan configured)
./vendor/bin/phpstan analyse
```

## When in Doubt

1. **Check the codebase first** - Look for similar implementations and follow established patterns
2. **Read the docs** - `/docs/CONTRIBUTING.md`, `/docs/design/DATA.md`, `/docs/design/TECH-STACK.md`
3. **Follow Laravel conventions** - Laravel has excellent documentation at [laravel.com](https://laravel.com)
4. **Ask for clarification** - If requirements are unclear, seek clarification before implementation

## Continuous Improvement

This document is a living guide. As patterns emerge and best practices evolve:
- Document new patterns for team consistency
- Update this file when architectural decisions change
- Keep the build plan and design docs in sync with implementation
- Reference this guide in code reviews to maintain standards
