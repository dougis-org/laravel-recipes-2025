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

### Tech Stack (Latest Stable)
- **Backend**: Laravel 12.x, PHP 8.5+, Eloquent ORM
- **Frontend**: Tailwind CSS 4+, Alpine.js 3.x, Blade components
- **Build Tool**: Vite (modern, fast asset compilation)
- **Database**: MySQL/PostgreSQL with timestamped migrations
- **Testing**: PHPUnit 10+ or Pest 2.0+
- **Search**: Laravel Scout with database driver or native Eloquent scopes

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
    
    a. **2024_01_01_000001_create_classifications_table.php**
       - Source: [2015_12_21_233545_create_classifications_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_classifications_table.php)
       - Modernize: Use `$table->id()`, `$table->string('name')->unique()`, `$table->timestamps()`
    
    b. **2024_01_01_000002_create_sources_table.php**
       - Source: [2015_12_21_233545_create_sources_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_sources_table.php)
       - Modernize: Use modern Blueprint methods
    
    c. **2024_01_01_000003_create_recipes_table.php**
       - Source: [2015_12_21_233545_create_recipes_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_recipes_table.php)
       - Update: Change `string` columns to `text` where appropriate (ingredients, instructions, notes)
       - Update: Change nutrition columns from string to decimal/float
       - Update: Add inline foreign key definitions for classification_id, source_id
       - Key columns: id, name (unique), ingredients (text), instructions (text), notes (text, nullable), servings (int, nullable), classification_id, source_id, date_added (dateTime), calories (decimal), fat (decimal), cholesterol (decimal), sodium (decimal), protein (decimal), marked (boolean), timestamps
    
    d. **2024_01_01_000004_create_meals_table.php**
       - Source: [2015_12_21_233545_create_meals_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_meals_table.php)
       - Modernize: Use modern Blueprint methods
    
    e. **2024_01_01_000005_create_preparations_table.php**
       - Source: [2015_12_21_233545_create_preparations_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_preparations_table.php)
       - Modernize: Use modern Blueprint methods
    
    f. **2024_01_01_000006_create_courses_table.php**
       - Source: [2015_12_21_233545_create_courses_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_courses_table.php)
       - Modernize: Use modern Blueprint methods
    
    g. **2024_01_01_000007_create_cookbooks_table.php**
       - Source: [2015_12_21_233545_create_cookbooks_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_cookbooks_table.php)
       - Modernize: Use modern Blueprint methods
    
    h. **2024_01_01_000008_create_recipe_meals_table.php**
       - Source: [2015_12_21_233545_create_recipe_meals_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_recipe_meals_table.php)
       - Update: Add inline foreign keys with cascading deletes
    
    i. **2024_01_01_000009_create_recipe_preparations_table.php**
       - Source: [2015_12_21_233545_create_recipe_preparations_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_recipe_preparations_table.php)
       - Update: Add inline foreign keys with cascading deletes
    
    j. **2024_01_01_000010_create_recipe_courses_table.php**
       - Source: [2015_12_21_233545_create_recipe_courses_table.php](https://github.com/dougis-org/laravel-recipes-update/blob/main/database/migrations/2015_12_21_233545_create_recipe_courses_table.php)
       - Update: Add inline foreign keys with cascading deletes
    
    k. **2024_01_01_000011_create_cookbook_recipes_table.php**
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

12. **Create/Modernize Eloquent Models** (in `app/Models/`)
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

## Phase 13: Error Handling & User Experience

**Goals**: Implement error pages and improve user experience

### Tasks

50. **Create Error Views** (in `resources/views/errors/`)
    
    a. **404.blade.php**: Not found error
    b. **500.blade.php**: Server error
    c. **419.blade.php**: Session expired (CSRF token)
    d. **429.blade.php**: Too many requests

51. **Configure Exception Handler** (`app/Exceptions/Handler.php`)
    - Set up proper error logging
    - Return user-friendly error responses
    - Log errors to storage/logs/

52. **Add Flash Messages**
    - Implement success/error flash messages
    - Display in layout header/footer area
    - Auto-dismiss after 5 seconds with Alpine.js

53. **Implement 404 Handling**
    - Test 404 pages in browser
    - Verify styling matches application

**Success Criteria**:
- ✅ 404 error displays gracefully
- ✅ 500 error displays gracefully
- ✅ Error pages styled consistently with app
- ✅ User feedback messages display correctly
- ✅ No raw exception messages shown to users

---

## Phase 14: Accessibility & Performance

**Goals**: Ensure application is accessible and performant

### Tasks

54. **Implement Accessibility**
    - Add alt text to images
    - Use semantic HTML (header, nav, main, footer, section, article)
    - Add ARIA labels where needed
    - Ensure form inputs have associated labels
    - Test keyboard navigation
    - Verify color contrast meets WCAG AA standards

55. **Performance Optimization**
    - Add database indexes on frequently queried columns: name, classification_id, date_added
    - Verify queries use eager loading: `with('classification', 'source')`
    - Test with production build: `npm run build`
    - Verify lazy loading of images if present
    - Check Lighthouse score (target >90 on all metrics)

56. **Test Responsive Design**
    - Test on mobile (320px), tablet (768px), desktop (1024px+)
    - Verify touch targets are adequate (minimum 44px)
    - Test navigation on all screen sizes
    - Verify forms are usable on mobile

**Success Criteria**:
- ✅ Application is keyboard navigable
- ✅ Alt text present on all images
- ✅ Semantic HTML used throughout
- ✅ Lighthouse score >90 on performance and accessibility
- ✅ Responsive design works on all screen sizes
- ✅ Mobile experience is smooth and usable

---

## Phase 15: Documentation & Deployment

**Goals**: Document the application and prepare for deployment

### Tasks

57. **Update Documentation**
    - Update `README.md` with:
      - Project overview
      - Tech stack (Laravel 12, Tailwind CSS 4+, Alpine.js 3, Vite, PHP 8.5+, Node.js 25+)
      - Setup instructions
      - Database schema overview
      - Feature documentation
    - Update `.github/copilot-instructions.md` with modern patterns (already done in this project)
    - Create `DEVELOPMENT.md` with:
      - Development workflow (running dev server, building assets, running tests)
      - Debugging tips
      - Common tasks (creating models, migrations, seeders)

58. **Configure Environment**
    - Create `.env.example` with all required variables
    - Document each environment variable's purpose
    - Set production values in deployment environment

59. **Test Fresh Installation**
    - Clone repository and run setup from scratch:
      - `git clone <repo>`
      - `composer install`
      - `npm install`
      - `cp .env.example .env`
      - `php artisan key:generate`
      - `php artisan migrate --seed`
      - `npm run build`
      - Verify application runs correctly

60. **Deployment Checklist**
    - [ ] All tests pass
    - [ ] No console errors or warnings
    - [ ] Production build completes successfully
    - [ ] `.env` configured for production
    - [ ] Database migrations ready
    - [ ] Error handling configured
    - [ ] Logging configured
    - [ ] CSRF protection enabled
    - [ ] Security headers configured
    - [ ] CORS configured if needed

**Success Criteria**:
- ✅ README updated with setup instructions
- ✅ Development documentation complete
- ✅ Fresh installation works from scratch
- ✅ All environment variables documented
- ✅ Deployment process clear and tested

---

## Implementation Checklist

### Phase 1: Project Setup
- [ ] Laravel 12 project initialized
- [ ] Database configured
- [ ] Version control initialized

### Phase 2: Frontend Stack
- [ ] Tailwind CSS 4 installed and configured
- [ ] Alpine.js 3 installed
- [ ] Vite build pipeline working
- [ ] npm run dev and npm run build functional

### Phase 3: Database & Models
- [ ] All migrations created and run successfully
- [ ] All Eloquent models created with relationships
- [ ] Models tested in Tinker

### Phase 4: Search
- [ ] Search implementation chosen (Scout or native scopes)
- [ ] Search functionality working

### Phase 5: Controllers & Routing
- [ ] RecipeController created with index and show methods
- [ ] CookbookController created with index and show methods
- [ ] Routes defined and tested
- [ ] Default route redirects correctly

### Phase 6: Layout & Components
- [ ] Base layout created
- [ ] All reusable components created
- [ ] Navigation working
- [ ] Responsive design verified

### Phase 7: Recipe Views
- [ ] Recipe index view created with search, sort, pagination
- [ ] Recipe detail view created
- [ ] Recipe card component created
- [ ] All features working

### Phase 8: Cookbook Views
- [ ] Cookbook index view created
- [ ] Cookbook detail view created
- [ ] Recipe ordering verified

### Phase 9: Alpine.js Interactivity
- [ ] Mobile menu working
- [ ] Sort toggle working
- [ ] Display count selector working
- [ ] Hover effects working

### Phase 10: Asset Pipeline
- [ ] Development build working
- [ ] Production build working
- [ ] Assets optimized

### Phase 11: Database Seeding
- [ ] All seeders created
- [ ] Factories created
- [ ] Database seeded successfully
- [ ] Test data displays correctly

### Phase 12: Testing
- [ ] Feature tests created and passing
- [ ] Unit tests created and passing
- [ ] Performance verified (no N+1 queries)
- [ ] All tests pass: `php artisan test`

### Phase 13: Error Handling
- [ ] Error views created
- [ ] Exception handler configured
- [ ] Flash messages working
- [ ] Error pages displaying correctly

### Phase 14: Accessibility & Performance
- [ ] Accessibility verified
- [ ] Lighthouse score >90
- [ ] Responsive design tested
- [ ] Performance optimized

### Phase 15: Documentation & Deployment
- [ ] Documentation updated
- [ ] Fresh installation tested
- [ ] Deployment checklist completed
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
// To: 2024_01_01_000002_create_recipes_table.php (with modern syntax and consolidated foreign keys)

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
- Boots without errors on Laravel 12
- All tests passing
- No N+1 database queries
- Production build optimized and minified
- Fresh `php artisan migrate --seed` works from scratch

✅ **Frontend**:
- Modern design using Tailwind CSS 4 consistently
- Responsive on mobile, tablet, desktop
- Alpine.js interactivity working (mobile menu, sort controls)
- No Bootstrap classes remaining
- Lighthouse score >90

✅ **Code Quality**:
- Follows modern Laravel 12 conventions
- All code uses type hints and meaningful names
- Blade components reusable and DRY
- Controllers slim and focused
- Models with proper relationships and scopes

✅ **User Experience**:
- Clean, intuitive interface
- Fast page loads
- Smooth interactions
- Clear navigation
- Accessible to all users

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
