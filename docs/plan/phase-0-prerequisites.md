# Milestone 0 - Prerequisites

**Goal**: Verify system meets all requirements before starting development

**Estimated Total Effort**: 3-5 hours (includes GitHub setup)
**Can Start**: Immediately
**Parallel Capacity**: Up to 6 agents (all tasks independent)

---

## Issues

### M0-1 (#224): Verify PHP Installation and Extensions ⚡
**Type**: `type:setup`
**Priority**: `P1`
**Effort**: `effort:small` (30-60 min)
**Depends On**: None
**Blocks**: M1-1 (Laravel installation)

**Description**:
Verify PHP 8.5+ is installed with all required extensions for Laravel 12.

**Acceptance Criteria**:
- [ ] PHP version 8.5 or higher verified (`php -v`)
- [ ] All required extensions installed and verified (`php -m`):
  - [ ] pdo, pdo_mysql (or pdo_pgsql)
  - [ ] mbstring, xml, bcmath
  - [ ] curl, tokenizer, json, openssl
  - [ ] fileinfo, gd
- [ ] Created documentation file: `docs/setup/php-setup.md` with:
  - [ ] Installed PHP version
  - [ ] List of installed extensions
  - [ ] Installation commands used (if any)
  - [ ] Platform-specific notes (Ubuntu/macOS/Windows)

**Files to Create/Modify**:
- `docs/setup/php-setup.md` (create)

**Testing**: Manual verification of PHP version and extensions

**Story**:
```
As a developer
I want to verify PHP 8.5+ is installed with all required extensions
So that Laravel 12 can run without errors
```

---

### M0-2 (#225): Verify Node.js and npm Installation ⚡
**Type**: `type:setup`
**Priority**: `P1`
**Effort**: `effort:small` (30-60 min)
**Depends On**: None
**Blocks**: M2-1 (Frontend package installation)

**Description**:
Verify Node.js 25+ and npm are installed for frontend tooling.

**Acceptance Criteria**:
- [ ] Node.js version 25 or higher verified (`node -v`)
- [ ] npm version 10 or higher verified (`npm -v`)
- [ ] Created documentation file: `docs/setup/nodejs-setup.md` with:
  - [ ] Installed Node.js version
  - [ ] Installed npm version
  - [ ] Installation method used (nvm/brew/installer)
  - [ ] Platform-specific notes

**Files to Create/Modify**:
- `docs/setup/nodejs-setup.md` (create)

**Testing**: Manual verification of Node.js and npm versions

**Story**:
```
As a developer
I want to verify Node.js 25+ and npm are installed
So that I can use Vite for frontend asset compilation
```

---

### M0-3 (#223): Verify Composer Installation ⚡
**Type**: `type:setup`
**Priority**: `P1`
**Effort**: `effort:small` (15-30 min)
**Depends On**: None
**Blocks**: M1-1 (Laravel installation)

**Description**:
Verify Composer 2.7+ is installed for PHP dependency management.

**Acceptance Criteria**:
- [ ] Composer version 2.7 or higher verified (`composer -V`)
- [ ] Composer updated to latest if needed (`composer self-update`)
- [ ] Created documentation file: `docs/setup/composer-setup.md` with:
  - [ ] Installed Composer version
  - [ ] Installation method
  - [ ] Update procedure

**Files to Create/Modify**:
- `docs/setup/composer-setup.md` (create)

**Testing**: Manual verification of Composer version

**Story**:
```
As a developer
I want to verify Composer 2.7+ is installed
So that I can install Laravel 12 and its dependencies
```

---

### M0-4 (#218): Set Up and Verify Database Server ⚡
**Type**: `type:setup`
**Priority**: `P1`
**Effort**: `effort:medium` (1-2 hours)
**Depends On**: None
**Blocks**: M1-2 (Database configuration), M3-1 (Run migrations)

**Description**:
Set up MySQL 8.0+ or PostgreSQL 14+ database server and create application database.

**Acceptance Criteria**:
- [ ] Database server installed and running (MySQL 8.0+ OR PostgreSQL 14+)
- [ ] Database version verified (`mysql --version` or `psql --version`)
- [ ] Database server is running and accessible
- [ ] Created database: `laravel_recipes` with UTF8MB4 encoding
- [ ] Created database user with appropriate permissions
- [ ] Test database: `laravel_recipes_test` created for testing
- [ ] Created documentation file: `docs/setup/database-setup.md` with:
  - [ ] Database type and version
  - [ ] Database name and test database name
  - [ ] User permissions granted
  - [ ] Connection parameters (host, port)
  - [ ] Backup of credentials template

**Files to Create/Modify**:
- `docs/setup/database-setup.md` (create)

**Testing**:
- Connect to database successfully
- Verify permissions by creating/dropping a test table

**Story**:
```
As a developer
I want to have a MySQL 8.0+ or PostgreSQL 14+ database server running
So that Laravel can store and retrieve application data
```

---

### M0-5 (#219): Verify Git Installation and Configuration ⚡
**Type**: `type:setup`
**Priority**: `P1`
**Effort**: `effort:small` (15-30 min)
**Depends On**: None
**Blocks**: M1-3 (Git initialization)

**Description**:
Verify Git is installed and configured with user identity.

**Acceptance Criteria**:
- [ ] Git version 2.30+ verified (`git --version`)
- [ ] Git user name configured (`git config --global user.name`)
- [ ] Git user email configured (`git config --global user.email`)
- [ ] Git configuration verified (`git config --list`)
- [ ] Created documentation file: `docs/setup/git-setup.md` with:
  - [ ] Git version
  - [ ] Configuration settings
  - [ ] Branching strategy notes (trunk-based delivery)

**Files to Create/Modify**:
- `docs/setup/git-setup.md` (create)

**Testing**: Create a test repository and commit to verify configuration

**Story**:
```
As a developer
I want to verify Git is installed and configured
So that I can version control my code and follow trunk-based delivery
```

---

### M0-6 (#220): Choose and Configure Development Environment ⚡
**Type**: `type:setup`
**Priority**: `P2`
**Effort**: `effort:medium` (1-2 hours)
**Depends On**: M0-1 (PHP installed), M0-2 (Node.js installed)
**Blocks**: M1-1 (Laravel serve)

**Description**:
Set up local development server (Laravel Valet, Herd, or artisan serve).

**Acceptance Criteria**:
- [ ] Development environment chosen and installed
  - [ ] Laravel Valet (macOS) OR
  - [ ] Laravel Herd (cross-platform) OR
  - [ ] `php artisan serve` documented
- [ ] Test server can be started and accessed
- [ ] HTTPS capability verified (if using Valet/Herd)
- [ ] Created documentation file: `docs/setup/dev-environment.md` with:
  - [ ] Environment choice and rationale
  - [ ] Installation steps
  - [ ] How to start/stop server
  - [ ] Default URL (http://localhost:8000 or custom)
  - [ ] Troubleshooting common issues

**Files to Create/Modify**:
- `docs/setup/dev-environment.md` (create)

**Testing**:
- Start development server
- Access test page in browser
- Verify HTTPS (if applicable)

**Story**:
```
As a developer
I want to have a local development server configured
So that I can run and test the Laravel application locally
```

---

### M0-7 (#221): Configure Code Editor with Extensions ⚡
**Type**: `type:setup`
**Priority**: `P3`
**Effort**: `effort:small` (30-60 min)
**Depends On**: None
**Blocks**: None

**Description**:
Set up code editor (VS Code or PhpStorm) with recommended extensions.

**Acceptance Criteria**:
- [ ] Code editor installed (VS Code, PhpStorm, or other)
- [ ] PHP language support installed
- [ ] Blade syntax highlighting installed
- [ ] Tailwind CSS IntelliSense installed
- [ ] EditorConfig configured for consistent formatting
- [ ] Created `.editorconfig` file in project root with Laravel standards
- [ ] Created documentation file: `docs/setup/editor-setup.md` with:
  - [ ] Editor choice
  - [ ] List of installed extensions
  - [ ] Extension settings/configuration
  - [ ] Keyboard shortcuts (optional)

**Files to Create/Modify**:
- `.editorconfig` (create)
- `docs/setup/editor-setup.md` (create)

**Testing**: Open a PHP file and verify syntax highlighting works

**Story**:
```
As a developer
I want my code editor configured with appropriate extensions
So that I have autocomplete, syntax highlighting, and consistent formatting
```

---

### M0-8 (#222): Document System Specifications
**Type**: `type:docs`
**Priority**: `P3`
**Effort**: `effort:small` (30 min)
**Depends On**: M0-1, M0-2, M0-3, M0-4, M0-5, M0-6
**Blocks**: None

**Description**:
Create comprehensive documentation of system specifications and setup.

**Acceptance Criteria**:
- [ ] Created documentation file: `docs/setup/system-specs.md` with:
  - [ ] Operating system and version
  - [ ] PHP version and extensions
  - [ ] Node.js and npm versions
  - [ ] Composer version
  - [ ] Database type and version
  - [ ] Git version
  - [ ] Development environment choice
  - [ ] Code editor and extensions
  - [ ] RAM and disk space available
  - [ ] CPU information
- [ ] Consolidated README in `docs/setup/README.md` linking to all setup docs

**Files to Create/Modify**:
- `docs/setup/system-specs.md` (create)
- `docs/setup/README.md` (create)

**Testing**: Review documentation for completeness

**Story**:
```
As a developer
I want comprehensive documentation of my system setup
So that I can reproduce the environment or troubleshoot issues
```

---

## Summary

**Total Issues**: 8
**Can Run in Parallel**: All 8 (with M0-6 starting after M0-1 and M0-2)
**Critical Path**: M0-1, M0-3 → M1-1 (Laravel installation)
**Estimated Milestone Completion**: 3-5 hours with 6 agents, 12-16 hours solo

**Parallel Execution Strategy**:
- **Agent 1**: M0-1 (PHP) → M0-6 (Dev Environment)
- **Agent 2**: M0-2 (Node.js)
- **Agent 3**: M0-3 (Composer)
- **Agent 4**: M0-4 (Database)
- **Agent 5**: M0-5 (Git)
- **Agent 6**: M0-7 (Editor)
- **Agent 1-6** (any available): M0-8 (Documentation)

**Success Criteria**:
All prerequisite tools installed, verified, and documented. System ready for Laravel 12 project initialization.
