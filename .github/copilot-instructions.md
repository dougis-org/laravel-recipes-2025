# Laravel Recipe Manager - AI Coding Agent Instructions

## Purpose

This document provides AI coding agents with guidelines for implementing features, fixes, and improvements in the Laravel Recipe Manager project. For human developer information, see `/docs/CONTRIBUTING.md`.

## Project Overview
**Clean Laravel Project**: A modern Laravel 12 recipe management application built with current best practices. The application displays recipes and cookbooks with many-to-many relationships through pivot tables. Core entities: **Recipes**, **Cookbooks**, **Classifications**, **Courses**, **Meals**, and **Preparations**.

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
