# Milestone 11 - Database Seeding

**Goal**: Create seeders and factories for all models to enable testing and development

**Estimated Total Effort**: 6-8 hours
**Can Start**: After M3-15 through M3-20 complete (all models)
**Parallel Capacity**: 4-5 agents (excellent parallelization possible)

---

## Issues

### M11-1 (#343): Create ClassificationSeeder
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30 min)
**Depends On**: M3-15 (Classification model)
**Blocks**: M11-8 (DatabaseSeeder)

**Description**:
Create seeder to populate common recipe classifications.

**Acceptance Criteria**:
- [ ] Created `database/seeders/ClassificationSeeder.php`:
  ```php
  class ClassificationSeeder extends Seeder
  {
      public function run(): void
      {
          $classifications = [
              'Appetizer',
              'Salad',
              'Soup',
              'Main Dish',
              'Side Dish',
              'Dessert',
              'Beverage',
              'Bread',
              'Breakfast',
              'Snack',
          ];

          foreach ($classifications as $name) {
              Classification::firstOrCreate(['name' => $name]);
          }
      }
  }
  ```
- [ ] Uses `firstOrCreate` to prevent duplicates
- [ ] Includes common classifications
- [ ] Alphabetically ordered (optional)
- [ ] Can be run multiple times safely

**Files to Create/Modify**:
- `database/seeders/ClassificationSeeder.php` (create)

**Testing**:
```bash
# Run seeder
php artisan db:seed --class=ClassificationSeeder

# Verify data
php artisan tinker
>>> Classification::count()
>>> Classification::all()->pluck('name')

# Run again to test idempotency
php artisan db:seed --class=ClassificationSeeder
>>> Classification::count() // Should still be 10
```

**Story**:
```
As a developer
I want common classifications seeded
So that I have realistic data for development and testing
```

---

### M11-2 (#344): Create SourceSeeder
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30 min)
**Depends On**: M3-16 (Source model)
**Blocks**: M11-8 (DatabaseSeeder)

**Description**:
Create seeder to populate common recipe sources.

**Acceptance Criteria**:
- [ ] Created `database/seeders/SourceSeeder.php`:
  ```php
  class SourceSeeder extends Seeder
  {
      public function run(): void
      {
          $sources = [
              'Family Recipe',
              'Internet',
              'Cookbook',
              'Magazine',
              'Restaurant',
              'Friend',
              'Original Creation',
              'TV Show',
              'YouTube',
              'Blog',
          ];

          foreach ($sources as $name) {
              Source::firstOrCreate(['name' => $name]);
          }
      }
  }
  ```
- [ ] Uses `firstOrCreate` for idempotency
- [ ] Includes common sources
- [ ] Can be run multiple times safely

**Files to Create/Modify**:
- `database/seeders/SourceSeeder.php` (create)

**Testing**:
```bash
php artisan db:seed --class=SourceSeeder
php artisan tinker
>>> Source::all()->pluck('name')
```

**Story**:
```
As a developer
I want common sources seeded
So that recipes have realistic source attribution
```

---

### M11-3 (#345): Create MealSeeder
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (15-30 min)
**Depends On**: M3-17 (Meal model)
**Blocks**: M11-8 (DatabaseSeeder)

**Description**:
Create seeder to populate meal types.

**Acceptance Criteria**:
- [ ] Created `database/seeders/MealSeeder.php`:
  ```php
  class MealSeeder extends Seeder
  {
      public function run(): void
      {
          $meals = [
              'Breakfast',
              'Brunch',
              'Lunch',
              'Dinner',
              'Snack',
              'Dessert',
          ];

          foreach ($meals as $name) {
              Meal::firstOrCreate(['name' => $name]);
          }
      }
  }
  ```

**Files to Create/Modify**:
- `database/seeders/MealSeeder.php` (create)

**Testing**:
```bash
php artisan db:seed --class=MealSeeder
```

**Story**:
```
As a developer
I want meal types seeded
So that recipes can be categorized by when they're served
```

---

### M11-4 (#346): Create PreparationSeeder
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (15-30 min)
**Depends On**: M3-18 (Preparation model)
**Blocks**: M11-8 (DatabaseSeeder)

**Description**:
Create seeder to populate preparation methods.

**Acceptance Criteria**:
- [ ] Created `database/seeders/PreparationSeeder.php`:
  ```php
  class PreparationSeeder extends Seeder
  {
      public function run(): void
      {
          $preparations = [
              'Baked',
              'Grilled',
              'Fried',
              'Boiled',
              'Steamed',
              'Sautéed',
              'Roasted',
              'Slow Cooker',
              'Pressure Cooker',
              'No Cook',
              'Microwave',
          ];

          foreach ($preparations as $name) {
              Preparation::firstOrCreate(['name' => $name]);
          }
      }
  }
  ```

**Files to Create/Modify**:
- `database/seeders/PreparationSeeder.php` (create)

**Testing**:
```bash
php artisan db:seed --class=PreparationSeeder
```

**Story**:
```
As a developer
I want preparation methods seeded
So that recipes can specify cooking techniques
```

---

### M11-5 (#347): Create CourseSeeder
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (15-30 min)
**Depends On**: M3-19 (Course model)
**Blocks**: M11-8 (DatabaseSeeder)

**Description**:
Create seeder to populate course types.

**Acceptance Criteria**:
- [ ] Created `database/seeders/CourseSeeder.php`:
  ```php
  class CourseSeeder extends Seeder
  {
      public function run(): void
      {
          $courses = [
              'Appetizer',
              'Soup',
              'Salad',
              'Main Course',
              'Side Dish',
              'Dessert',
              'Beverage',
          ];

          foreach ($courses as $name) {
              Course::firstOrCreate(['name' => $name]);
          }
      }
  }
  ```

**Files to Create/Modify**:
- `database/seeders/CourseSeeder.php` (create)

**Testing**:
```bash
php artisan db:seed --class=CourseSeeder
```

**Story**:
```
As a developer
I want course types seeded
So that recipes can specify serving order
```

---

### M11-6: Create RecipeFactory
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:medium` (1-2 hours)
**Depends On**: M3-14 (Recipe model)
**Blocks**: M11-8 (DatabaseSeeder), M12-2 (Tests using factory)

**Description**:
Create factory for generating test recipe data with realistic values.

**Acceptance Criteria**:
- [ ] Created `database/factories/RecipeFactory.php`:
  ```php
  class RecipeFactory extends Factory
  {
      protected $model = Recipe::class;

      public function definition(): array
      {
          return [
              'name' => $this->faker->words(3, true),
              'ingredients' => $this->faker->paragraphs(3, true),
              'instructions' => $this->faker->paragraphs(5, true),
              'notes' => $this->faker->optional(0.3)->paragraph(),
              'date_added' => $this->faker->dateTimeBetween('-2 years', 'now'),
              'last_made' => $this->faker->optional(0.4)->dateTimeBetween('-1 year', 'now'),

              // Relationships (will be set during seeding)
              'classification_id' => Classification::inRandomOrder()->first()?->id,
              'source_id' => Source::inRandomOrder()->first()?->id,

              // Nutrition (optional, 50% chance)
              'calories' => $this->faker->optional(0.5)->numberBetween(100, 800),
              'total_fat' => $this->faker->optional(0.5)->numberBetween(5, 50),
              'saturated_fat' => $this->faker->optional(0.5)->numberBetween(1, 20),
              'cholesterol' => $this->faker->optional(0.5)->numberBetween(0, 200),
              'sodium' => $this->faker->optional(0.5)->numberBetween(100, 2000),
              'total_carbohydrates' => $this->faker->optional(0.5)->numberBetween(10, 100),
              'dietary_fiber' => $this->faker->optional(0.5)->numberBetween(1, 20),
              'sugars' => $this->faker->optional(0.5)->numberBetween(1, 50),
              'protein' => $this->faker->optional(0.5)->numberBetween(5, 60),
          ];
      }

      /**
       * Recipe with full nutrition info
       */
      public function withNutrition(): static
      {
          return $this->state(fn (array $attributes) => [
              'calories' => $this->faker->numberBetween(100, 800),
              'total_fat' => $this->faker->numberBetween(5, 50),
              'saturated_fat' => $this->faker->numberBetween(1, 20),
              'cholesterol' => $this->faker->numberBetween(0, 200),
              'sodium' => $this->faker->numberBetween(100, 2000),
              'total_carbohydrates' => $this->faker->numberBetween(10, 100),
              'dietary_fiber' => $this->faker->numberBetween(1, 20),
              'sugars' => $this->faker->numberBetween(1, 50),
              'protein' => $this->faker->numberBetween(5, 60),
          ]);
      }

      /**
       * Recipe without nutrition info
       */
      public function withoutNutrition(): static
      {
          return $this->state(fn (array $attributes) => [
              'calories' => null,
              'total_fat' => null,
              'saturated_fat' => null,
              'cholesterol' => null,
              'sodium' => null,
              'total_carbohydrates' => null,
              'dietary_fiber' => null,
              'sugars' => null,
              'protein' => null,
          ]);
      }
  }
  ```
- [ ] Uses Faker for realistic data
- [ ] Optional nutrition info (50% chance)
- [ ] State methods for nutrition control
- [ ] Relationships properly handled
- [ ] Realistic date ranges
- [ ] Optional notes and last_made fields

**Files to Create/Modify**:
- `database/factories/RecipeFactory.php` (create)

**Testing**:
```php
// In tinker or test
Recipe::factory()->count(5)->create();
Recipe::factory()->withNutrition()->create();
Recipe::factory()->withoutNutrition()->create();

// With relationships
Recipe::factory()
    ->has(Meal::factory()->count(2))
    ->has(Course::factory()->count(1))
    ->create();
```

**Story**:
```
As a developer
I want a recipe factory
So that I can easily create test data
```

---

### M11-7: Create CookbookFactory
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30 min)
**Depends On**: M3-20 (Cookbook model)
**Blocks**: M11-8 (DatabaseSeeder)

**Description**:
Create factory for generating test cookbook data.

**Acceptance Criteria**:
- [ ] Created `database/factories/CookbookFactory.php`:
  ```php
  class CookbookFactory extends Factory
  {
      protected $model = Cookbook::class;

      public function definition(): array
      {
          return [
              'name' => $this->faker->words(3, true),
              'description' => $this->faker->optional(0.7)->sentence(10),
          ];
      }

      /**
       * Cookbook with recipes attached
       */
      public function withRecipes(int $count = 10): static
      {
          return $this->afterCreating(function (Cookbook $cookbook) use ($count) {
              $recipes = Recipe::inRandomOrder()->limit($count)->get();

              foreach ($recipes as $recipe) {
                  $cookbook->recipes()->attach($recipe->id, [
                      'classification_id' => $recipe->classification_id,
                  ]);
              }
          });
      }
  }
  ```
- [ ] Uses Faker for names and descriptions
- [ ] Optional description (70% chance)
- [ ] State method to attach recipes
- [ ] Properly handles pivot data (classification_id)

**Files to Create/Modify**:
- `database/factories/CookbookFactory.php` (create)

**Testing**:
```php
// In tinker
Cookbook::factory()->count(3)->create();
Cookbook::factory()->withRecipes(15)->create();
```

**Story**:
```
As a developer
I want a cookbook factory
So that I can test cookbook functionality
```

---

### M11-8: Update DatabaseSeeder
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:medium` (1 hour)
**Depends On**: M11-1 through M11-7 (All seeders and factories)
**Blocks**: M11-9 (Testing seeding)

**Description**:
Update main DatabaseSeeder to call all seeders in correct order and create test data.

**Acceptance Criteria**:
- [ ] Updated `database/seeders/DatabaseSeeder.php`:
  ```php
  class DatabaseSeeder extends Seeder
  {
      public function run(): void
      {
          // Seed lookup tables first
          $this->call([
              ClassificationSeeder::class,
              SourceSeeder::class,
              MealSeeder::class,
              PreparationSeeder::class,
              CourseSeeder::class,
          ]);

          // Create recipes with relationships
          Recipe::factory()
              ->count(50)
              ->create()
              ->each(function (Recipe $recipe) {
                  // Attach random meals (1-3)
                  $recipe->meals()->attach(
                      Meal::inRandomOrder()->limit(rand(1, 3))->pluck('id')
                  );

                  // Attach random preparations (1-2)
                  $recipe->preparations()->attach(
                      Preparation::inRandomOrder()->limit(rand(1, 2))->pluck('id')
                  );

                  // Attach random courses (1-2)
                  $recipe->courses()->attach(
                      Course::inRandomOrder()->limit(rand(1, 2))->pluck('id')
                  );
              });

          // Create cookbooks with recipes
          Cookbook::factory()
              ->count(5)
              ->create()
              ->each(function (Cookbook $cookbook) {
                  $recipes = Recipe::inRandomOrder()->limit(rand(5, 15))->get();

                  foreach ($recipes as $recipe) {
                      $cookbook->recipes()->attach($recipe->id, [
                          'classification_id' => $recipe->classification_id,
                      ]);
                  }
              });
      }
  }
  ```
- [ ] Calls all seeders in correct dependency order
- [ ] Creates 50 recipes with relationships
- [ ] Creates 5 cookbooks with recipes
- [ ] Randomizes relationship counts for variety
- [ ] Properly attaches pivot data for cookbooks
- [ ] Can be run with `php artisan db:seed`
- [ ] Progress output during seeding (optional)

**Files to Create/Modify**:
- `database/seeders/DatabaseSeeder.php` (modify)

**Testing**:
```bash
# Fresh database with seeded data
php artisan migrate:fresh --seed

# Verify counts
php artisan tinker
>>> Classification::count()  // 10
>>> Source::count()  // 10
>>> Meal::count()  // 6
>>> Preparation::count()  // 11
>>> Course::count()  // 7
>>> Recipe::count()  // 50
>>> Cookbook::count()  // 5
```

**Story**:
```
As a developer
I want a complete database seeder
So that I can quickly set up a development environment
```

---

### M11-9: Test Seeding Process
**Type**: `type:testing`
**Priority**: `P1`
**Effort**: `effort:medium` (1 hour)
**Depends On**: M11-8 (DatabaseSeeder complete)
**Blocks**: None

**Description**:
Comprehensive testing of the entire seeding process.

**Acceptance Criteria**:
- [ ] **Fresh Seeding Test**:
  ```bash
  php artisan migrate:fresh --seed
  ```
  - [ ] Completes without errors
  - [ ] All tables populated
  - [ ] Correct record counts
  - [ ] Relationships properly attached
- [ ] **Data Validation**:
  - [ ] Recipe names realistic
  - [ ] Ingredients and instructions present
  - [ ] Dates in valid ranges
  - [ ] Nutrition values reasonable
  - [ ] Relationships make sense
  - [ ] Cookbook recipes ordered correctly
- [ ] **Idempotency Test**:
  ```bash
  php artisan db:seed
  php artisan db:seed  # Run again
  ```
  - [ ] Lookup tables don't duplicate
  - [ ] Recipe/Cookbook counts increase appropriately
- [ ] **UI Verification**:
  - [ ] Start development server
  - [ ] Visit `/recipes` - verify recipes display
  - [ ] Visit recipe detail - verify all data present
  - [ ] Visit `/cookbooks` - verify cookbooks display
  - [ ] Visit cookbook detail - verify recipes grouped correctly
- [ ] **Performance Test**:
  - [ ] Seeding 50 recipes completes in <30 seconds
  - [ ] No N+1 query issues during seeding
  - [ ] Memory usage acceptable

**Files to Create/Modify**:
- `docs/testing/seeding-test-plan.md` (create)
- Fix any issues found

**Testing Checklist**:
```markdown
## Seeding Tests
- [ ] migrate:fresh --seed completes successfully
- [ ] All lookup tables seeded correctly
- [ ] 50 recipes created
- [ ] 5 cookbooks created
- [ ] Recipe relationships attached
- [ ] Cookbook recipes attached with pivot data
- [ ] Data appears realistic in UI
- [ ] No errors in logs
- [ ] Can reseed without duplicating lookups
```

**Story**:
```
As a developer
I want comprehensive seeding tests
So that I can rely on seeded data for development
```

---

### M11-10: Create Seeding Documentation
**Type**: `type:docs`
**Priority**: `P2`
**Effort**: `effort:small` (30 min)
**Depends On**: M11-9 (Seeding tested)
**Blocks**: None

**Description**:
Document seeding process, available seeders, and factory usage.

**Acceptance Criteria**:
- [ ] Created `docs/DATABASE_SEEDING.md`:
  ```markdown
  # Database Seeding

  ## Quick Start
  \`\`\`bash
  # Fresh database with seed data
  php artisan migrate:fresh --seed
  \`\`\`

  ## Available Seeders
  - ClassificationSeeder - 10 recipe classifications
  - SourceSeeder - 10 recipe sources
  - MealSeeder - 6 meal types
  - PreparationSeeder - 11 preparation methods
  - CourseSeeder - 7 course types
  - DatabaseSeeder - Complete seeding (includes 50 recipes, 5 cookbooks)

  ## Running Individual Seeders
  \`\`\`bash
  php artisan db:seed --class=ClassificationSeeder
  \`\`\`

  ## Factories
  [Documentation of RecipeFactory and CookbookFactory usage]

  ## Testing
  [Examples of using factories in tests]
  ```
- [ ] Includes examples for each seeder
- [ ] Documents factory states (withNutrition, withoutNutrition, etc.)
- [ ] Explains seeding order and dependencies
- [ ] Provides troubleshooting tips
- [ ] Links to factory usage in tests

**Files to Create/Modify**:
- `docs/DATABASE_SEEDING.md` (create)
- `README.md` (add link to seeding docs)

**Testing**:
Review documentation for accuracy and completeness

**Story**:
```
As a developer
I want seeding documentation
So that I understand how to use and maintain seeders
```

---

## Summary

**Total Issues**: 10
**Can Run in Parallel**: M11-1 through M11-7 can all run in parallel, then M11-8, then M11-9, then M11-10
**Critical Path**: M11-1 through M11-7 → M11-8 → M11-9 → M11-10
**Estimated Milestone Completion**: 6-8 hours with 4-5 agents, 12-16 hours solo

**Parallel Execution Strategy**:
- **Wave 1** (All parallel):
  - **Agent 1**: M11-1 (ClassificationSeeder)
  - **Agent 2**: M11-2 (SourceSeeder)
  - **Agent 3**: M11-3 (MealSeeder)
  - **Agent 4**: M11-4 (PreparationSeeder)
  - **Agent 5**: M11-5 (CourseSeeder)
- **Wave 2** (Parallel after Wave 1):
  - **Agent 1**: M11-6 (RecipeFactory)
  - **Agent 2**: M11-7 (CookbookFactory)
- **Wave 3** (After Wave 2):
  - **Agent 1**: M11-8 (DatabaseSeeder)
- **Wave 4** (After Wave 3):
  - **Agent 1**: M11-9 (Testing)
- **Wave 5** (After Wave 4):
  - **Agent 1**: M11-10 (Documentation)

**Dependency Chain**:
```
M3-15 → M11-1 ↘
M3-16 → M11-2  ↘
M3-17 → M11-3   → M11-8 → M11-9 → M11-10
M3-18 → M11-4  ↗       ↓
M3-19 → M11-5 ↗       M12-2 (Tests use factories)
M3-14 → M11-6 ↗
M3-20 → M11-7 ↗
```

**Success Criteria**:
All seeders and factories created and working. DatabaseSeeder populates database with realistic test data. 50 recipes and 5 cookbooks created with proper relationships. Seeding idempotent for lookup tables. UI displays seeded data correctly. Comprehensive documentation in place.
