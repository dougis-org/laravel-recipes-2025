# Laravel Recipe Manager - Clean Build Implementation Plan

## Overview

This plan details building a modern Laravel 12 Recipe Manager application from scratch using current best practices. The application displays recipes and cookbooks with many-to-many relationships through explicit pivot tables. The architecture mirrors the functionality of the legacy Laravel 5.2 app while adopting contemporary Laravel patterns, frontend technologies, and code organization.

**Key Goals**:
- Modern Laravel 12 conventions throughout (no legacy patterns)
- Clean, maintainable codebase built for extensibility
- Contemporary frontend user experience (Tailwind CSS 4+, Alpine.js 3)
- Preserved data model and relationships from legacy app
- Zero technical debt

---

## Architecture Overview

### Tech Stack & Version Requirements

**Required Versions** (Locked for consistency):
- **PHP**: `>=8.5.0` (latest stable with type safety, attributes, match expressions)
- **Laravel**: `^12.0` (latest major version)
- **Node.js**: `>=25.0.0` (for Vite and build tools)
- **Composer**: `^2.7` (PHP dependency manager)

**Backend Dependencies**:
- **Laravel Framework**: `^12.0`
- **Eloquent ORM**: Included with Laravel
- **Guzzle HTTP**: `^7.8` (HTTP client)

**Frontend Dependencies**:
- **Tailwind CSS**: `^4.0.0` (utility-first CSS framework)
- **Alpine.js**: `^3.14.0` (lightweight reactive framework)
- **PostCSS**: `^8.4` (CSS processing)
- **Autoprefixer**: `^10.4` (vendor prefix automation)

**Build Tools**:
- **Vite**: `^5.0` (modern, fast asset compilation with HMR)
- **Laravel Vite Plugin**: `^1.0`

**Database**:
- **MySQL**: `>=8.0` OR **PostgreSQL**: `>=14.0`
- **Database Driver**: `pdo_mysql` or `pdo_pgsql`

**Testing**:
- **Pest**: `^2.34` (recommended - modern syntax) OR **PHPUnit**: `^10.5`
- **Laravel Dusk**: `^7.0` (optional - browser testing)

**Development Tools**:
- **Laravel Pint**: `^1.13` (code style fixer - PSR-12)
- **PHPStan**: `^1.10` (optional - static analysis)
- **Laravel Debugbar**: `^3.9` (optional - query debugging)

**Required PHP Extensions**:
- `pdo`, `pdo_mysql` (or `pdo_pgsql`)
- `mbstring`, `xml`, `bcmath`, `curl`
- `tokenizer`, `json`, `openssl`
- `fileinfo`, `gd` (for image handling)

**Browser Support**:
- Chrome/Edge: Last 2 versions
- Firefox: Last 2 versions
- Safari: Last 2 versions
- Mobile Safari (iOS): Last 2 versions
- Chrome Mobile (Android): Last 2 versions

### Project Structure
```
app/
├── Models/
│   ├── Recipe.php
│   ├── Cookbook.php
│   ├── Classification.php
│   ├── Source.php
│   ├── Meal.php
│   ├── Preparation.php
│   └── Course.php
├── Http/
│   ├── Controllers/
│   │   ├── RecipeController.php
│   │   └── CookbookController.php
│   └── Requests/
│       ├── SearchRecipeRequest.php
│       └── ...
├── Exceptions/
│   └── Handler.php
└── ...
resources/
├── views/
│   ├── layouts/
│   │   └── app.blade.php
│   ├── components/
│   │   ├── button.blade.php
│   │   ├── input.blade.php
│   │   ├── card.blade.php
│   │   └── ...
│   ├── recipes/
│   │   ├── index.blade.php
│   │   └── show.blade.php
│   └── cookbooks/
│       ├── index.blade.php
│       └── show.blade.php
├── css/
│   └── app.css
└── js/
    └── app.js
database/
├── migrations/
│   ├── 2024_01_01_000000_create_classifications_table.php
│   ├── 2024_01_01_000001_create_sources_table.php
│   ├── 2024_01_01_000002_create_recipes_table.php
│   ├── 2024_01_01_000003_create_meals_table.php
│   ├── 2024_01_01_000004_create_preparations_table.php
│   ├── 2024_01_01_000005_create_courses_table.php
│   ├── 2024_01_01_000006_create_cookbooks_table.php
│   ├── 2024_01_01_000007_create_recipe_meals_table.php
│   ├── 2024_01_01_000008_create_recipe_preparations_table.php
│   ├── 2024_01_01_000009_create_recipe_courses_table.php
│   └── 2024_01_01_000010_create_cookbook_recipes_table.php
├── seeders/
│   ├── DatabaseSeeder.php
│   ├── ClassificationSeeder.php
│   ├── SourceSeeder.php
│   └── ...
└── factories/
    └── RecipeFactory.php
tests/
├── Feature/
│   ├── RecipeIndexTest.php
│   ├── RecipeShowTest.php
│   ├── CookbookIndexTest.php
│   └── CookbookShowTest.php
└── Unit/
    ├── RecipeModelTest.php
    └── CookbookModelTest.php
```

---

## Reusable Artifacts from Legacy App

**GitHub Repository**: [laravel-recipes-update](https://github.com/dougis-org/laravel-recipes-update)

The legacy Laravel 5.2 application contains proven implementations that can be adapted for the modern Laravel 12 application. All artifacts are version-controlled and publicly accessible.

### Complete List of Reusable Items

| Artifact | GitHub Path | Reusable As-Is | Notes |
|----------|----------|---|---|
| **Migrations (19 total)** | [`database/migrations/`](https://github.com/dougis-org/laravel-recipes-update/tree/main/database/migrations) | ~80% | Modernize syntax; consolidate foreign keys; update data types |
| **Models (7 core)** | [`app/Models/`](https://github.com/dougis-org/laravel-recipes-update/tree/main/app/Models) | ~70% | Remove Eloquence trait; update relationship syntax; add query scopes |
| **Controllers (2)** | [`app/Http/Controllers/`](https://github.com/dougis-org/laravel-recipes-update/tree/main/app/Http/Controllers) | ~60% | Update for modern Laravel; preserve sorting/search logic; add eager loading |
| **Views (recipe/cookbook)** | [`resources/views/recipe/`](https://github.com/dougis-org/laravel-recipes-update/tree/main/resources/views/recipe), [`resources/views/cookbook/`](https://github.com/dougis-org/laravel-recipes-update/tree/main/resources/views/cookbook) | ~40% | Layout/logic reusable; completely restyle with Tailwind CSS |
| **Search Logic** | [RecipeController.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/app/Http/Controllers/RecipeController.php) | ~50% | Adapt from `search()` method; replace Eloquence with native scopes |
| **Pagination/Sort Logic** | [RecipeController.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/app/Http/Controllers/RecipeController.php) | ~90% | Query parameter handling logic directly applicable |
| **Cookbook Recipe Ordering** | [Cookbook.php model](https://github.com/dougis-org/laravel-recipes-update/blob/main/app/Models/Cookbook.php) | ~95% | Already uses correct join approach; minimal updates needed |
| **Data Schema** | [migrations](https://github.com/dougis-org/laravel-recipes-update/tree/main/database/migrations) | 100% | Schema proven and correct; just modernize syntax |

### What to Build From Scratch
- **Frontend Components**: Tailwind CSS 4 components (no Bootstrap equivalent in legacy app)
- **Alpine.js Interactivity**: Mobile menu, sort toggles (legacy app uses minimal JS)
- **Modern Blade Layout**: Legacy uses Foundation; build modern header/footer/layout
- **Error Views**: Not present in legacy app
- **Tests**: Build comprehensive test suite (legacy has minimal tests)

---

## Phase 0: Prerequisites & System Requirements

**Goals**: Verify system meets all requirements before starting development

### Tasks

1. **Verify PHP Version and Extensions**
   - Check PHP version: `php -v` (must be >=8.5.0)
   - Check installed extensions: `php -m`
   - Required extensions: pdo, pdo_mysql, mbstring, xml, bcmath, curl, tokenizer, json, openssl, fileinfo, gd
   - Install missing extensions:
     - Ubuntu/Debian: `sudo apt install php8.5-{ext-name}`
     - macOS: `brew install php@8.5` (includes most extensions)
     - Windows: Enable in `php.ini`

2. **Verify Node.js and npm**
   - Check Node version: `node -v` (must be >=25.0.0)
   - Check npm version: `npm -v` (should be >=10.0.0)
   - Install/update if needed:
     - Using nvm: `nvm install 25 && nvm use 25`
     - macOS: `brew install node@25`
     - Windows: Download from nodejs.org

3. **Verify Composer**
   - Check Composer version: `composer -V` (must be >=2.7)
   - Update if needed: `composer self-update`
   - Install if missing: https://getcomposer.org/download/

4. **Verify Database**
   - MySQL: `mysql --version` (must be >=8.0)
   - OR PostgreSQL: `psql --version` (must be >=14.0)
   - Verify database server is running
   - Create database: `CREATE DATABASE laravel_recipes CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
   - Create database user with appropriate permissions

5. **Install Git**
   - Check Git version: `git --version` (>=2.30 recommended)
   - Configure Git identity:
     ```bash
     git config --global user.name "Your Name"
     git config --global user.email "your.email@example.com"
     ```

6. **Development Environment Setup**
   - Choose local server option:
     - Laravel Valet (macOS) - recommended for Mac
     - Laravel Herd (macOS/Windows) - recommended cross-platform
     - `php artisan serve` - built-in PHP server
     - Docker with Laravel Sail - containerized environment
   - Verify HTTPS capability (required for modern browser features)

7. **Code Editor Setup** (Recommended)
   - Install VS Code, PhpStorm, or preferred IDE
   - Install PHP language support and Blade syntax highlighting
   - Install Tailwind CSS IntelliSense extension
   - Configure EditorConfig for consistent formatting

8. **Performance Verification**
   - Verify system has adequate resources:
     - RAM: 4GB minimum, 8GB+ recommended
     - Disk space: 2GB minimum for project
     - CPU: Multi-core processor recommended for build tools

**Success Criteria**:
- ✅ PHP 8.5+ installed with all required extensions
- ✅ Node.js 25+ and npm installed
- ✅ Composer 2.7+ installed
- ✅ Database server (MySQL 8.0+ or PostgreSQL 14+) running
- ✅ Git installed and configured
- ✅ Development environment ready (Valet/Herd/artisan serve)
- ✅ All system requirements met and verified

---

## Phase 1: Project Setup & Configuration

**Goals**: Initialize Laravel 12 project with proper dependencies and configuration

### Tasks

1. **Initialize Laravel 12 Project**
   - Command: `laravel new recipe-manager`
   - Verify PHP version requirement (8.5+) in `composer.json`

2. **Configure Database Connection**
   - Set `.env` file with database credentials (MySQL/PostgreSQL)
   - Ensure `DB_CONNECTION`, `DB_HOST`, `DB_PORT`, `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD` are set

3. **Initialize Version Control**
   - Initialize git repository
   - Create `.gitignore` (Laravel defaults)
   - Create initial commit

4. **Review Application Structure**
   - Verify `app/Models/`, `app/Http/Controllers/`, `resources/views/` directories exist
   - Check `config/app.php` for timezone and locale settings

**Success Criteria**:
- ✅ Project boots without errors: `php artisan serve`
- ✅ Database connection verified: `php artisan migrate` (should succeed or indicate no migrations)
- ✅ `.env` file properly configured

---

## Phase 2: Frontend Stack Configuration

**Goals**: Set up modern frontend build pipeline with Tailwind CSS 4+ and Alpine.js 3

### Tasks

5. **Install and Configure Vite**
   - Laravel 12 includes Vite by default
   - Verify `vite.config.js` is present and properly configured with Laravel plugin
   - Check `resources/views/app.blade.php` includes Vite directives: `@vite(['resources/css/app.css', 'resources/js/app.js'])`

6. **Install Tailwind CSS 4+**
   - Command: `npm install -D tailwindcss@latest postcss autoprefixer`
   - Create/update `tailwind.config.js`:
     ```javascript
     export default {
       content: [
         "./resources/views/**/*.blade.php",
         "./resources/js/**/*.js",
       ],
       theme: {
         extend: {},
       },
       plugins: [],
     }
     ```
   - Create/update `postcss.config.js`:
     ```javascript
     export default {
       plugins: {
         tailwindcss: {},
         autoprefixer: {},
       },
     }
     ```

7. **Configure Tailwind CSS in Asset Files**
   - Update `resources/css/app.css`:
     ```css
     @tailwind base;
     @tailwind components;
     @tailwind utilities;
     ```

8. **Install Alpine.js 3.x**
   - Command: `npm install alpinejs@latest`
   - Update `resources/js/app.js`:
     ```javascript
     import Alpine from 'alpinejs'
     window.Alpine = Alpine
     Alpine.start()
     ```

9. **Configure Package Scripts**
   - Update `package.json` scripts:
     ```json
     "scripts": {
       "dev": "vite",
       "build": "vite build"
     }
     ```

10. **Test Frontend Build Pipeline**
    - Run: `npm run dev` (verify Vite server starts)
    - Run: `npm run build` (verify assets compile to `public/build/`)
    - Verify no CSS or JS errors in browser console

**Success Criteria**:
- ✅ `npm run dev` starts Vite dev server without errors
- ✅ `npm run build` compiles assets successfully
- ✅ `@vite` directives in Blade templates load correctly
- ✅ Tailwind CSS classes work in browser (e.g., `bg-blue-500`)
- ✅ Alpine.js loads without errors (check browser console)

---

## Phase 3: Database Schema & Models

**Goals**: Create database schema and Eloquent models reflecting the data model

### Base Artifacts Available
- **Existing Migrations**: Available at [`database/migrations/`](https://github.com/dougis-org/laravel-recipes-update/tree/main/database/migrations) in the legacy repo - These migrations can be largely reused or adapted (see details below for Laravel 12 updates needed)
- **Existing Models**: Available at [`app/Models/`](https://github.com/dougis-org/laravel-recipes-update/tree/main/app/Models) in the legacy repo - Provide good foundation, require modernization (remove Eloquence trait, update relationship syntax)
- **Schema**: Legacy app has proven schema that works; we'll adapt it to modern Laravel conventions

### Migration Adaptation Strategy
The legacy app has 19 migrations created with Laravel 5.2 syntax. We'll adapt these for Laravel 12 by:
1. Updating migration class names and method signatures to modern syntax
2. Removing deprecated migration methods
3. Adding proper index and foreign key definitions inline (not in separate migrations)
4. Consolidating where possible while maintaining schema integrity
5. Using modern Blueprint methods (e.g., `$table->id()` instead of `$table->integer('id', true)`)

### Tasks

11. **Create/Adapt Migrations** (in order by timestamp)
    - **Source**: Adapt from [laravel-recipes-update/database/migrations/](https://github.com/dougis-org/laravel-recipes-update/tree/main/database/migrations)
    - **Approach**: Modernize existing migrations rather than rebuild from scratch
    
    Tables to create (adapted from legacy app):
    
    a. **2025_01_01_000001_create_classifications_table.php**
       - Source: [2015_12_21_233545_create_classifications_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_classifications_table.php)
       - Modernize: Use `$table->id()`, `$table->string('name')->unique()`, `$table->timestamps()`
    
    b. **2025_01_01_000002_create_sources_table.php**
       - Source: [2015_12_21_233545_create_sources_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_sources_table.php)
       - Modernize: Use modern Blueprint methods
    
    c. **2025_01_01_000003_create_recipes_table.php**
       - Source: [2015_12_21_233545_create_recipes_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_recipes_table.php)
       - Update: Change `string` columns to `text` where appropriate (ingredients, instructions, notes)
       - Update: Change nutrition columns from string to decimal/float
       - Update: Add inline foreign key definitions for classification_id, source_id
       - Key columns: id, name (unique), ingredients (text), instructions (text), notes (text, nullable), servings (int, nullable), classification_id, source_id, date_added (dateTime), calories (decimal), fat (decimal), cholesterol (decimal), sodium (decimal), protein (decimal), marked (boolean), timestamps
    
    d. **2025_01_01_000004_create_meals_table.php**
       - Source: [2015_12_21_233545_create_meals_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_meals_table.php)
       - Modernize: Use modern Blueprint methods
    
    e. **2025_01_01_000005_create_preparations_table.php**
       - Source: [2015_12_21_233545_create_preparations_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_preparations_table.php)
       - Modernize: Use modern Blueprint methods
    
    f. **2025_01_01_000006_create_courses_table.php**
       - Source: [2015_12_21_233545_create_courses_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_courses_table.php)
       - Modernize: Use modern Blueprint methods
    
    g. **2025_01_01_000007_create_cookbooks_table.php**
       - Source: [2015_12_21_233545_create_cookbooks_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_cookbooks_table.php)
       - Modernize: Use modern Blueprint methods
    
    h. **2025_01_01_000008_create_recipe_meals_table.php**
       - Source: [2015_12_21_233545_create_recipe_meals_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_recipe_meals_table.php)
       - Update: Add inline foreign keys with cascading deletes
    
    i. **2025_01_01_000009_create_recipe_preparations_table.php**
       - Source: [2015_12_21_233545_create_recipe_preparations_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_recipe_preparations_table.php)
       - Update: Add inline foreign keys with cascading deletes
    
    j. **2025_01_01_000010_create_recipe_courses_table.php**
       - Source: [2015_12_21_233545_create_recipe_courses_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_recipe_courses_table.php)
       - Update: Add inline foreign keys with cascading deletes
    
    k. **2025_01_01_000011_create_cookbook_recipes_table.php**
       - Source: [2015_12_21_233545_create_cookbook_recipes_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_cookbook_recipes_table.php)
       - Update: Add inline foreign keys with cascading deletes

    Command: `php artisan migrate`
    
    **Migration Modernization Details**:
    - Replace `class ClassName extends Migration` with modern syntax
    - Use `Schema::create()` with closure instead of `Schema::create('table', function(Blueprint $table){})`
    - Use `$table->id()` instead of `$table->integer('id', true)`
    - Use `$table->foreignId('model_id')->constrained()->cascadeOnDelete()` instead of separate foreign key calls
    - Remove deprecated index() methods; use `->index()` inline on columns
    - Ensure all required foreign keys and constraints are defined

12. **Add Database Indexes for Performance**
    - Create migration: `2025_01_01_000012_add_database_indexes.php`
    - Add indexes for frequently queried columns:
      ```php
      Schema::table('recipes', function (Blueprint $table) {
          // Single column indexes
          $table->index('name');
          $table->index('date_added');
          $table->index('classification_id');
          $table->index('source_id');
          $table->index('marked');

          // Compound indexes for common query patterns
          $table->index(['classification_id', 'name']); // Sorted by classification
          $table->index(['source_id', 'name']); // Recipes by source
          $table->index(['date_added', 'id']); // Pagination optimization

          // Full-text index for search (MySQL only)
          $table->fullText(['name', 'ingredients']);
      });

      Schema::table('cookbooks', function (Blueprint $table) {
          $table->index('name');
      });

      // Pivot table indexes
      Schema::table('cookbook_recipes', function (Blueprint $table) {
          $table->index('cookbook_id');
          $table->index('recipe_id');
          $table->index(['cookbook_id', 'recipe_id']); // Prevent duplicates
      });

      Schema::table('recipe_meals', function (Blueprint $table) {
          $table->index(['recipe_id', 'meal_id']);
      });

      Schema::table('recipe_preparations', function (Blueprint $table) {
          $table->index(['recipe_id', 'preparation_id']);
      });

      Schema::table('recipe_courses', function (Blueprint $table) {
          $table->index(['recipe_id', 'course_id']);
      });
      ```
    - **Note**: Full-text indexes only work on MyISAM or InnoDB (MySQL 5.6+)
    - For PostgreSQL, consider using GIN indexes for search

13. **Create/Modernize Eloquent Models** (in `app/Models/`)
    - **Source**: Adapt from [legacy app Models](https://github.com/dougis-org/laravel-recipes-update/tree/main/app/Models) (all 7 models exist)
    - **Approach**: Remove Eloquence trait, modernize relationship syntax, adapt to Laravel 12 conventions
    
    a. **Recipe.php**
       - Source: [Recipe.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/app/Models/Recipe.php)
       - Remove: `Sofa\Eloquence\Eloquence` trait
       - Update relationships: Change `getSource()` → `source()`, `getClassification()` → `classification()`
       - Use modern syntax: `$this->belongsTo(Source::class)` instead of `$this->hasOne('App\Models\Source')`
       - Update searchable: Replace Eloquence trait with native query scope `scopeSearch()`
       - Keep fillable array as-is
       - Add query scopes: `scopeOrderByDateAdded()`, `scopeOrderByName()`, `scopeSearch($query, $term)`
       - Relationships: source (belongsTo), classification (belongsTo), meals (belongsToMany), preparations (belongsToMany), courses (belongsToMany), cookbooks (belongsToMany)
    
    b. **Classification.php**
       - Source: [Classification.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/app/Models/Classification.php)
       - Remove: `getName()` and `setName()` methods (Laravel accessors/mutators if needed)
       - Keep: Simple model with timestamps and fillable
       - Add relationship: `recipes()` (hasMany)
    
    c. **Source.php**
       - Source: [Source.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/app/Models/Source.php) (if exists, otherwise create)
       - Create: Similar to Classification with `recipes()` hasMany relationship
       - Keep: Simple model with timestamps and fillable
    
    d. **Cookbook.php**
       - Source: [Cookbook.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/app/Models/Cookbook.php)
       - Remove: `getName()` and `setName()` methods
       - Update: Keep recipes relationship with leftJoin and orderBy for classification.name, then recipes.name
       - Already uses modern belongsToMany syntax (good pattern to follow)
    
    e. **Meal.php**
       - Source: [Meal.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/app/Models/Meal.php) (if exists, otherwise create)
       - Create: Simple model with timestamps, fillable, and `recipes()` belongsToMany relationship
    
    f. **Preparation.php**
       - Source: [Preparation.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/app/Models/Preparation.php) (if exists, otherwise create)
       - Create: Simple model with timestamps, fillable, and `recipes()` belongsToMany relationship
    
    g. **Course.php**
       - Source: [Course.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/app/Models/Course.php) (if exists, otherwise create)
       - Create: Simple model with timestamps, fillable, and `recipes()` belongsToMany relationship

**Success Criteria**:
- ✅ All migrations run without errors: `php artisan migrate`
- ✅ Models created with proper relationships
- ✅ Model relationships load correctly in Tinker: `php artisan tinker` → `Recipe::with('classification', 'source')->first()`
- ✅ Pivot relationships work: `$recipe->meals()` returns correct data

---

## Phase 4: Search Implementation

**Goals**: Enable recipe search by name and ingredients

### Base Artifacts Available
- **Legacy Search Implementation**: The legacy app uses `Sofa\Eloquence` trait with `protected $searchableColumns = ['name', 'ingredients']` in Recipe model
- **Strategy**: Replace Eloquence trait with native Eloquent query scope for simplicity and fewer dependencies

### Tasks

13. **Implement Search via Query Scope** (no external dependencies)
    - Add to `Recipe` model: `scopeSearch($query, $term)` method
    - Implementation:
      ```php
      public function scopeSearch($query, $term)
      {
          return $query->where('name', 'like', "%{$term}%")
                      ->orWhere('ingredients', 'like', "%{$term}%");
      }
      ```
    - Usage in controller: `Recipe::search('pasta')->paginate()` or `Recipe::search('pasta')->get()`
    - This replaces the legacy `Recipe::search($sortOrder)` pattern with a cleaner implementation

**Success Criteria**:
- ✅ Search functionality works: `Recipe::search('pasta')->get()` or `Recipe::search('pasta')->paginate()`
- ✅ No N+1 query problems (verify with Debugbar or query logging)
- ✅ Search results are accurate and relevant

---

## Phase 5: Controllers & Routing

**Goals**: Implement controllers and routes for recipe and cookbook listing

### Base Artifacts Available
- **RecipeController**: Available at [github.com/dougis-org/laravel-recipes-update/app/Http/Controllers/RecipeController.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/app/Http/Controllers/RecipeController.php) - Handles all sorting, searching, and pagination logic
- **CookbookController**: Available at [github.com/dougis-org/laravel-recipes-update/app/Http/Controllers/CookbookController.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/app/Http/Controllers/CookbookController.php) - Handles listing and detail views
- **Routing**: Legacy app uses resource-based routing in modularized `Http/Routes/` files

### Tasks

15. **Adapt RecipeController**
    - Source: [github.com/dougis-org/laravel-recipes-update/app/Http/Controllers/RecipeController.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/app/Http/Controllers/RecipeController.php)
    - Update: Modernize for Laravel 12 while preserving functionality
    - Key logic to preserve:
      - Query parameters: `sortField` (name, date_added), `sortOrder` (asc, desc), `displayCount` (20, 30, all), `search` query
      - Default sorting: date_added descending
      - Default display count: 30 per page
      - Search handling: differentiates between search results and sorted results
    - Modernize: Remove legacy search handling; replace with query scope
    - Add eager loading: `with(['classification', 'source', 'meals', 'preparations', 'courses'])`
    - Methods:
      - `index()`: List recipes with filtering, sorting, pagination
      - `show($id)`: Show recipe details with relationships

16. **Adapt CookbookController**
    - Source: [github.com/dougis-org/laravel-recipes-update/app/Http/Controllers/CookbookController.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/app/Http/Controllers/CookbookController.php)
    - Update: Add eager loading and modernize for Laravel 12
    - Key logic to preserve:
      - Index: Show all cookbooks with recipe count
      - Show: Display cookbook detail with recipes ordered by classification name, then recipe name
    - Methods:
      - `index()`: List cookbooks with recipe counts
      - `show($id)`: Show cookbook detail with recipes ordered by classification, then name

17. **Create Form Requests** (optional but recommended for validation)
    - `app/Http/Requests/SearchRecipeRequest.php`: Validate search parameters
    - Add rules for sortField, sortOrder, displayCount

18. **Define Routes** (in `routes/web.php`)
    ```php
    Route::resource('recipes', RecipeController::class)->only(['index', 'show']);
    Route::resource('cookbooks', CookbookController::class)->only(['index', 'show']);
    Route::redirect('/', '/recipes?sortField=date_added&sortOrder=desc&displayCount=30');
    ```

19. **Test Routes**
    - Verify routes exist: `php artisan route:list`
    - Test routes in browser: http://localhost:8000/recipes

**Success Criteria**:
- ✅ Routes registered and accessible
- ✅ Controllers respond to requests without errors
- ✅ RecipeController index returns paginated recipes with proper sorting
- ✅ RecipeController show returns single recipe with relationships
- ✅ Default route redirects to recipe index with default sorting
- ✅ CookbookController listing and detail work correctly

---

## Phase 6: Views - Layout & Components

**Goals**: Create base layout and reusable Blade components styled with Tailwind CSS

### Tasks

20. **Create Base Layout** (`resources/views/layouts/app.blade.php`)
    - Include HTML5 structure
    - Include Vite directives for CSS and JS
    - Navigation bar with Tailwind styling
    - Footer
    - Flash message display for alerts
    - Yield or slot for page content
    - Meta tags (charset, viewport, etc.)

21. **Create Reusable Components** (in `resources/views/components/`)
    
    a. **button.blade.php**: Reusable button with type variants (primary, secondary, danger)
       - Props: type (default primary), icon (optional), text, href (optional for link button)
    
    b. **input.blade.php**: Form input field with label and error display
       - Props: name, label, type (default text), value, error (optional)
    
    c. **select.blade.php**: Form select field with options
       - Props: name, label, options (array), selected (optional), error (optional)
    
    d. **card.blade.php**: Card container with optional header and footer
       - Props: title (optional), class (optional), slots for header, body, footer
    
    e. **recipe-card.blade.php**: Display recipe summary (for grid/list)
       - Props: recipe object
       - Display: name, classification, source, date added, nutrition summary
    
    f. **pagination.blade.php**: Pagination links with Tailwind styling
       - Accept paginator object and render links
    
    g. **sort-controls.blade.php**: Sort direction and field selector
       - Props: current sortField, current sortOrder
       - Allow toggling sort direction and field

22. **Create Navigation Component** (in `resources/views/components/`)
    - navbar.blade.php: Fixed or sticky header with logo, menu items, mobile toggle
    - Use Alpine.js for mobile menu functionality
    - Links to Recipes, Cookbooks, etc.

23. **Test Components in Browser**
    - Verify Tailwind classes render correctly
    - Check responsive behavior on mobile
    - Verify Alpine.js components work (e.g., mobile menu toggle)

**Success Criteria**:
- ✅ Base layout renders without errors
- ✅ Components display correctly with Tailwind styling
- ✅ Mobile menu toggle works with Alpine.js
- ✅ All views inherit from base layout
- ✅ No CSS class naming conflicts
- ✅ Responsive design works on mobile, tablet, desktop

---

## Phase 7: Views - Recipe Pages

**Goals**: Implement recipe listing and detail views using modern Tailwind CSS

### Base Artifacts Available
- **Recipe Index View**: Available at [github.com/dougis-org/laravel-recipes-update/resources/views/recipe/index.blade.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/resources/views/recipe/index.blade.php) - Shows recipe grid with search/sort/pagination
- **Recipe Show View**: Available at [github.com/dougis-org/laravel-recipes-update/resources/views/recipe/show.blade.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/resources/views/recipe/show.blade.php) - Shows recipe detail
- **Legacy Styling**: Uses Foundation Framework (to be replaced with Tailwind CSS 4)

### Tasks

24. **Create Modern Recipe Index View** (`resources/views/recipes/index.blade.php`)
    - Source layout: [github.com/dougis-org/laravel-recipes-update/resources/views/recipe/index.blade.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/resources/views/recipe/index.blade.php)
    - Preserve functionality: Search form, sort controls, display count selector, pagination
    - Modernize styling: Replace Foundation grid (`.large-3 .medium-6 .small-12`) with Tailwind responsive classes
    - Layout:
      - Search form (query input with submit)
      - Sort controls (field selector and direction toggle)
      - Display count selector (20, 30, all)
      - Recipe card grid using Tailwind: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4`
      - Pagination controls below grid
    - Use Blade components created in Phase 6

25. **Create Modern Recipe Show View** (`resources/views/recipes/show.blade.php`)
    - Source layout: [github.com/dougis-org/laravel-recipes-update/resources/views/recipe/show.blade.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/resources/views/recipe/show.blade.php)
    - Preserve functionality: Display all recipe details and relationships
    - Modernize styling: Replace Foundation styling with Tailwind CSS
    - Display recipe details:
      - Name (large heading)
      - Classification and source
      - Ingredients (formatted as list)
      - Instructions (formatted as paragraphs or numbered list)
      - Nutritional information (servings, calories, fat, protein, etc.)
      - Related meals, preparations, courses (as badge/tag list)
      - Cookbooks containing this recipe (as list)
      - Back to listing link
    - Use card component for each section

26. **Implement Recipe Card Component**
    - Show recipe name, classification, source, date added
    - Add hover effect with Tailwind (shadow, scale)
    - Make clickable to detail view

27. **Style Forms with Tailwind**
    - Search form: input field + submit button
    - Sort controls: dropdown selects + buttons
    - Use component input and select fields
    - Add visual feedback for active sorting

**Success Criteria**:
- ✅ Recipe index displays recipes in responsive grid
- ✅ Pagination controls work and maintain search/sort parameters
- ✅ Sorting by name and date works (ascending and descending)
- ✅ Display count selector changes page size (20, 30, all)
- ✅ Search filters recipes by name and ingredients
- ✅ Recipe detail view displays all information correctly
- ✅ Related data (meals, preparations, courses, cookbooks) displays
- ✅ All styling uses Tailwind CSS, no Bootstrap classes

---

## Phase 8: Views - Cookbook Pages

**Goals**: Implement cookbook listing and detail views using modern Tailwind CSS

### Base Artifacts Available
- **Cookbook Index View**: Available at [github.com/dougis-org/laravel-recipes-update/resources/views/cookbook/index.blade.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/resources/views/cookbook/index.blade.php) - Shows cookbook list
- **Cookbook Show View**: Available at [github.com/dougis-org/laravel-recipes-update/resources/views/cookbook/show.blade.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/resources/views/cookbook/show.blade.php) - Shows cookbook detail with recipes
- **Legacy Styling**: Uses Foundation Framework (to be replaced with Tailwind CSS 4)

### Tasks

28. **Create Modern Cookbook Index View** (`resources/views/cookbooks/index.blade.php`)
    - Source layout: [github.com/dougis-org/laravel-recipes-update/resources/views/cookbook/index.blade.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/resources/views/cookbook/index.blade.php)
    - Preserve functionality: Display all cookbooks with recipe counts
    - Modernize styling: Replace Foundation styling with Tailwind CSS
    - Display:
      - Cookbook listing (card grid or table)
      - Each card shows: cookbook name, recipe count, link to detail
      - Pagination if many cookbooks

29. **Create Modern Cookbook Show View** (`resources/views/cookbooks/show.blade.php`)
    - Source layout: [github.com/dougis-org/laravel-recipes-update/resources/views/cookbook/show.blade.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/resources/views/cookbook/show.blade.php)
    - Preserve functionality: Display cookbook detail with recipes ordered by classification, then name
    - Modernize styling: Replace Foundation styling with Tailwind CSS
    - Display:
      - Cookbook name (large heading)
      - Recipe count
      - Recipes organized by classification (optional grouping), then by name
      - Each recipe as a card or list item with link to detail
      - Back to listing link

30. **Create Cookbook Card Component** (`resources/views/components/cookbook-card.blade.php`)
    - Show cookbook name, recipe count
    - Link to detail view

31. **Implement Cookbook Recipe Ordering**
    - Use eager loading to fetch recipes with classification: `with(['recipes' => function ($query) { $query->join('classifications', ...)->orderBy('classifications.name')->orderBy('recipes.name'); }])`
    - Or use Eloquent ordering: `recipes()->orderBy('classification_name')->orderBy('name')`

**Success Criteria**:
- ✅ Cookbook index displays cookbooks with recipe counts
- ✅ Cookbook detail shows all recipes ordered correctly (by classification, then name)
- ✅ Recipes display with classification and source information
- ✅ Pagination works if many cookbooks
- ✅ Styling consistent with recipe pages

---

## Phase 9: Frontend Interactivity with Alpine.js

**Goals**: Add lightweight interactivity with Alpine.js

### Tasks

32. **Mobile Menu Toggle**
    - Use Alpine.js `x-data` and `@click` to toggle menu visibility
    - Show/hide navigation items on mobile
    - Add smooth transition with Tailwind

33. **Sort Direction Toggle**
    - Add Alpine component to toggle sort direction (asc ↔ desc)
    - Update form input and submit on click

34. **Display Count Selector**
    - Create Alpine component to select display count (20, 30, all)
    - Update form input and submit on selection

35. **Search Form Enhancement** (optional)
    - Add debounced search input for live preview (optional)
    - Show search icon and clear button
    - Highlight active search term

36. **Hover Effects**
    - Recipe cards: add shadow and scale on hover
    - Buttons: add color transitions and cursor pointer
    - Use Tailwind classes: `hover:shadow-lg`, `hover:scale-105`, `transition`

**Success Criteria**:
- ✅ Mobile menu opens/closes smoothly
- ✅ Sort direction toggle works without full page refresh
- ✅ Display count selector updates results
- ✅ No console errors from Alpine.js
- ✅ Interactivity works on all screen sizes
- ✅ Transitions are smooth (not jarring)

---

## Phase 10: Asset Pipeline & Build Optimization

**Goals**: Ensure assets compile correctly for development and production

### Tasks

37. **Verify Vite Configuration**
    - Check `vite.config.js` includes Laravel plugin
    - Verify entry points: `resources/css/app.css` and `resources/js/app.js`

38. **Development Build**
    - Run: `npm run dev`
    - Verify assets load in browser (check Network tab)
    - Verify styles apply correctly
    - Verify Alpine.js functionality works

39. **Production Build**
    - Run: `npm run build`
    - Verify `public/build/` contains compiled assets
    - Verify manifest.json exists
    - Test loading production-built assets (run `php artisan serve` after build)

40. **Asset Optimization**
    - Verify CSS is minified in production
    - Verify JS is minified in production
    - Check file sizes are reasonable
    - Verify no console warnings about asset loading

**Success Criteria**:
- ✅ Development build works with hot reload
- ✅ Production build generates minified assets
- ✅ No 404 errors for asset files
- ✅ All styles and scripts apply correctly
- ✅ Bundle size is reasonable (CSS <100KB minified, JS <50KB)

---

## Phase 11: Database Seeding

**Goals**: Populate database with test data

### Tasks

41. **Create Seeders** (in `database/seeders/`)
    
    a. **ClassificationSeeder.php**: Create common classifications (Appetizer, Main Course, Dessert, Beverage, Sauce)
    
    b. **SourceSeeder.php**: Create common sources (cookbook names, websites, family recipes)
    
    c. **MealSeeder.php**: Create meals (Breakfast, Lunch, Dinner, Snack)
    
    d. **PreparationSeeder.php**: Create preparation methods (Baked, Fried, Grilled, Raw, Boiled, Steamed)
    
    e. **CourseSeeder.php**: Create courses (Appetizer, Salad, Soup, Main, Side, Dessert)

42. **Create Recipe Factory** (`database/factories/RecipeFactory.php`)
    - Generate random recipe data with valid relationships
    - Include realistic ingredients and instructions
    - Set date_added to random past date

43. **Create Cookbook Factory** (`database/factories/CookbookFactory.php`)
    - Generate random cookbook data
    - Attach random recipes to each cookbook

44. **Update DatabaseSeeder** (`database/seeders/DatabaseSeeder.php`)
    - Call all seeders
    - Create test recipes with relationships
    - Create test cookbooks with recipes

45. **Seed Database**
    - Command: `php artisan migrate:fresh --seed`
    - Verify data is created correctly

**Success Criteria**:
- ✅ Migrations and seeds run without errors
- ✅ Database contains test data: recipes, classifications, sources, meals, preparations, courses, cookbooks
- ✅ Relationships are correctly established (recipes belong to classifications and sources, etc.)
- ✅ Recipe index displays seeded recipes with proper sorting
- ✅ Cookbook detail shows recipes ordered correctly

---

## Phase 12: Testing & Quality Assurance

**Goals**: Write tests for critical functionality

### Tasks

46. **Create Feature Tests** (in `tests/Feature/`)
    
    a. **RecipeIndexTest.php**: Test recipe listing
       - Test default sorting (by date_added desc)
       - Test sorting by name (asc/desc)
       - Test pagination with different display counts
       - Test search functionality
       - Test relationships load correctly
    
    b. **RecipeShowTest.php**: Test recipe detail
       - Test recipe loads with all relationships
       - Test 404 for non-existent recipe
    
    c. **CookbookIndexTest.php**: Test cookbook listing
       - Test listing displays all cookbooks
       - Test recipe counts are correct
    
    d. **CookbookShowTest.php**: Test cookbook detail
       - Test recipes display in correct order (by classification, then name)
       - Test 404 for non-existent cookbook

47. **Create Unit Tests** (in `tests/Unit/`)
    
    a. **RecipeModelTest.php**: Test Recipe model scopes and relationships
       - Test `search()` scope
       - Test `orderByDateAdded()` scope
       - Test `orderByName()` scope
       - Test relationships (classification, source, meals, preparations, courses, cookbooks)
    
    b. **CookbookModelTest.php**: Test Cookbook model
       - Test recipes relationship with correct ordering
       - Test eager loading performance

48. **Run Tests**
    - Command: `php artisan test`
    - All tests pass without errors
    - Verify code coverage for critical paths

49. **Performance Testing**
    - Verify no N+1 queries (use query logging or Debugbar)
    - Verify pagination performs well with large datasets
    - Test search performance
    - Verify eager loading is used in controllers

**Success Criteria**:
- ✅ All tests pass: `php artisan test`
- ✅ Recipe index loads recipes correctly with default sorting
- ✅ Pagination works with 20, 30, all display counts
- ✅ Search filters results accurately
- ✅ Sorting by name and date works in both directions
- ✅ Cookbook recipes are ordered by classification, then name
- ✅ No N+1 query problems
- ✅ No console errors or warnings

---

## Phase 13: Security Hardening & Error Handling

**Goals**: Implement comprehensive security measures, error handling, and improve user experience

### Tasks

50. **Configure Security Headers**
    - Update `config/app.php` and middleware
    - Add security headers in `app/Http/Middleware/`:
      ```php
      // Content Security Policy
      header("Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';");

      // Prevent clickjacking
      header("X-Frame-Options: SAMEORIGIN");

      // Prevent MIME sniffing
      header("X-Content-Type-Options: nosniff");

      // XSS Protection
      header("X-XSS-Protection: 1; mode=block");

      // HSTS (HTTPS enforcement) - only in production
      header("Strict-Transport-Security: max-age=31536000; includeSubDomains");
      ```
    - OR use package: `composer require bepsvpt/secure-headers`

51. **Implement Rate Limiting**
    - Configure in `app/Http/Kernel.php`:
      ```php
      'api' => [
          'throttle:60,1', // 60 requests per minute
      ],
      'web' => [
          'throttle:1000,1', // 1000 requests per minute
      ],
      ```
    - Add custom rate limiting for search:
      ```php
      RateLimiter::for('search', function (Request $request) {
          return Limit::perMinute(30)->by($request->ip());
      });
      ```

52. **Implement Form Request Validation**
    - Create `app/Http/Requests/SearchRecipeRequest.php`:
      ```php
      public function rules() {
          return [
              'search' => 'nullable|string|max:100',
              'sortField' => 'nullable|in:name,date_added',
              'sortOrder' => 'nullable|in:asc,desc',
              'displayCount' => 'nullable|integer|in:20,30,50,100',
          ];
      }
      ```
    - Prevents SQL injection and validates all user input

53. **Configure CSRF Protection**
    - Verify CSRF middleware is active in `app/Http/Kernel.php`
    - Add `@csrf` to all forms
    - Configure CSRF token refresh for long-running sessions
    - Custom 419 error page for expired tokens

54. **Implement Mass Assignment Protection**
    - Verify all models have `$fillable` or `$guarded` arrays
    - Never use `$guarded = []` in production
    - Review all models for proper mass assignment protection

55. **Configure HTTPS Enforcement** (Production)
    - Update `.env`: `APP_URL=https://your-domain.com`
    - Add middleware to force HTTPS:
      ```php
      if (!$request->secure() && app()->environment('production')) {
          return redirect()->secure($request->getRequestUri());
      }
      ```
    - Or use `TrustProxies` middleware

56. **Implement Input Sanitization**
    - Use Laravel's built-in XSS protection (Blade escaping)
    - Verify all output uses `{{ $variable }}` not `{!! $variable !!}`
    - Sanitize user input in controllers before database storage

57. **Create Error Views** (in `resources/views/errors/`)

    a. **404.blade.php**: Not found error
    b. **500.blade.php**: Server error
    c. **419.blade.php**: Session expired (CSRF token)
    d. **429.blade.php**: Too many requests (rate limit)
    e. **403.blade.php**: Forbidden (authorization)

58. **Configure Exception Handler** (`app/Exceptions/Handler.php`)
    - Set up proper error logging with context
    - Return user-friendly error responses (no stack traces in production)
    - Log errors to `storage/logs/` with rotation
    - Configure error reporting levels per environment
    - Never expose sensitive data in error messages

59. **Implement Error Monitoring** (Optional but recommended)
    - Option 1: Laravel Flare (free tier available)
      - Install: `composer require spatie/laravel-ignition`
      - Configure in `config/flare.php`
    - Option 2: Sentry
      - Install: `composer require sentry/sentry-laravel`
      - Add DSN to `.env`: `SENTRY_LARAVEL_DSN=your-dsn`
    - Option 3: Bugsnag
      - Install: `composer require bugsnag/bugsnag-laravel`

60. **Add Flash Messages**
    - Implement success/error flash messages
    - Display in layout header/footer area
    - Auto-dismiss after 5 seconds with Alpine.js
    - Use Bootstrap-style alerts: success, error, warning, info

61. **Security Testing**
    - Test CSRF protection on all forms
    - Test rate limiting on search endpoint
    - Verify HTTPS redirects (in production)
    - Test 419 error page for expired CSRF tokens
    - Verify no SQL injection vulnerabilities
    - Test XSS protection (try injecting `<script>alert('xss')</script>`)

**Success Criteria**:
- ✅ All security headers configured and verified
- ✅ Rate limiting active on search and forms
- ✅ CSRF protection working on all forms
- ✅ Input validation active via Form Requests
- ✅ Mass assignment protection verified on all models
- ✅ HTTPS enforced in production environment
- ✅ 404 error displays gracefully
- ✅ 500 error displays gracefully
- ✅ Error pages styled consistently with app
- ✅ User feedback messages display correctly
- ✅ No raw exception messages shown to users
- ✅ Error monitoring configured (if using external service)
- ✅ Security testing completed with no vulnerabilities

---

## Phase 14: Accessibility, Performance & Browser Compatibility

**Goals**: Ensure application is accessible, performant, and compatible across browsers

### Tasks

62. **Implement Accessibility (WCAG 2.1 AA)**
    - Add alt text to all images
    - Use semantic HTML (header, nav, main, footer, section, article)
    - Add ARIA labels where needed:
      ```html
      <nav aria-label="Main navigation">
      <button aria-label="Open mobile menu" aria-expanded="false">
      ```
    - Ensure all form inputs have associated labels
    - Add skip navigation link for keyboard users
    - Test keyboard navigation (Tab, Enter, Escape)
    - Verify color contrast meets WCAG AA standards (4.5:1 for normal text, 3:1 for large text)
    - Test with screen reader (NVDA, JAWS, or VoiceOver)
    - Add focus indicators for all interactive elements

63. **Performance Optimization**
    - Database query optimization:
      - Verify indexes are used (check with `EXPLAIN` queries)
      - Ensure eager loading prevents N+1: `with('classification', 'source')`
      - Add query result caching for reference data (classifications, sources)
    - Asset optimization:
      - Test with production build: `npm run build`
      - Verify CSS is minified and purged (unused Tailwind classes removed)
      - Verify JavaScript is minified
      - Enable gzip/brotli compression in web server
    - Image optimization (if applicable):
      - Use lazy loading: `loading="lazy"`
      - Use modern formats (WebP with fallbacks)
      - Serve appropriately sized images
    - Implement caching headers:
      - Static assets: `Cache-Control: public, max-age=31536000, immutable`
      - HTML: `Cache-Control: no-cache, must-revalidate`

64. **Set Performance Benchmarks**
    - **Target Metrics**:
      - First Contentful Paint (FCP): < 1.8s
      - Largest Contentful Paint (LCP): < 2.5s
      - Time to Interactive (TTI): < 3.5s
      - Cumulative Layout Shift (CLS): < 0.1
      - First Input Delay (FID): < 100ms
      - Total Blocking Time (TBT): < 300ms
    - **Page Load Times** (3G connection):
      - Recipe index: < 2.0s
      - Recipe detail: < 1.5s
      - Cookbook index: < 2.0s
      - Cookbook detail: < 2.5s
    - **Database Performance**:
      - Max queries per page: 10 queries
      - Average query time: < 50ms
      - No queries over 200ms
    - **Asset Sizes**:
      - CSS bundle: < 100KB (minified)
      - JavaScript bundle: < 50KB (minified)
      - Total page size: < 500KB

65. **Run Lighthouse Audit**
    - Performance: > 90
    - Accessibility: > 90
    - Best Practices: > 90
    - SEO: > 90
    - Run on multiple pages (index, detail, cookbook)
    - Test on both desktop and mobile
    - Document and fix any issues

66. **Test Browser Compatibility**
    - **Desktop Browsers** (test all core features):
      - Chrome/Edge (last 2 versions): Latest stable + previous
      - Firefox (last 2 versions): Latest stable + previous
      - Safari (last 2 versions): macOS Safari latest + previous
    - **Mobile Browsers**:
      - Chrome Mobile (Android): Latest stable
      - Safari Mobile (iOS): iOS 16+ and 17+
    - **Feature Testing Matrix**:
      - ✅ Tailwind CSS rendering
      - ✅ Alpine.js functionality (mobile menu, toggles)
      - ✅ Form submissions
      - ✅ Pagination
      - ✅ Search functionality
      - ✅ Responsive design breakpoints
    - **Polyfills** (if needed):
      - Add polyfills for older browsers via browserslist
      - Configure in `package.json`:
        ```json
        "browserslist": [
          "last 2 versions",
          "> 1%",
          "not dead"
        ]
        ```

67. **Test Responsive Design**
    - **Breakpoints to test**:
      - Mobile: 320px, 375px, 414px (iPhone SE, iPhone 12/13, iPhone Pro Max)
      - Tablet: 768px, 834px, 1024px (iPad, iPad Air, iPad Pro)
      - Desktop: 1280px, 1440px, 1920px, 2560px
    - **Responsive checks**:
      - Navigation collapses to hamburger menu on mobile
      - Recipe grid adjusts columns (1 → 2 → 3 → 4)
      - Forms are thumb-friendly with adequate spacing
      - Touch targets minimum 44x44px
      - Font sizes readable without zooming
      - No horizontal scrolling
    - **Test orientations**:
      - Portrait and landscape on mobile/tablet
    - **Test devices** (BrowserStack or physical):
      - iPhone 12/13/14
      - iPad Air
      - Samsung Galaxy S21/S22
      - Desktop at various resolutions

68. **Performance Monitoring Setup** (Ongoing)
    - Add server timing headers for debugging
    - Configure Laravel Telescope for local debugging (optional)
    - Set up performance monitoring in production:
      - New Relic (recommended)
      - Blackfire.io
      - Laravel Debugbar (dev only)
    - Monitor Core Web Vitals in production

**Success Criteria**:
- ✅ WCAG 2.1 AA compliance verified with automated tools
- ✅ Application is fully keyboard navigable
- ✅ Alt text present on all images
- ✅ Semantic HTML used throughout
- ✅ Screen reader testing completed
- ✅ Lighthouse score > 90 on all metrics (Performance, Accessibility, Best Practices, SEO)
- ✅ All performance benchmarks met (FCP < 1.8s, LCP < 2.5s, etc.)
- ✅ Page load times within targets (< 2.0s for index, < 1.5s for detail)
- ✅ Database queries optimized (< 10 per page, < 50ms average)
- ✅ Asset sizes within limits (CSS < 100KB, JS < 50KB)
- ✅ Tested and working in all supported browsers
- ✅ Responsive design verified on all breakpoints and devices
- ✅ Touch targets adequate for mobile (44x44px minimum)
- ✅ No layout shifts (CLS < 0.1)
- ✅ Mobile experience is smooth and usable

---

## Phase 15: CI/CD Pipeline Setup

**Goals**: Automate testing, code quality checks, and deployment process

### Tasks

69. **Create GitHub Actions Workflow** (`.github/workflows/laravel.yml`)
    ```yaml
    name: Laravel CI/CD

    on:
      push:
        branches: [ main, develop ]
      pull_request:
        branches: [ main, develop ]

    jobs:
      test:
        runs-on: ubuntu-latest

        services:
          mysql:
            image: mysql:8.0
            env:
              MYSQL_ROOT_PASSWORD: password
              MYSQL_DATABASE: testing
            ports:
              - 3306:3306
            options: --health-cmd="mysqladmin ping" --health-interval=10s --health-timeout=5s --health-retries=3

        steps:
        - uses: actions/checkout@v4

        - name: Setup PHP
          uses: shivammathur/setup-php@v2
          with:
            php-version: '8.5'
            extensions: mbstring, xml, bcmath, pdo_mysql
            coverage: xdebug

        - name: Install Composer dependencies
          run: composer install --prefer-dist --no-progress

        - name: Copy .env
          run: php -r "file_exists('.env') || copy('.env.testing', '.env');"

        - name: Generate key
          run: php artisan key:generate

        - name: Directory Permissions
          run: chmod -R 777 storage bootstrap/cache

        - name: Run migrations
          env:
            DB_CONNECTION: mysql
            DB_HOST: 127.0.0.1
            DB_PORT: 3306
            DB_DATABASE: testing
            DB_USERNAME: root
            DB_PASSWORD: password
          run: php artisan migrate

        - name: Execute tests
          env:
            DB_CONNECTION: mysql
            DB_HOST: 127.0.0.1
            DB_PORT: 3306
            DB_DATABASE: testing
            DB_USERNAME: root
            DB_PASSWORD: password
          run: vendor/bin/pest --coverage --min=80

        - name: Run Laravel Pint (code style)
          run: vendor/bin/pint --test

        - name: Run PHPStan (static analysis)
          run: vendor/bin/phpstan analyse --memory-limit=2G

      frontend:
        runs-on: ubuntu-latest

        steps:
        - uses: actions/checkout@v4

        - name: Setup Node.js
          uses: actions/setup-node@v4
          with:
            node-version: '25'
            cache: 'npm'

        - name: Install dependencies
          run: npm ci

        - name: Build assets
          run: npm run build

        - name: Lint JavaScript
          run: npm run lint || true
    ```

70. **Configure PHPStan** (`phpstan.neon`)
    ```neon
    parameters:
        level: 5
        paths:
            - app
        excludePaths:
            - app/Console/Kernel.php
        checkMissingIterableValueType: false
    ```

71. **Configure Laravel Pint** (`pint.json`)
    ```json
    {
        "preset": "laravel",
        "rules": {
            "simplified_null_return": true,
            "braces": true,
            "new_with_braces": true
        }
    }
    ```

72. **Add Pre-commit Hooks** (Optional)
    - Install: `composer require --dev brainmaestro/composer-git-hooks`
    - Configure in `composer.json`:
      ```json
      "extra": {
          "hooks": {
              "pre-commit": [
                  "vendor/bin/pint",
                  "vendor/bin/pest"
              ],
              "pre-push": [
                  "vendor/bin/phpstan analyse"
              ]
          }
      }
      ```
    - Install hooks: `vendor/bin/cghooks add --ignore-lock`

73. **Configure Dependabot** (`.github/dependabot.yml`)
    ```yaml
    version: 2
    updates:
      - package-ecosystem: "composer"
        directory: "/"
        schedule:
          interval: "weekly"

      - package-ecosystem: "npm"
        directory: "/"
        schedule:
          interval: "weekly"

      - package-ecosystem: "github-actions"
        directory: "/"
        schedule:
          interval: "weekly"
    ```

74. **Add Code Coverage Reporting** (Optional)
    - Codecov: Add to GitHub Actions
      ```yaml
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
      ```
    - Or use Coveralls
    - Add badge to README.md

75. **Configure Deployment** (Choose one)

    **Option A: Laravel Forge**
    - Connect GitHub repository
    - Configure deployment trigger on main branch
    - Set up environment variables
    - Configure deployment script

    **Option B: GitHub Actions Deployment**
    ```yaml
    deploy:
      needs: [test, frontend]
      runs-on: ubuntu-latest
      if: github.ref == 'refs/heads/main'

      steps:
        - uses: actions/checkout@v4

        - name: Deploy to production
          uses: appleboy/ssh-action@master
          with:
            host: ${{ secrets.HOST }}
            username: ${{ secrets.USERNAME }}
            key: ${{ secrets.SSH_KEY }}
            script: |
              cd /var/www/laravel-recipes
              git pull origin main
              composer install --no-dev --optimize-autoloader
              npm ci && npm run build
              php artisan migrate --force
              php artisan config:cache
              php artisan route:cache
              php artisan view:cache
              php artisan queue:restart
    ```

76. **Test CI/CD Pipeline**
    - Push to feature branch and create PR
    - Verify all checks pass
    - Merge PR and verify deployment (if configured)

**Success Criteria**:
- ✅ GitHub Actions workflow running on all PRs
- ✅ All tests pass in CI environment
- ✅ Code style checks (Pint) passing
- ✅ Static analysis (PHPStan) passing
- ✅ Frontend build succeeds in CI
- ✅ Code coverage reports generated (>80%)
- ✅ Deployment automation configured
- ✅ Dependabot configured for dependency updates
- ✅ Pre-commit hooks working (if configured)

---

## Phase 16: Documentation, Backup & Deployment

**Goals**: Document the application, configure backup strategy, and prepare for deployment

### Tasks

77. **Configure Database Backup Strategy**

    **Option A: Automated Backups with Laravel Backup Package**
    - Install: `composer require spatie/laravel-backup`
    - Configure `config/backup.php`:
      ```php
      'backup' => [
          'name' => env('APP_NAME', 'laravel-backup'),
          'source' => [
              'files' => [
                  'include' => [
                      base_path(),
                  ],
                  'exclude' => [
                      base_path('vendor'),
                      base_path('node_modules'),
                  ],
              ],
              'databases' => [
                  'mysql',
              ],
          ],
          'destination' => [
              'filename_prefix' => '',
              'disks' => [
                  's3', // or 'local' for testing
              ],
          ],
      ],
      ```
    - Schedule in `app/Console/Kernel.php`:
      ```php
      protected function schedule(Schedule $schedule)
      {
          $schedule->command('backup:clean')->daily()->at('01:00');
          $schedule->command('backup:run')->daily()->at('02:00');
      }
      ```

    **Option B: Manual MySQL Backups**
    - Create backup script (`scripts/backup.sh`):
      ```bash
      #!/bin/bash
      DATE=$(date +%Y%m%d_%H%M%S)
      mysqldump -u $DB_USER -p$DB_PASS $DB_NAME > backups/db_$DATE.sql
      gzip backups/db_$DATE.sql
      # Upload to S3 or remote storage
      aws s3 cp backups/db_$DATE.sql.gz s3://your-bucket/backups/
      # Keep only last 30 days
      find backups/ -name "db_*.sql.gz" -mtime +30 -delete
      ```
    - Add to crontab: `0 2 * * * /path/to/scripts/backup.sh`

78. **Configure Backup Verification**
    - Test backup restoration weekly
    - Verify backup integrity:
      ```bash
      gunzip < backup.sql.gz | mysql -u user -p dbname_test
      ```
    - Set up backup monitoring alerts
    - Store backups in multiple locations (local + cloud)

79. **Implement Disaster Recovery Plan**

    **Recovery Procedures Documentation** (`docs/DISASTER_RECOVERY.md`):
    - Database restoration steps
    - Application restoration steps
    - DNS failover procedures (if applicable)
    - Contact list for emergencies
    - Expected Recovery Time Objective (RTO): < 4 hours
    - Recovery Point Objective (RPO): < 24 hours (daily backups)

    **Database Recovery Steps**:
    ```bash
    # 1. Stop application
    php artisan down

    # 2. Restore database from backup
    gunzip < backup_YYYYMMDD.sql.gz | mysql -u user -p database

    # 3. Run any pending migrations
    php artisan migrate --force

    # 4. Clear caches
    php artisan config:clear
    php artisan cache:clear
    php artisan view:clear

    # 5. Bring application back online
    php artisan up
    ```

80. **Configure Staging Environment**
    - Set up staging server matching production
    - Configure `.env.staging` with separate database
    - Set up separate domain: `staging.yourdomain.com`
    - Configure deployment to staging before production
    - Use for final testing before production deployment
    - Set `APP_ENV=staging` and `APP_DEBUG=true`

81. **Update Documentation**
    - Update `README.md` with:
      - Project overview
      - Tech stack (Laravel 12, Tailwind CSS 4+, Alpine.js 3, Vite, PHP 8.5+, Node.js 25+)
      - Setup instructions
      - Database schema overview
      - Feature documentation
      - Browser compatibility matrix
    - Create `DEVELOPMENT.md` with:
      - Development workflow (running dev server, building assets, running tests)
      - Debugging tips (Laravel Telescope, Debugbar, Log viewing)
      - Common tasks (creating models, migrations, seeders)
      - Running tests with code coverage
      - Code style guidelines (PSR-12, Pint configuration)
    - Create `DEPLOYMENT.md` with:
      - Server requirements
      - Deployment steps
      - Environment configuration
      - Rollback procedures
      - Backup and recovery procedures
    - Create `DISASTER_RECOVERY.md` with:
      - Recovery procedures
      - Backup restoration steps
      - Emergency contacts
      - RTO/RPO commitments

82. **Configure Environment Variables**
    - Create comprehensive `.env.example`:
      ```env
      APP_NAME="Laravel Recipes"
      APP_ENV=local
      APP_KEY=
      APP_DEBUG=true
      APP_URL=http://localhost

      LOG_CHANNEL=stack
      LOG_LEVEL=debug

      DB_CONNECTION=mysql
      DB_HOST=127.0.0.1
      DB_PORT=3306
      DB_DATABASE=laravel_recipes
      DB_USERNAME=root
      DB_PASSWORD=

      BROADCAST_DRIVER=log
      CACHE_DRIVER=file
      FILESYSTEM_DISK=local
      QUEUE_CONNECTION=sync
      SESSION_DRIVER=file
      SESSION_LIFETIME=120

      # Backup Configuration (if using spatie/laravel-backup)
      BACKUP_DISK=s3
      AWS_ACCESS_KEY_ID=
      AWS_SECRET_ACCESS_KEY=
      AWS_DEFAULT_REGION=us-east-1
      AWS_BUCKET=

      # Mail Configuration
      MAIL_MAILER=smtp
      MAIL_HOST=mailhog
      MAIL_PORT=1025
      MAIL_USERNAME=null
      MAIL_PASSWORD=null
      MAIL_ENCRYPTION=null
      MAIL_FROM_ADDRESS="hello@example.com"
      MAIL_FROM_NAME="${APP_NAME}"

      # Error Monitoring (optional)
      SENTRY_LARAVEL_DSN=
      FLARE_KEY=
      ```
    - Document each variable's purpose in `.env.example` comments

83. **Test Fresh Installation**
    - Clone repository and run setup from scratch:
      ```bash
      git clone <repo>
      cd laravel-recipes-2025
      composer install
      npm install
      cp .env.example .env
      php artisan key:generate
      php artisan migrate --seed
      npm run build
      php artisan serve
      ```
    - Verify application runs correctly
    - Test all major features work
    - Verify database seeded properly

84. **Production Deployment Checklist**
    - [ ] All tests pass (`vendor/bin/pest`)
    - [ ] Code style checks pass (`vendor/bin/pint --test`)
    - [ ] Static analysis passes (`vendor/bin/phpstan analyse`)
    - [ ] No console errors or warnings
    - [ ] Production build completes successfully (`npm run build`)
    - [ ] `.env` configured for production (APP_ENV=production, APP_DEBUG=false)
    - [ ] Database migrations tested on staging
    - [ ] Backup system configured and tested
    - [ ] Error monitoring configured (Sentry/Flare)
    - [ ] Security headers configured
    - [ ] HTTPS enforced
    - [ ] CSRF protection enabled
    - [ ] Rate limiting configured
    - [ ] Cron jobs configured (backups, scheduled tasks)
    - [ ] Log rotation configured
    - [ ] Server requirements met (PHP 8.5+, MySQL 8.0+, Node.js 25+)
    - [ ] File permissions set correctly (storage/ and bootstrap/cache/ writable)
    - [ ] Composer autoload optimized (`composer install --optimize-autoloader --no-dev`)
    - [ ] Config cached (`php artisan config:cache`)
    - [ ] Routes cached (`php artisan route:cache`)
    - [ ] Views cached (`php artisan view:cache`)
    - [ ] Rollback plan documented and tested
    - [ ] Disaster recovery plan documented
    - [ ] Monitoring and alerting configured
    - [ ] Performance benchmarks met

85. **Post-Deployment Verification**
    - Verify application is accessible
    - Test all major features:
      - Recipe listing with sorting
      - Recipe search
      - Recipe detail pages
      - Cookbook listing
      - Cookbook detail pages
    - Verify error pages (404, 500, 419)
    - Check Lighthouse scores (all > 90)
    - Monitor error logs for first 24 hours
    - Verify backups are running
    - Test disaster recovery procedure

**Success Criteria**:
- ✅ Automated backup system configured and tested
- ✅ Backups stored in multiple locations
- ✅ Disaster recovery plan documented and tested
- ✅ Staging environment configured
- ✅ README updated with comprehensive setup instructions
- ✅ Development documentation complete (DEVELOPMENT.md)
- ✅ Deployment documentation complete (DEPLOYMENT.md)
- ✅ Disaster recovery documentation complete (DISASTER_RECOVERY.md)
- ✅ Fresh installation works from scratch
- ✅ All environment variables documented
- ✅ Production deployment checklist completed
- ✅ Post-deployment verification successful
- ✅ Monitoring and alerting configured

---

## Implementation Checklist

### Phase 0: Prerequisites & System Requirements
- [ ] PHP 8.5+ installed with all required extensions
- [ ] Node.js 25+ and npm installed
- [ ] Composer 2.7+ installed
- [ ] Database server (MySQL 8.0+ or PostgreSQL 14+) running
- [ ] Git installed and configured
- [ ] Development environment ready (Valet/Herd/artisan serve)
- [ ] Code editor configured with extensions

### Phase 1: Project Setup
- [ ] Laravel 12 project initialized
- [ ] Database configured
- [ ] Version control initialized
- [ ] Dependencies installed and verified

### Phase 2: Frontend Stack
- [ ] Tailwind CSS 4+ installed and configured
- [ ] Alpine.js 3.14+ installed
- [ ] PostCSS and Autoprefixer configured
- [ ] Vite build pipeline working
- [ ] npm run dev and npm run build functional
- [ ] Asset loading verified in browser

### Phase 3: Database & Models
- [ ] All migrations created (tables + indexes)
- [ ] Database indexes migration created
- [ ] All migrations run successfully
- [ ] All Eloquent models created with relationships
- [ ] Models tested in Tinker
- [ ] Foreign key constraints verified

### Phase 4: Search
- [ ] Search scope implemented in Recipe model
- [ ] Search functionality working
- [ ] Full-text index created (if using MySQL)

### Phase 5: Controllers & Routing
- [ ] RecipeController created with index and show methods
- [ ] CookbookController created with index and show methods
- [ ] Form Request validation classes created
- [ ] Routes defined and tested
- [ ] Default route redirects correctly
- [ ] Eager loading configured to prevent N+1 queries

### Phase 6: Layout & Components
- [ ] Base layout created with Vite directives
- [ ] All reusable Blade components created
- [ ] Navigation component with mobile menu
- [ ] Responsive design verified
- [ ] Component library documented

### Phase 7: Recipe Views
- [ ] Recipe index view created with search, sort, pagination
- [ ] Recipe detail view created
- [ ] Recipe card component created
- [ ] All Tailwind CSS styling applied
- [ ] All features working (search, sort, pagination)

### Phase 8: Cookbook Views
- [ ] Cookbook index view created
- [ ] Cookbook detail view created
- [ ] Cookbook card component created
- [ ] Recipe ordering verified (by classification, then name)

### Phase 9: Alpine.js Interactivity
- [ ] Mobile menu working
- [ ] Sort toggle working
- [ ] Display count selector working
- [ ] Hover effects and transitions working
- [ ] No Alpine.js console errors

### Phase 10: Asset Pipeline
- [ ] Development build working with HMR
- [ ] Production build working
- [ ] CSS minified and purged
- [ ] JavaScript minified
- [ ] Assets within size limits (<100KB CSS, <50KB JS)

### Phase 11: Database Seeding
- [ ] All seeders created (Classifications, Sources, Meals, Preparations, Courses)
- [ ] RecipeFactory and CookbookFactory created
- [ ] Database seeded successfully
- [ ] Test data displays correctly in views
- [ ] Relationships properly seeded

### Phase 12: Testing
- [ ] Pest or PHPUnit configured
- [ ] Feature tests created and passing
- [ ] Unit tests created and passing
- [ ] Test coverage >80%
- [ ] Performance verified (no N+1 queries, <10 queries per page)
- [ ] All tests pass: `vendor/bin/pest`

### Phase 13: Security Hardening & Error Handling
- [ ] Security headers configured
- [ ] Rate limiting implemented
- [ ] Form Request validation on all inputs
- [ ] CSRF protection verified
- [ ] Mass assignment protection verified
- [ ] HTTPS enforcement configured (production)
- [ ] Input sanitization verified
- [ ] Error views created (404, 500, 419, 429, 403)
- [ ] Exception handler configured
- [ ] Error monitoring configured (optional)
- [ ] Flash messages working
- [ ] Security testing completed

### Phase 14: Accessibility, Performance & Browser Compatibility
- [ ] WCAG 2.1 AA compliance verified
- [ ] Keyboard navigation working
- [ ] Screen reader testing completed
- [ ] Semantic HTML throughout
- [ ] Database indexes verified with EXPLAIN
- [ ] Query caching configured
- [ ] Asset optimization complete
- [ ] Performance benchmarks met (FCP <1.8s, LCP <2.5s, CLS <0.1)
- [ ] Lighthouse score >90 on all metrics
- [ ] Tested in all supported browsers
- [ ] Responsive design verified on all breakpoints
- [ ] Touch targets adequate (44x44px minimum)

### Phase 15: CI/CD Pipeline
- [ ] GitHub Actions workflow created
- [ ] PHPStan configured and passing
- [ ] Laravel Pint configured and passing
- [ ] Tests running in CI environment
- [ ] Frontend build in CI working
- [ ] Code coverage reporting configured
- [ ] Dependabot configured
- [ ] Deployment automation configured
- [ ] Pre-commit hooks configured (optional)

### Phase 16: Documentation, Backup & Deployment
- [ ] Backup strategy configured and tested
- [ ] Backup verification process established
- [ ] Disaster recovery plan documented
- [ ] Staging environment configured
- [ ] README.md updated
- [ ] DEVELOPMENT.md created
- [ ] DEPLOYMENT.md created
- [ ] DISASTER_RECOVERY.md created
- [ ] .env.example comprehensive and documented
- [ ] Fresh installation tested
- [ ] Production deployment checklist completed
- [ ] Post-deployment verification successful
- [ ] Monitoring and alerting configured
- [ ] Ready for production deployment

---

## Legacy Artifact Adaptation Guide

This section provides detailed guidance on adapting artifacts from [github.com/dougis-org/laravel-recipes-update](https://github.com/dougis-org/laravel-recipes-update) for use in the modern Laravel 12 application.

### Migrations Adaptation Strategy

**Source**: [laravel-recipes-update/database/migrations/](https://github.com/dougis-org/laravel-recipes-update/tree/main/database/migrations)

**Key Differences Between Laravel 5.2 and Laravel 12 Migration Syntax**:

```php
// Laravel 5.2 (Old)
class CreateRecipesTable extends Migration {
    public function up() {
        Schema::create('recipes', function(Blueprint $table) {
            $table->integer('id', true);
            $table->string('name', 50);
        });
    }
}

// Laravel 12 (Modern)
return new class extends Migration {
    public function up(): void {
        Schema::create('recipes', function (Blueprint $table) {
            $table->id();
            $table->string('name');
        });
    }
    
    public function down(): void {
        Schema::dropIfExists('recipes');
    }
};
```

**Adaptation Checklist**:
- [ ] Use anonymous class syntax: `return new class extends Migration`
- [ ] Use return type hints: `up(): void`, `down(): void`
- [ ] Replace `$table->integer('id', true)` with `$table->id()`
- [ ] Remove string length limits where unnecessary (use `$table->string('name')` not `$table->string('name', 50)`)
- [ ] Use modern foreign key syntax: `$table->foreignId('source_id')->constrained()->cascadeOnDelete()` instead of separate foreign key calls
- [ ] Use `Schema::dropIfExists('table')` in down() method instead of `Schema::drop('table')`
- [ ] Consolidate related foreign key constraints into same migration (optional but cleaner)
- [ ] Update nutrition columns from `string` to `decimal` or `float`

**Example: Modernizing recipes table migration**:
```php
// From: 2015_12_21_233545_create_recipes_table.php
// To: 2025_01_01_000003_create_recipes_table.php (with modern syntax and consolidated foreign keys)

return new class extends Migration {
    public function up(): void {
        Schema::create('recipes', function (Blueprint $table) {
            $table->id();
            $table->string('name')->unique();
            $table->text('ingredients')->nullable();
            $table->text('instructions')->nullable();
            $table->text('notes')->nullable();
            $table->integer('servings')->nullable()->default(0);
            $table->dateTime('date_added')->nullable();
            $table->decimal('calories', 8, 2)->nullable();
            $table->decimal('fat', 8, 2)->nullable();
            $table->decimal('cholesterol', 8, 2)->nullable();
            $table->decimal('sodium', 8, 2)->nullable();
            $table->decimal('protein', 8, 2)->nullable();
            $table->boolean('marked')->nullable()->default(false);
            $table->foreignId('classification_id')->constrained()->cascadeOnDelete();
            $table->foreignId('source_id')->constrained()->cascadeOnDelete();
            $table->timestamps();
        });
    }
    
    public function down(): void {
        Schema::dropIfExists('recipes');
    }
};
```

### Models Adaptation Strategy

**Source**: [laravel-recipes-update/app/Models/](https://github.com/dougis-org/laravel-recipes-update/tree/main/app/Models)

**Key Differences**:

```php
// Laravel 5.2 (Old) - Recipe.php
class Recipe extends Model {
    use Eloquence; // Third-party trait for search
    
    protected $fillable = [...];
    protected $guarded = [];
    protected $searchableColumns = ['name', 'ingredients'];
    
    public function getSource() {
        return $this->hasOne('App\Models\Source', 'id', 'source_id');
    }
    
    public function meals() {
        return $this->belongsToMany('App\Models\Meal', 'recipe_meals');
    }
}

// Laravel 12 (Modern)
class Recipe extends Model {
    use HasFactory; // Laravel's built-in factory support
    
    protected $fillable = [...];
    
    public function source(): BelongsTo {
        return $this->belongsTo(Source::class);
    }
    
    public function meals(): BelongsToMany {
        return $this->belongsToMany(Meal::class);
    }
    
    public function scopeSearch($query, string $term) {
        return $query->where('name', 'like', "%{$term}%")
                    ->orWhere('ingredients', 'like', "%{$term}%");
    }
}
```

**Adaptation Checklist for Each Model**:
- [ ] Remove `Sofa\Eloquence\Eloquence` trait
- [ ] Add return type hints to all methods
- [ ] Replace `getX()` methods with `x()` relationship methods
- [ ] Change `hasOne()` calls to use full class names: `return $this->belongsTo(Source::class)`
- [ ] Replace Legacy namespace strings with class constants: `'App\Models\Source'` → `Source::class`
- [ ] Remove legacy getter/setter methods (`getName()`, `setName()`) - use accessors/mutators if needed
- [ ] Add native query scopes for search instead of Eloquence trait
- [ ] Keep `protected $fillable` array as-is
- [ ] Add `use HasFactory;` trait for testing

**Recipe Model Additions**:
```php
// Add these query scopes to Recipe model
public function scopeOrderByDateAdded($query) {
    return $query->orderBy('date_added', 'desc');
}

public function scopeOrderByName($query) {
    return $query->orderBy('name', 'asc');
}

public function scopeSearch($query, string $term) {
    return $query->where('name', 'like', "%{$term}%")
                ->orWhere('ingredients', 'like', "%{$term}%");
}
```

### Controllers Adaptation Strategy

**Source**: [laravel-recipes-update/app/Http/Controllers/](https://github.com/dougis-org/laravel-recipes-update/tree/main/app/Http/Controllers)

**RecipeController Changes**:

Legacy controller uses:
```php
// Legacy: Complex search handling with Eloquence trait
if ($sortField == 'search') {
    $recipes = Recipe::search($sortOrder)->paginate($displayCount);
}
```

Modern approach:
```php
// Modern: Use query scope with consistent interface
$recipes = Recipe::query()
    ->when($search, fn($q) => $q->search($search))
    ->when($sortField == 'name', fn($q) => $q->orderByName())
    ->when($sortField == 'date_added', fn($q) => $q->orderByDateAdded())
    ->paginate($displayCount);
```

**Key Logic to Preserve**:
- Default sort: `date_added` descending
- Default pagination: 30 per page
- Query parameters: `sortField`, `sortOrder`, `displayCount`, `search`
- Support "all" option to return all results unpaginated

**Adaptation Checklist**:
- [ ] Keep query parameter logic exactly as-is (legacy approach is proven and works)
- [ ] Add eager loading: `.with(['classification', 'source', 'meals', 'preparations', 'courses'])`
- [ ] Simplify search handling by using query scopes
- [ ] Update method return types and PHPDoc comments
- [ ] Remove unnecessary session/carbon imports if unused

### Views Adaptation Strategy

**Source**: [laravel-recipes-update/resources/views/](https://github.com/dougis-org/laravel-recipes-update/tree/main/resources/views)

**Layout Structure (to preserve functionality)**:
- Recipe index displays grid of recipes with search, sort, pagination
- Recipe show displays full recipe details
- Cookbook index lists all cookbooks
- Cookbook show displays recipes in cookbook ordered by classification

**CSS Class Conversion (Foundation → Tailwind)**:

```html
<!-- Foundation (Legacy) -->
<div class="row">
    <div class="large-3 medium-6 small-12 columns">
        <div class="recipe">...</div>
    </div>
</div>

<!-- Tailwind (Modern) -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <div class="recipe-card">...</div>
</div>
```

**Adaptation Checklist**:
- [ ] Preserve all HTML structure and logic flow
- [ ] Replace `.row` and `.columns` grid with Tailwind `grid` classes
- [ ] Replace `.btn .btn-primary` with Tailwind button utilities: `px-4 py-2 bg-blue-600 text-white rounded`
- [ ] Replace `.form-control` with Tailwind form input utilities
- [ ] Replace `.container` with `mx-auto px-4 max-w-7xl`
- [ ] Remove Foundation CSS file imports
- [ ] Use Blade components for repeated patterns

**Button Migration Example**:
```html
<!-- Foundation -->
<a href="#" class="btn btn-primary">View Recipe</a>

<!-- Tailwind (with component) -->
<x-button href="/recipes/{{ $recipe->id }}">View Recipe</x-button>

<!-- Component: resources/views/components/button.blade.php -->
<a {{ $attributes->class(['px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition']) }}>
    {{ $slot }}
</a>
```

### Testing Strategy

**Legacy App**: Minimal test coverage (only `ExampleTest.php`)

**Modern App Testing Requirements**:

1. **Feature Tests** (test user interactions):
   - RecipeIndexTest: Test listing, sorting, pagination, search
   - RecipeShowTest: Test recipe detail page
   - CookbookIndexTest: Test cookbook listing
   - CookbookShowTest: Test cookbook detail

2. **Unit Tests** (test model logic):
   - RecipeModelTest: Test query scopes, relationships
   - CookbookModelTest: Test recipe ordering relationship

**Example Feature Test**:
```php
// tests/Feature/RecipeIndexTest.php
test('can list recipes sorted by date added descending', function () {
    $recipes = Recipe::factory(3)->create();
    
    $response = $this->get('/recipes?sortField=date_added&sortOrder=desc');
    
    $response->assertStatus(200);
    $response->assertViewHas('recipes');
    // Verify sorting order...
});
```

### Database Seeding Strategy

**Legacy Seeding**: Minimal seeding (check DatabaseSeeder.php)

**Modern Approach**: Build comprehensive seeders and factories

**Seeders to Create**:
1. `ClassificationSeeder`: Create common classifications (Appetizer, Main, Dessert, etc.)
2. `SourceSeeder`: Create common sources (cookbook names, websites)
3. `MealSeeder`: Create meals (Breakfast, Lunch, Dinner, Snack)
4. `PreparationSeeder`: Create preparation methods
5. `CourseSeeder`: Create course types
6. `RecipeSeeder`: Use factory to create recipes with relationships

**RecipeFactory Example**:
```php
// database/factories/RecipeFactory.php
class RecipeFactory extends Factory {
    protected $model = Recipe::class;
    
    public function definition(): array {
        return [
            'name' => $this->faker->unique()->sentence(3),
            'ingredients' => implode("\n", $this->faker->sentences(5)),
            'instructions' => implode("\n", $this->faker->sentences(10)),
            'servings' => $this->faker->numberBetween(2, 12),
            'date_added' => $this->faker->dateTimeBetween('-2 years'),
            'classification_id' => Classification::inRandomOrder()->first()?->id,
            'source_id' => Source::inRandomOrder()->first()?->id,
        ];
    }
}
```

---



The application is complete when:

✅ **Functionality**:
- All recipe and cookbook listing/detail pages working
- Search functionality working on name and ingredients
- Sorting by name and date working (ascending/descending)
- Pagination working with configurable display count (20, 30, all)
- Default sort is by date_added descending, 30 per page
- All relationships displaying correctly

✅ **Technical**:
- Boots without errors on Laravel 12 with PHP 8.5+
- All tests passing with >80% code coverage
- No N+1 database queries (<10 queries per page)
- Database indexes optimized (name, date_added, foreign keys, full-text)
- Production build optimized and minified (CSS <100KB, JS <50KB)
- Fresh `php artisan migrate --seed` works from scratch
- CI/CD pipeline running successfully
- Code style checks passing (Laravel Pint)
- Static analysis passing (PHPStan level 5)

✅ **Security**:
- Security headers configured (CSP, HSTS, X-Frame-Options, etc.)
- Rate limiting active on all routes
- CSRF protection on all forms
- Input validation via Form Requests
- Mass assignment protection verified
- HTTPS enforced in production
- No SQL injection or XSS vulnerabilities
- Security testing completed

✅ **Frontend**:
- Modern design using Tailwind CSS 4+ consistently
- Responsive on mobile, tablet, desktop (all breakpoints tested)
- Alpine.js 3.14+ interactivity working (mobile menu, sort controls)
- No Bootstrap or Foundation classes remaining
- Lighthouse score >90 on all metrics (Performance, Accessibility, Best Practices, SEO)
- Browser compatibility verified (Chrome, Firefox, Safari, Edge - last 2 versions)
- Touch targets adequate (44x44px minimum)

✅ **Performance**:
- Page load times met (Index <2.0s, Detail <1.5s on 3G)
- Core Web Vitals met (FCP <1.8s, LCP <2.5s, CLS <0.1, FID <100ms)
- Database query times <50ms average
- Asset sizes within limits
- No layout shifts

✅ **Accessibility**:
- WCAG 2.1 AA compliance verified
- Keyboard navigable
- Screen reader compatible
- Semantic HTML throughout
- Alt text on all images
- Color contrast meets standards (4.5:1)
- Focus indicators on interactive elements

✅ **Code Quality**:
- Follows modern Laravel 12 conventions
- All code uses type hints and meaningful names
- Blade components reusable and DRY
- Controllers slim and focused (<50 lines per method)
- Models with proper relationships and scopes
- PSR-12 code style enforced
- No code duplication

✅ **Testing**:
- Feature tests cover all user flows
- Unit tests cover model logic
- Test coverage >80%
- Tests run in CI environment
- Performance tests verify no N+1 queries

✅ **Deployment & Operations**:
- Backup system configured and tested
- Disaster recovery plan documented
- Staging environment configured
- Deployment automation working
- Error monitoring configured
- Documentation complete (README, DEVELOPMENT, DEPLOYMENT, DISASTER_RECOVERY)
- Environment variables documented
- Fresh installation tested

✅ **User Experience**:
- Clean, intuitive interface
- Fast page loads (<2s)
- Smooth interactions
- Clear navigation
- Accessible to all users
- Error messages helpful and user-friendly

---

## Notes & Considerations

### Performance
- Use eager loading (`with()`) to prevent N+1 queries
- Add database indexes on `recipes.name`, `recipes.classification_id`, `recipes.date_added`
- Consider caching if recipe data is large and changes infrequently

### Scalability
- Current architecture supports thousands of recipes
- Consider pagination strategies if data grows significantly
- Search performance depends on database optimization

### Maintenance
- Keep Laravel and dependencies updated
- Monitor error logs regularly
- Verify Lighthouse score after updates
- Update documentation when features change

### Future Enhancement Ideas
- User authentication and bookmarking
- Recipe rating/review system
- Advanced search filters (by meal, preparation, course)
- Print recipe functionality
- Export to PDF or email
- Recipe submission form
- Admin interface for content management
