# Milestone 3 - Database & Models

**Goal**: Create database schema and Eloquent models reflecting the data model

**Estimated Total Effort**: 8-12 hours
**Can Start**: After M1-2 (Database configured)
**Parallel Capacity**: 4-6 agents (high parallelization for migrations and models)

---

## Migration Issues (Wave 1: Independent Tables)

### M3-1 (#250): Create Classifications Table Migration
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30 min)
**Depends On**: M1-2 (Database config)
**Blocks**: M3-8 (Recipes table), M3-14 (Classification model)

**Description**:
Create migration for classifications lookup table.

**Acceptance Criteria**:
- [ ] Created migration: `2025_01_01_000001_create_classifications_table.php`
- [ ] Migration includes:
  - [ ] `id` (primary key, auto-increment)
  - [ ] `name` (string, unique)
  - [ ] `timestamps` (created_at, updated_at)
- [ ] Migration uses modern syntax: `return new class extends Migration`
- [ ] Uses `$table->id()` for primary key
- [ ] Includes `down()` method with `Schema::dropIfExists()`
- [ ] Migration runs successfully: `php artisan migrate`
- [ ] Migration can be rolled back: `php artisan migrate:rollback`

**Files to Create**:
- `database/migrations/2025_01_01_000001_create_classifications_table.php`

**Testing**:
```bash
php artisan migrate
php artisan db:show classifications  # Verify table exists
php artisan migrate:rollback
php artisan migrate  # Re-run to test idempotency
```

**Story**:
```
As a developer
I want to create the classifications table
So that recipes can be categorized by type (Appetizer, Main Course, etc.)
```

---

### M3-2 (#283): Create Sources Table Migration
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30 min)
**Depends On**: M1-2 (Database config)
**Blocks**: M3-8 (Recipes table), M3-15 (Source model)

**Description**:
Create migration for sources lookup table.

**Acceptance Criteria**:
- [ ] Created migration: `2025_01_01_000002_create_sources_table.php`
- [ ] Migration includes:
  - [ ] `id` (primary key)
  - [ ] `name` (string, unique)
  - [ ] `timestamps`
- [ ] Modern migration syntax
- [ ] Migration runs and rolls back successfully

**Files to Create**:
- `database/migrations/2025_01_01_000002_create_sources_table.php`

**Testing**: Same as M3-1

**Story**:
```
As a developer
I want to create the sources table
So that recipes can reference their origin (cookbook, website, etc.)
```

---

### M3-3 (#248): Create Meals Table Migration
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30 min)
**Depends On**: M1-2 (Database config)
**Blocks**: M3-9 (recipe_meals pivot), M3-17 (Meal model)

**Description**:
Create migration for meals lookup table.

**Acceptance Criteria**:
- [ ] Created migration: `2025_01_01_000004_create_meals_table.php`
- [ ] Migration includes standard fields (id, name, timestamps)
- [ ] Migration runs and rolls back successfully

**Files to Create**:
- `database/migrations/2025_01_01_000004_create_meals_table.php`

**Testing**: Same as M3-1

**Story**:
```
As a developer
I want to create the meals table
So that recipes can be tagged by meal type (Breakfast, Lunch, Dinner)
```

---

### M3-4 (#247): Create Preparations Table Migration
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30 min)
**Depends On**: M1-2 (Database config)
**Blocks**: M3-10 (recipe_preparations pivot), M3-18 (Preparation model)

**Description**:
Create migration for preparations lookup table.

**Acceptance Criteria**:
- [ ] Created migration: `2025_01_01_000005_create_preparations_table.php`
- [ ] Migration includes standard fields (id, name, timestamps)
- [ ] Migration runs and rolls back successfully

**Files to Create**:
- `database/migrations/2025_01_01_000005_create_preparations_table.php`

**Testing**: Same as M3-1

**Story**:
```
As a developer
I want to create the preparations table
So that recipes can specify preparation methods (Baked, Fried, etc.)
```

---

### M3-5 (#256): Create Courses Table Migration
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30 min)
**Depends On**: M1-2 (Database config)
**Blocks**: M3-11 (recipe_courses pivot), M3-19 (Course model)

**Description**:
Create migration for courses lookup table.

**Acceptance Criteria**:
- [ ] Created migration: `2025_01_01_000006_create_courses_table.php`
- [ ] Migration includes standard fields (id, name, timestamps)
- [ ] Migration runs and rolls back successfully

**Files to Create**:
- `database/migrations/2025_01_01_000006_create_courses_table.php`

**Testing**: Same as M3-1

**Story**:
```
As a developer
I want to create the courses table
So that recipes can specify course type (Appetizer, Main, Dessert, etc.)
```

---

### M3-6 (#252): Create Cookbooks Table Migration
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30 min)
**Depends On**: M1-2 (Database config)
**Blocks**: M3-12 (cookbook_recipes pivot), M3-16 (Cookbook model)

**Description**:
Create migration for cookbooks table.

**Acceptance Criteria**:
- [ ] Created migration: `2025_01_01_000007_create_cookbooks_table.php`
- [ ] Migration includes standard fields (id, name, timestamps)
- [ ] Migration runs and rolls back successfully

**Files to Create**:
- `database/migrations/2025_01_01_000007_create_cookbooks_table.php`

**Testing**: Same as M3-1

**Story**:
```
As a developer
I want to create the cookbooks table
So that recipes can be organized into collections
```

---

## Migration Issues (Wave 2: Recipes Table)

### M3-8 (#279): Create Recipes Table Migration
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:medium` (1 hour)
**Depends On**: M3-1 (Classifications), M3-2 (Sources)
**Blocks**: M3-9, M3-10, M3-11, M3-12 (pivot tables), M3-14 (Recipe model)

**Description**:
Create migration for recipes main table with all fields and foreign keys.

**Acceptance Criteria**:
- [ ] Created migration: `2025_01_01_000003_create_recipes_table.php`
- [ ] Migration includes all fields:
  - [ ] `id`, `name` (unique), `timestamps`
  - [ ] `ingredients` (text, nullable)
  - [ ] `instructions` (text, nullable)
  - [ ] `notes` (text, nullable)
  - [ ] `servings` (integer, nullable, default 0)
  - [ ] `date_added` (dateTime, nullable)
  - [ ] Nutrition fields (decimal 8,2, nullable): calories, fat, cholesterol, sodium, protein
  - [ ] `marked` (boolean, nullable, default false)
  - [ ] Foreign keys: `classification_id`, `source_id` with constraints and cascade on delete
- [ ] Migration runs successfully
- [ ] Foreign key constraints verified

**Files to Create**:
- `database/migrations/2025_01_01_000003_create_recipes_table.php`

**Testing**:
```bash
php artisan migrate
# Try to insert a recipe with invalid classification_id (should fail)
# Try to delete a classification that has recipes (should cascade)
```

**Story**:
```
As a developer
I want to create the recipes table with all fields and relationships
So that recipe data can be stored with proper foreign key constraints
```

---

## Migration Issues (Wave 3: Pivot Tables)

### M3-9 (#280): Create Recipe-Meals Pivot Table Migration
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30 min)
**Depends On**: M3-8 (Recipes), M3-3 (Meals)
**Blocks**: M3-14 (Recipe model relationships)

**Description**:
Create pivot table for many-to-many relationship between recipes and meals.

**Acceptance Criteria**:
- [ ] Created migration: `2025_01_01_000008_create_recipe_meals_table.php`
- [ ] Migration includes:
  - [ ] `id` (primary key)
  - [ ] `recipe_id` (foreign key to recipes, cascade on delete)
  - [ ] `meal_id` (foreign key to meals, cascade on delete)
  - [ ] `timestamps`
  - [ ] Compound unique index on `recipe_id, meal_id`
- [ ] Migration runs successfully

**Files to Create**:
- `database/migrations/2025_01_01_000008_create_recipe_meals_table.php`

**Testing**: Verify table created and foreign keys work

**Story**:
```
As a developer
I want a pivot table linking recipes to meals
So that recipes can be tagged with multiple meal types
```

---

### M3-10 (#254): Create Recipe-Preparations Pivot Table Migration
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30 min)
**Depends On**: M3-8 (Recipes), M3-4 (Preparations)
**Blocks**: M3-14 (Recipe model relationships)

**Description**:
Create pivot table for recipes and preparations many-to-many relationship.

**Acceptance Criteria**:
- [ ] Created migration: `2025_01_01_000009_create_recipe_preparations_table.php`
- [ ] Includes id, recipe_id, preparation_id, timestamps, foreign keys, compound index
- [ ] Migration runs successfully

**Files to Create**:
- `database/migrations/2025_01_01_000009_create_recipe_preparations_table.php`

**Testing**: Same as M3-9

**Story**:
```
As a developer
I want a pivot table linking recipes to preparations
So that recipes can specify multiple preparation methods
```

---

### M3-11 (#258): Create Recipe-Courses Pivot Table Migration
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30 min)
**Depends On**: M3-8 (Recipes), M3-5 (Courses)
**Blocks**: M3-14 (Recipe model relationships)

**Description**:
Create pivot table for recipes and courses many-to-many relationship.

**Acceptance Criteria**:
- [ ] Created migration: `2025_01_01_000010_create_recipe_courses_table.php`
- [ ] Includes id, recipe_id, course_id, timestamps, foreign keys, compound index
- [ ] Migration runs successfully

**Files to Create**:
- `database/migrations/2025_01_01_000010_create_recipe_courses_table.php`

**Testing**: Same as M3-9

**Story**:
```
As a developer
I want a pivot table linking recipes to courses
So that recipes can belong to multiple course types
```

---

### M3-12 (#257): Create Cookbook-Recipes Pivot Table Migration
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30 min)
**Depends On**: M3-8 (Recipes), M3-6 (Cookbooks)
**Blocks**: M3-14, M3-16 (Model relationships)

**Description**:
Create pivot table for cookbooks and recipes many-to-many relationship.

**Acceptance Criteria**:
- [ ] Created migration: `2025_01_01_000011_create_cookbook_recipes_table.php`
- [ ] Includes id, cookbook_id, recipe_id, timestamps, foreign keys, compound index
- [ ] Migration runs successfully

**Files to Create**:
- `database/migrations/2025_01_01_000011_create_cookbook_recipes_table.php`

**Testing**: Same as M3-9

**Story**:
```
As a developer
I want a pivot table linking cookbooks to recipes
So that recipes can be organized into multiple cookbooks
```

---

## Migration Issues (Wave 4: Indexes)

### M3-13 (#261): Create Database Indexes Migration
**Type**: `type:performance`
**Priority**: `P2`
**Effort**: `effort:medium` (1 hour)
**Depends On**: M3-8 (Recipes), M3-6 (Cookbooks), M3-9, M3-10, M3-11, M3-12 (Pivots)
**Blocks**: None

**Description**:
Add database indexes for query optimization.

**Acceptance Criteria**:
- [ ] Created migration: `2025_01_01_000012_add_database_indexes.php`
- [ ] Indexes on recipes table:
  - [ ] Single: name, date_added, classification_id, source_id, marked
  - [ ] Compound: [classification_id, name], [source_id, name], [date_added, id]
  - [ ] Full-text: [name, ingredients] (MySQL only)
- [ ] Index on cookbooks: name
- [ ] Indexes on pivot tables as documented in BUILD_PLAN
- [ ] Migration runs successfully
- [ ] Verify indexes created: `SHOW INDEXES FROM recipes;` (MySQL)

**Files to Create**:
- `database/migrations/2025_01_01_000012_add_database_indexes.php`

**Testing**:
```bash
php artisan migrate
# MySQL: SHOW INDEXES FROM recipes;
# PostgreSQL: \d recipes
# Verify all indexes listed
```

**Story**:
```
As a developer
I want database indexes on frequently queried columns
So that queries perform efficiently as data grows
```

---

## Model Issues (Can mostly parallelize)

### M3-14 (#266): Create Recipe Model with Relationships
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:medium` (1-2 hours)
**Depends On**: M3-8 (Recipes table), M3-9, M3-10, M3-11, M3-12 (Pivots)
**Blocks**: M4-1 (Search scope), M5-1 (RecipeController)

**Description**:
Create Recipe model with all relationships, fillable attributes, and query scopes.

**Acceptance Criteria**:
- [ ] Created model: `app/Models/Recipe.php`
- [ ] Includes `use HasFactory` trait
- [ ] Fillable attributes defined (all recipe fields except id, timestamps)
- [ ] Relationships defined:
  - [ ] `classification()` - belongsTo(Classification::class)
  - [ ] `source()` - belongsTo(Source::class)
  - [ ] `meals()` - belongsToMany(Meal::class, 'recipe_meals')
  - [ ] `preparations()` - belongsToMany(Preparation::class, 'recipe_preparations')
  - [ ] `courses()` - belongsToMany(Course::class, 'recipe_courses')
  - [ ] `cookbooks()` - belongsToMany(Cookbook::class, 'cookbook_recipes')
- [ ] Query scopes added:
  - [ ] `scopeOrderByDateAdded()` - orders by date_added desc
  - [ ] `scopeOrderByName()` - orders by name asc
- [ ] Casts defined:
  - [ ] `date_added` => `datetime`
  - [ ] `marked` => `boolean`
  - [ ] Nutrition fields => `decimal:2`

**Files to Create**:
- `app/Models/Recipe.php`

**Testing (via Tinker)**:
```php
php artisan tinker
>>> Recipe::factory()->count(1)->create();
>>> $recipe = Recipe::first();
>>> $recipe->classification; // Should eager load
>>> $recipe->meals()->attach(1);
>>> $recipe->meals; // Should return collection
```

**Story**:
```
As a developer
I want a Recipe model with all relationships
So that I can easily query and manipulate recipe data with Eloquent
```

---

### M3-15 (#282): Create Classification Model
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:small` (30 min)
**Depends On**: M3-1 (Classifications table)
**Blocks**: M3-14 (Recipe relationships)

**Description**:
Create Classification model with relationships.

**Acceptance Criteria**:
- [ ] Created model: `app/Models/Classification.php`
- [ ] Includes HasFactory trait
- [ ] Fillable: ['name']
- [ ] Relationship: `recipes()` - hasMany(Recipe::class)

**Files to Create**:
- `app/Models/Classification.php`

**Testing**: Tinker - create classification, access recipes relationship

**Story**:
```
As a developer
I want a Classification model
So that I can manage recipe categories
```

---

### M3-16 (#260): Create Source Model
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:small` (30 min)
**Depends On**: M3-2 (Sources table)
**Blocks**: M3-14 (Recipe relationships)

**Description**:
Create Source model with relationships.

**Acceptance Criteria**:
- [ ] Created model: `app/Models/Source.php`
- [ ] Includes HasFactory trait
- [ ] Fillable: ['name']
- [ ] Relationship: `recipes()` - hasMany(Recipe::class)

**Files to Create**:
- `app/Models/Source.php`

**Testing**: Same as M3-15

**Story**:
```
As a developer
I want a Source model
So that I can track where recipes come from
```

---

### M3-17 (#285): Create Meal Model
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:small` (30 min)
**Depends On**: M3-3 (Meals table), M3-9 (Pivot)
**Blocks**: M3-14 (Recipe relationships)

**Description**:
Create Meal model with relationships.

**Acceptance Criteria**:
- [ ] Created model: `app/Models/Meal.php`
- [ ] Includes HasFactory trait
- [ ] Fillable: ['name']
- [ ] Relationship: `recipes()` - belongsToMany(Recipe::class, 'recipe_meals')

**Files to Create**:
- `app/Models/Meal.php`

**Testing**: Same as M3-15

**Story**:
```
As a developer
I want a Meal model
So that recipes can be tagged by meal type
```

---

### M3-18 (#294): Create Preparation Model
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:small` (30 min)
**Depends On**: M3-4 (Preparations table), M3-10 (Pivot)
**Blocks**: M3-14 (Recipe relationships)

**Description**:
Create Preparation model with relationships.

**Acceptance Criteria**:
- [ ] Created model: `app/Models/Preparation.php`
- [ ] Includes HasFactory trait
- [ ] Fillable: ['name']
- [ ] Relationship: `recipes()` - belongsToMany(Recipe::class, 'recipe_preparations')

**Files to Create**:
- `app/Models/Preparation.php`

**Testing**: Same as M3-15

**Story**:
```
As a developer
I want a Preparation model
So that recipes can specify preparation methods
```

---

### M3-19 (#284): Create Course Model
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:small` (30 min)
**Depends On**: M3-5 (Courses table), M3-11 (Pivot)
**Blocks**: M3-14 (Recipe relationships)

**Description**:
Create Course model with relationships.

**Acceptance Criteria**:
- [ ] Created model: `app/Models/Course.php`
- [ ] Includes HasFactory trait
- [ ] Fillable: ['name']
- [ ] Relationship: `recipes()` - belongsToMany(Recipe::class, 'recipe_courses')

**Files to Create**:
- `app/Models/Course.php`

**Testing**: Same as M3-15

**Story**:
```
As a developer
I want a Course model
So that recipes can specify which course they belong to
```

---

### M3-20 (#296): Create Cookbook Model with Ordered Recipes
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:medium` (1 hour)
**Depends On**: M3-6 (Cookbooks table), M3-12 (Pivot), M3-14 (Recipe model)
**Blocks**: M8-1 (Cookbook views)

**Description**:
Create Cookbook model with recipes relationship ordered by classification and name.

**Acceptance Criteria**:
- [ ] Created model: `app/Models/Cookbook.php`
- [ ] Includes HasFactory trait
- [ ] Fillable: ['name']
- [ ] Relationship: `recipes()` - belongsToMany with ordering:
  ```php
  return $this->belongsToMany(Recipe::class, 'cookbook_recipes')
      ->join('classifications', 'recipes.classification_id', '=', 'classifications.id')
      ->orderBy('classifications.name')
      ->orderBy('recipes.name')
      ->select('recipes.*');
  ```

**Files to Create**:
- `app/Models/Cookbook.php`

**Testing (Tinker)**:
```php
$cookbook = Cookbook::factory()->create();
$cookbook->recipes()->attach([1,2,3]);
$cookbook->recipes; // Should be ordered by classification, then name
```

**Story**:
```
As a developer
I want a Cookbook model with ordered recipes
So that cookbook recipes display in the correct order
```

---

## Summary

**Total Issues**: 20 issues
**Parallel Capacity**: High (4-6 agents)
**Critical Path**: M3-1, M3-2 → M3-8 → M3-9,10,11,12 → M3-14 → M4-1, M5-1
**Estimated Milestone Completion**: 8-12 hours with 4-6 agents, 20-30 hours solo

**Parallel Execution Strategy (Waves)**:

**Wave 1** (6 agents in parallel):
- Agent 1: M3-1 (Classifications)
- Agent 2: M3-2 (Sources)
- Agent 3: M3-3 (Meals)
- Agent 4: M3-4 (Preparations)
- Agent 5: M3-5 (Courses)
- Agent 6: M3-6 (Cookbooks)

**Wave 2** (1 agent, must wait for wave 1):
- Agent 1: M3-8 (Recipes) - depends on M3-1, M3-2

**Wave 3** (4 agents in parallel after wave 2):
- Agent 1: M3-9 (recipe_meals pivot)
- Agent 2: M3-10 (recipe_preparations pivot)
- Agent 3: M3-11 (recipe_courses pivot)
- Agent 4: M3-12 (cookbook_recipes pivot)

**Wave 4** (6 agents in parallel after wave 1):
- Agent 1: M3-15 (Classification model)
- Agent 2: M3-16 (Source model)
- Agent 3: M3-17 (Meal model)
- Agent 4: M3-18 (Preparation model)
- Agent 5: M3-19 (Course model)
- Agent 6: M3-13 (Indexes) - can start after wave 3

**Wave 5** (2 agents after wave 3 and 4):
- Agent 1: M3-14 (Recipe model)
- Agent 2: M3-20 (Cookbook model)

**Success Criteria**:
All database tables created with proper relationships and constraints. All Eloquent models created with relationships. Database optimized with indexes. Models tested via Tinker.
