# Milestone 1 - Project Setup

**Goal**: Initialize Laravel 12 project with proper dependencies and configuration

**Estimated Total Effort**: 4-5 hours (includes project-status.md GitHub Action)
**Can Start**: After M0 complete
**Parallel Capacity**: Limited (mostly sequential tasks with some parallelization)

---

## Issues

### M1-1: Create New Laravel 12 Project
**Type**: `type:setup`
**Priority**: `P1`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M0-1 (PHP), M0-3 (Composer)
**Blocks**: All other M1 issues, M2-1, M3-1

**Description**:
Initialize a new Laravel 12 project using Composer.

**Acceptance Criteria**:
- [ ] Laravel 12 project created using `composer create-project laravel/laravel laravel-recipes-2025`
- [ ] Verify Laravel version is 12.x (`php artisan --version`)
- [ ] Verify PHP version requirement in `composer.json` is `>=8.5.0`
- [ ] Application key generated
- [ ] Storage and bootstrap/cache directories have correct permissions (775)
- [ ] Application boots without errors (`php artisan serve` test)
- [ ] README.md updated with:
  - [ ] Project name and description
  - [ ] PHP and Laravel version requirements
  - [ ] Basic setup instructions

**Files to Create/Modify**:
- `composer.json` (verify/modify)
- `README.md` (update)
- All Laravel default files (created)

**Testing**:
```bash
php artisan --version  # Should show Laravel 12.x
php artisan serve      # Should start without errors
curl http://localhost:8000  # Should return Laravel welcome page
```

**Story**:
```
As a developer
I want to create a new Laravel 12 project
So that I have the foundation for building the recipe manager application
```

---

### M1-2: Configure Database Connection
**Type**: `type:setup`
**Priority**: `P1`
**Effort**: `effort:small` (30 min)
**Depends On**: M1-1 (Laravel project created), M0-4 (Database setup)
**Blocks**: M3-1 (Migrations)

**Description**:
Configure database connection in .env file and verify connectivity.

**Acceptance Criteria**:
- [ ] `.env` file configured with database credentials:
  - [ ] `DB_CONNECTION` set to mysql or pgsql
  - [ ] `DB_HOST` set (default: 127.0.0.1)
  - [ ] `DB_PORT` set (default: 3306 for MySQL, 5432 for PostgreSQL)
  - [ ] `DB_DATABASE` set to `laravel_recipes`
  - [ ] `DB_USERNAME` set
  - [ ] `DB_PASSWORD` set
- [ ] Test database connection verified:
  ```bash
  php artisan db:show  # Should display database info
  ```
- [ ] `.env.example` updated with database configuration template
- [ ] `.env.testing` created for test database:
  - [ ] `DB_DATABASE` set to `laravel_recipes_test`
  - [ ] All other settings match `.env`

**Files to Create/Modify**:
- `.env` (modify)
- `.env.example` (update)
- `.env.testing` (create)

**Testing**:
```bash
php artisan db:show         # Verify connection
php artisan migrate:status  # Should show "No migrations found"
```

**Story**:
```
As a developer
I want to configure the database connection
So that Laravel can communicate with the MySQL/PostgreSQL database
```

---

### M1-3: Initialize Git Repository
**Type**: `type:setup`
**Priority**: `P1`
**Effort**: `effort:small` (15-30 min)
**Depends On**: M1-1 (Laravel project), M0-5 (Git installed)
**Blocks**: None

**Description**:
Initialize Git repository and create initial commit.

**Acceptance Criteria**:
- [ ] Git repository initialized (`git init`)
- [ ] Verified `.gitignore` file exists with Laravel defaults:
  - [ ] `/vendor` excluded
  - [ ] `/node_modules` excluded
  - [ ] `.env` excluded
  - [ ] `/storage` excluded (except .gitkeep files)
  - [ ] `/public/build` excluded
- [ ] All files staged (`git add .`)
- [ ] Initial commit created with message: `chore: initial Laravel 12 project setup`
- [ ] Default branch named `main` (not `master`)
- [ ] Created `docs/git-workflow.md` with:
  - [ ] Branching strategy (trunk-based delivery)
  - [ ] Commit message conventions
  - [ ] PR process

**Files to Create/Modify**:
- `.gitignore` (verify/update)
- `docs/git-workflow.md` (create)

**Testing**:
```bash
git status               # Should show clean working tree
git log                  # Should show initial commit
git branch               # Should show main branch
```

**Story**:
```
As a developer
I want to initialize version control with Git
So that I can track changes and collaborate effectively
```

---

### M1-4: Configure Application Settings
**Type**: `type:setup`
**Priority**: `P2`
**Effort**: `effort:small` (30 min)
**Depends On**: M1-1 (Laravel project)
**Blocks**: None

**Description**:
Configure basic application settings in .env and config files.

**Acceptance Criteria**:
- [ ] `.env` file configured:
  - [ ] `APP_NAME` set to "Laravel Recipes"
  - [ ] `APP_ENV` set to `local`
  - [ ] `APP_DEBUG` set to `true`
  - [ ] `APP_URL` set to development URL
  - [ ] `APP_TIMEZONE` set to appropriate timezone
  - [ ] `APP_LOCALE` set to `en`
- [ ] Verify `config/app.php` settings:
  - [ ] Timezone matches `.env`
  - [ ] Locale is `en`
  - [ ] Fallback locale is `en`
- [ ] Generate application key if not already done
- [ ] Test configuration:
  ```bash
  php artisan config:show app  # Verify settings
  ```

**Files to Create/Modify**:
- `.env` (modify)
- `.env.example` (update)

**Testing**:
```bash
php artisan config:show app  # Verify all settings
php artisan serve            # App should boot with correct name
```

**Story**:
```
As a developer
I want to configure basic application settings
So that the application has the correct name, timezone, and locale
```

---

### M1-5: Verify Project Structure and Create Documentation
**Type**: `type:docs`
**Priority**: `P2`
**Effort**: `effort:small` (30 min)
**Depends On**: M1-1 (Laravel project)
**Blocks**: None

**Description**:
Verify Laravel project structure and create project documentation.

**Acceptance Criteria**:
- [ ] Verified directory structure exists:
  - [ ] `app/Models/`
  - [ ] `app/Http/Controllers/`
  - [ ] `resources/views/`
  - [ ] `database/migrations/`
  - [ ] `database/seeders/`
  - [ ] `database/factories/`
  - [ ] `tests/Feature/`
  - [ ] `tests/Unit/`
- [ ] Created `docs/PROJECT_STRUCTURE.md` with:
  - [ ] Overview of Laravel directory structure
  - [ ] Purpose of each main directory
  - [ ] Where to place different types of files
  - [ ] Naming conventions
- [ ] Created `docs/DEVELOPMENT.md` (initial version) with:
  - [ ] How to start development server
  - [ ] Common artisan commands
  - [ ] Development workflow basics

**Files to Create/Modify**:
- `docs/PROJECT_STRUCTURE.md` (create)
- `docs/DEVELOPMENT.md` (create)

**Testing**: Review documentation for accuracy and completeness

**Story**:
```
As a developer
I want to verify the project structure and have clear documentation
So that I understand where to place different types of files
```

---

### M1-6: Set Up Error Logging and Debugging
**Type**: `type:setup`
**Priority**: `P2`
**Effort**: `effort:small` (30 min)
**Depends On**: M1-1 (Laravel project)
**Blocks**: None

**Description**:
Configure error logging and debugging tools for development.

**Acceptance Criteria**:
- [ ] `.env` logging configuration verified:
  - [ ] `LOG_CHANNEL` set to `stack`
  - [ ] `LOG_LEVEL` set to `debug`
- [ ] Verified `config/logging.php` has appropriate channels configured
- [ ] Created test error log entry:
  ```php
  php artisan tinker
  >>> Log::info('Test log message');
  ```
- [ ] Verified log file created in `storage/logs/laravel.log`
- [ ] `.gitignore` verified to exclude `storage/logs/*.log`
- [ ] Created `docs/DEBUGGING.md` with:
  - [ ] How to view logs
  - [ ] Common debugging techniques
  - [ ] Using `dd()` and `dump()`
  - [ ] Log levels and when to use them

**Files to Create/Modify**:
- `.env` (verify)
- `docs/DEBUGGING.md` (create)

**Testing**:
```bash
php artisan tinker
>>> Log::info('Test message');
>>> exit
cat storage/logs/laravel.log  # Should contain test message
```

**Story**:
```
As a developer
I want error logging and debugging configured
So that I can troubleshoot issues during development
```

---

### M1-7: Set Up Project Status Dashboard GitHub Action
**Type**: `type:setup`
**Priority**: `P2`
**Effort**: `effort:medium` (1-2 hours)
**Depends On**: M1-3 (Git initialized)
**Blocks**: None

**Description**:
Create GitHub Action that generates/updates `docs/project-status.md` whenever a PR is merged or an issue is closed.

**Acceptance Criteria**:
- [ ] Created `.github/workflows/update-project-status.yml`
- [ ] Action triggers on `pull_request` (merged) and `issues` (closed)
- [ ] Generates `docs/project-status.md` with:
  - [ ] Milestone progress (% complete per milestone)
  - [ ] Open/closed issue counts by phase
  - [ ] Critical path status
  - [ ] Velocity trends (last 7 days, 30 days)
  - [ ] Burndown metrics from GitHub API
- [ ] Commits generated file automatically to main
- [ ] Created `docs/project-status.md` template

**Files to Create**:
- `.github/workflows/update-project-status.yml`
- `docs/project-status.md` (template)

**Testing**:
```bash
# Manually trigger workflow after PR merge
gh workflow run update-project-status.yml
```

**Story**:
```
As a project manager
I want automated project status tracking
So that progress is visible without manual updates
```

---

## Summary

**Total Issues**: 7 (now includes M1-7 for project-status.md GitHub Action)
**Can Run in Parallel**: Limited (M1-4, M1-5, M1-6, M1-7 can run after M1-1)
**Critical Path**: M1-1 → M1-2 → M3-1
**Estimated Milestone Completion**: 4-5 hours with 3-4 agents, 8-12 hours solo

**Parallel Execution Strategy**:
- **Agent 1**: M1-1 (Laravel install) → M1-2 (Database config)
- **Agent 2**: Wait for M1-1, then M1-3 (Git init)
- **Agent 3**: Wait for M1-1, then M1-4 (App config)
- **Agent 4**: Wait for M1-1, then M1-5 (Documentation)
- **Agent 5**: Wait for M1-1, then M1-6 (Logging setup)
- **Agent 6**: Wait for M1-3, then M1-7 (GitHub Action setup)

**Dependency Chain**:
```
M0-1, M0-3 → M1-1 → M1-2, M1-3, M1-4, M1-5, M1-6
                   ↓
                  M2-1, M3-1
```

**Success Criteria**:
Laravel 12 project initialized, database connected, Git repository created, basic configuration complete, and documentation in place.
