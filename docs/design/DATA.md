# Data Architecture & Model Design

## Entity Relationships

The application uses a relational model with many-to-many relationships through explicit pivot tables:

- **Recipe** → belongs to one **Classification** & one **Source**
- **Recipe** ↔ **Meal** (many-to-many via `recipe_meals`)
- **Recipe** ↔ **Preparation** (many-to-many via `recipe_preparations`)
- **Recipe** ↔ **Course** (many-to-many via `recipe_courses`)
- **Cookbook** ↔ **Recipe** (many-to-many via `cookbook_recipes`, ordered by classification then name)

## Core Entities

### Recipe
- Belongs to one Classification (required)
- Belongs to one Source (required)
- Has many-to-many relationships with Meals, Preparations, Courses
- Included in many-to-many relationship with Cookbooks
- Searchable fields: name, ingredients
- Timestamps: created_at, updated_at

### Cookbook
- Has many-to-many relationships with Recipes
- Recipes ordered by classification name then recipe name
- Timestamps: created_at, updated_at

### Classification
- Groups recipes by type (e.g., Appetizer, Main Course, Dessert)
- One-to-many relationship with Recipes
- Timestamps: created_at, updated_at

### Source
- Origin/reference for recipes (e.g., cookbook title, website)
- One-to-many relationship with Recipes
- Timestamps: created_at, updated_at

### Meal
- Type of meal (e.g., Breakfast, Lunch, Dinner)
- Many-to-many relationship with Recipes via `recipe_meals`
- Timestamps: created_at, updated_at

### Preparation
- Preparation method/type (e.g., Baked, Fried, Raw)
- Many-to-many relationship with Recipes via `recipe_preparations`
- Timestamps: created_at, updated_at

### Course
- Course type (e.g., Appetizer, Salad, Main, Dessert)
- Many-to-many relationship with Recipes via `recipe_courses`
- Timestamps: created_at, updated_at

## Database Structure

### Key Pattern
All many-to-many relationships use explicit pivot tables in `database/migrations/`:
- `recipe_meals`: Links recipes to meals
- `recipe_preparations`: Links recipes to preparations
- `recipe_courses`: Links recipes to courses
- `cookbook_recipes`: Links cookbooks to recipes with ordering

### Foreign Keys
- All relationships use foreign key constraints via `$table->foreign()`
- Cascading deletes configured where appropriate
- Migrations can combine table creation with foreign keys or keep them separate

### Timestamps
- All models include `public $timestamps = true;` by default
- Tracks creation and modification dates automatically

## Model Conventions

### Relationships
Eloquent models use modern relationship conventions:

```php
// Example: Recipe.php
public function source()
{
    return $this->belongsTo(Source::class, 'source_id');
}

public function classification()
{
    return $this->belongsTo(Classification::class, 'classification_id');
}

public function meals()
{
    return $this->belongsToMany(Meal::class, 'recipe_meals');
}

public function cookbooks()
{
    return $this->belongsToMany(Cookbook::class, 'cookbook_recipes');
}
```

Access relationships as properties: `$recipe->source` or `$recipe->source()->get()`

### Fillable Attributes
Each model defines `protected $fillable = [];` for mass assignment:
```php
protected $fillable = ['name', 'ingredients', 'classification_id', 'source_id'];
```

### Searchability
Models support search through:
- **Laravel Scout**: Search abstraction layer with Meilisearch, Algolia, or database driver
- **Eloquent Query Scopes**: Custom query methods for filtering and searching
- Example: `Recipe::search('pasta')->get()` or `Recipe::whereSearchable('pasta')->get()`

## Pivot Tables

### Explicit Pivot Table Structure
Each many-to-many relationship has an explicit pivot table:

#### recipe_meals
- `id`: Primary key
- `recipe_id`: Foreign key to recipes
- `meal_id`: Foreign key to meals
- `created_at`, `updated_at`: Timestamps

#### recipe_preparations
- `id`: Primary key
- `recipe_id`: Foreign key to recipes
- `preparation_id`: Foreign key to preparations
- `created_at`, `updated_at`: Timestamps

#### recipe_courses
- `id`: Primary key
- `recipe_id`: Foreign key to recipes
- `course_id`: Foreign key to courses
- `created_at`, `updated_at`: Timestamps

#### cookbook_recipes
- `id`: Primary key
- `cookbook_id`: Foreign key to cookbooks
- `recipe_id`: Foreign key to recipes
- Order columns (for sorting by classification then name)
- `created_at`, `updated_at`: Timestamps

## Default Behaviors

### Default Route
- `/` → redirects to recipe index with sorting params:
  - `sortField=date_added` (or creation date field)
  - `sortOrder=desc` (newest first)
  - `displayCount=30` (items per page)

### Sorting & Filtering
- Controllers support query parameters: `sortField`, `sortOrder`, `displayCount`
- Sorting field names map to database column names
- Order: `asc` for ascending, `desc` for descending
- Display count: Number of items per page

### Cookbook Recipe Ordering
- Recipes within a cookbook ordered by:
  1. Classification name (alphabetical)
  2. Recipe name (alphabetical)
- Maintained through pivot table ordering or application logic

## Migration File Naming

All migrations follow consistent timestamp prefix pattern:
- Format: `YYYY_MM_DD_HHMMSS_action_table.php`
- Example: `2025_01_15_100000_create_recipes_table.php`
- Foreign key migrations: `add_foreign_keys_to_table.php` or combined with creation
