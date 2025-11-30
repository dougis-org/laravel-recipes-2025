# Milestone 5 - Controllers & Routing

**Goal**: Create controllers and routes for recipes and cookbooks with proper request handling

**Estimated Total Effort**: 6-8 hours
**Can Start**: After M3-14, M3-20, M4-1 complete
**Parallel Capacity**: 3-4 agents (good parallelization possible)

---

## Issues

### M5-1: Create RecipeController with Index Method
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:medium` (1-2 hours)
**Depends On**: M3-14 (Recipe model), M4-1 (Search scope)
**Blocks**: M5-6 (Recipe routes), M7-1 (Recipe index view)

**Description**:
Create RecipeController with index() method supporting sorting, pagination, search, and eager loading.

**Acceptance Criteria**:
- [ ] Created `app/Http/Controllers/RecipeController.php`
- [ ] Implemented `index()` method with:
  ```php
  public function index(Request $request)
  {
      $recipes = Recipe::query()
          ->with(['classification', 'source', 'meals', 'preparations', 'courses'])
          ->search($request->input('search'))
          ->when($request->filled('sortField'), function (Builder $query) use ($request) {
              $sortField = $request->input('sortField', 'name');
              $sortOrder = $request->input('sortOrder', 'asc');
              return $query->orderBy($sortField, $sortOrder);
          }, function (Builder $query) {
              return $query->orderBy('name', 'asc');
          })
          ->paginate($request->input('displayCount', 25));

      return view('recipes.index', compact('recipes'));
  }
  ```
- [ ] Supports query parameters:
  - [ ] `search` - search term (optional)
  - [ ] `sortField` - column to sort by (default: 'name')
  - [ ] `sortOrder` - 'asc' or 'desc' (default: 'asc')
  - [ ] `displayCount` - results per page (default: 25)
- [ ] Uses eager loading to prevent N+1 queries
- [ ] Returns paginated results
- [ ] Handles missing/invalid parameters gracefully

**Files to Create/Modify**:
- `app/Http/Controllers/RecipeController.php` (create)

**Testing**:
Create test in `tests/Feature/RecipeControllerTest.php`:
```php
test('index displays paginated recipes', function () {
    Recipe::factory()->count(30)->create();

    $response = $this->get('/recipes');

    $response->assertOk();
    $response->assertViewIs('recipes.index');
    $response->assertViewHas('recipes');
});

test('index can search recipes', function () {
    Recipe::factory()->create(['name' => 'Chocolate Cake']);
    Recipe::factory()->create(['name' => 'Vanilla Ice Cream']);

    $response = $this->get('/recipes?search=Chocolate');

    $response->assertOk();
    $response->assertSee('Chocolate Cake');
    $response->assertDontSee('Vanilla Ice Cream');
});

test('index can sort recipes', function () {
    Recipe::factory()->create(['name' => 'Zebra Cake', 'date_added' => now()->subDays(1)]);
    Recipe::factory()->create(['name' => 'Apple Pie', 'date_added' => now()]);

    $response = $this->get('/recipes?sortField=name&sortOrder=asc');

    // Would need to check order in response
    $response->assertOk();
});

test('index respects display count', function () {
    Recipe::factory()->count(30)->create();

    $response = $this->get('/recipes?displayCount=10');

    $response->assertOk();
    // Pagination should show 10 per page
});

test('index prevents N+1 queries with eager loading', function () {
    Recipe::factory()->count(10)->create();

    DB::enableQueryLog();
    $this->get('/recipes');
    $queries = DB::getQueryLog();

    // Should be a small number of queries (1 for recipes + 1 per relationship)
    // Not 1 + N queries
    expect(count($queries))->toBeLessThan(20);
});
```

**Story**:
```
As a user
I want to view a list of recipes with search and sorting options
So that I can find recipes that interest me
```

---

### M5-2: Add RecipeController Show Method
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M5-1 (RecipeController created)
**Blocks**: M5-6 (Recipe routes), M7-2 (Recipe show view)

**Description**:
Add show() method to RecipeController to display individual recipe details.

**Acceptance Criteria**:
- [ ] Added `show()` method to RecipeController:
  ```php
  public function show(Recipe $recipe)
  {
      $recipe->load([
          'classification',
          'source',
          'meals',
          'preparations',
          'courses',
          'cookbooks',
      ]);

      return view('recipes.show', compact('recipe'));
  }
  ```
- [ ] Uses route model binding for automatic recipe lookup
- [ ] Eager loads all relationships
- [ ] Returns 404 for missing recipes (handled by Laravel automatically)
- [ ] Passes loaded recipe to view

**Files to Create/Modify**:
- `app/Http/Controllers/RecipeController.php` (modify)

**Testing**:
Add to `tests/Feature/RecipeControllerTest.php`:
```php
test('show displays a single recipe', function () {
    $recipe = Recipe::factory()->create(['name' => 'Test Recipe']);

    $response = $this->get("/recipes/{$recipe->id}");

    $response->assertOk();
    $response->assertViewIs('recipes.show');
    $response->assertViewHas('recipe');
    $response->assertSee('Test Recipe');
});

test('show returns 404 for missing recipe', function () {
    $response = $this->get('/recipes/99999');

    $response->assertNotFound();
});

test('show eager loads all relationships', function () {
    $recipe = Recipe::factory()
        ->has(Meal::factory()->count(2))
        ->has(Course::factory()->count(1))
        ->create();

    DB::enableQueryLog();
    $this->get("/recipes/{$recipe->id}");
    $queries = DB::getQueryLog();

    // Should be minimal queries due to eager loading
    expect(count($queries))->toBeLessThan(10);
});
```

**Story**:
```
As a user
I want to view detailed information about a specific recipe
So that I can see all ingredients, instructions, and nutrition info
```

---

### M5-3: Create CookbookController with Index
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M3-20 (Cookbook model)
**Blocks**: M5-7 (Cookbook routes), M8-1 (Cookbook index view)

**Description**:
Create CookbookController with index() method to list all cookbooks with recipe counts.

**Acceptance Criteria**:
- [ ] Created `app/Http/Controllers/CookbookController.php`
- [ ] Implemented `index()` method:
  ```php
  public function index()
  {
      $cookbooks = Cookbook::query()
          ->withCount('recipes')
          ->orderBy('name', 'asc')
          ->get();

      return view('cookbooks.index', compact('cookbooks'));
  }
  ```
- [ ] Loads recipe counts using `withCount()`
- [ ] Orders cookbooks alphabetically by name
- [ ] Returns all cookbooks (no pagination needed - small dataset)

**Files to Create/Modify**:
- `app/Http/Controllers/CookbookController.php` (create)

**Testing**:
Create `tests/Feature/CookbookControllerTest.php`:
```php
test('index displays all cookbooks', function () {
    Cookbook::factory()->count(5)->create();

    $response = $this->get('/cookbooks');

    $response->assertOk();
    $response->assertViewIs('cookbooks.index');
    $response->assertViewHas('cookbooks');
});

test('index shows recipe counts', function () {
    $cookbook = Cookbook::factory()
        ->has(Recipe::factory()->count(3))
        ->create(['name' => 'My Cookbook']);

    $response = $this->get('/cookbooks');

    $response->assertOk();
    // Would check that recipe count is displayed
});

test('index orders cookbooks alphabetically', function () {
    Cookbook::factory()->create(['name' => 'Zebra Cookbook']);
    Cookbook::factory()->create(['name' => 'Apple Cookbook']);

    $response = $this->get('/cookbooks');

    $response->assertOk();
    // Would verify order in response
});
```

**Story**:
```
As a user
I want to view a list of all cookbooks
So that I can browse my cookbook collection
```

---

### M5-4: Add CookbookController Show Method
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M5-3 (CookbookController created)
**Blocks**: M5-7 (Cookbook routes), M8-2 (Cookbook show view)

**Description**:
Add show() method to CookbookController to display cookbook with ordered recipes.

**Acceptance Criteria**:
- [ ] Added `show()` method to CookbookController:
  ```php
  public function show(Cookbook $cookbook)
  {
      $cookbook->load([
          'recipes' => function ($query) {
              $query->orderBy('cookbook_recipe.classification_id', 'asc')
                    ->orderBy('name', 'asc');
          },
          'recipes.classification',
          'recipes.source',
      ]);

      return view('cookbooks.show', compact('cookbook'));
  }
  ```
- [ ] Uses route model binding
- [ ] Orders recipes by classification, then by name
- [ ] Eager loads recipe relationships
- [ ] Returns 404 for missing cookbooks

**Files to Create/Modify**:
- `app/Http/Controllers/CookbookController.php` (modify)

**Testing**:
Add to `tests/Feature/CookbookControllerTest.php`:
```php
test('show displays a single cookbook with recipes', function () {
    $cookbook = Cookbook::factory()
        ->has(Recipe::factory()->count(3))
        ->create(['name' => 'Test Cookbook']);

    $response = $this->get("/cookbooks/{$cookbook->id}");

    $response->assertOk();
    $response->assertViewIs('cookbooks.show');
    $response->assertViewHas('cookbook');
    $response->assertSee('Test Cookbook');
});

test('show returns 404 for missing cookbook', function () {
    $response = $this->get('/cookbooks/99999');

    $response->assertNotFound();
});

test('show orders recipes by classification then name', function () {
    $classification1 = Classification::factory()->create(['id' => 1]);
    $classification2 = Classification::factory()->create(['id' => 2]);

    $cookbook = Cookbook::factory()->create();

    $recipe1 = Recipe::factory()->create([
        'name' => 'Zebra Dish',
        'classification_id' => 1,
    ]);
    $recipe2 = Recipe::factory()->create([
        'name' => 'Apple Dish',
        'classification_id' => 2,
    ]);
    $recipe3 = Recipe::factory()->create([
        'name' => 'Berry Dish',
        'classification_id' => 1,
    ]);

    $cookbook->recipes()->attach([$recipe1->id, $recipe2->id, $recipe3->id]);

    $response = $this->get("/cookbooks/{$cookbook->id}");

    $response->assertOk();
    // Would verify order: Berry Dish (class 1), Zebra Dish (class 1), Apple Dish (class 2)
});
```

**Story**:
```
As a user
I want to view a cookbook with its recipes properly organized
So that I can easily browse recipes by classification
```

---

### M5-5: Create SearchRecipeRequest Form Request
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:small` (30 min)
**Depends On**: M5-1 (RecipeController index)
**Blocks**: None

**Description**:
Create form request class to validate search and sorting parameters for recipe index.

**Acceptance Criteria**:
- [ ] Created `app/Http/Requests/SearchRecipeRequest.php`:
  ```php
  class SearchRecipeRequest extends FormRequest
  {
      public function authorize(): bool
      {
          return true; // Public access
      }

      public function rules(): array
      {
          return [
              'search' => ['nullable', 'string', 'max:255'],
              'sortField' => ['nullable', 'string', 'in:name,date_added'],
              'sortOrder' => ['nullable', 'string', 'in:asc,desc'],
              'displayCount' => ['nullable', 'integer', 'min:10', 'max:100'],
          ];
      }

      public function messages(): array
      {
          return [
              'sortField.in' => 'You can only sort by name or date added.',
              'sortOrder.in' => 'Sort order must be ascending or descending.',
              'displayCount.min' => 'Display count must be at least 10.',
              'displayCount.max' => 'Display count cannot exceed 100.',
          ];
      }
  }
  ```
- [ ] Validates all search/sort parameters
- [ ] Allows null values (parameters are optional)
- [ ] Restricts sortField to allowed columns
- [ ] Restricts displayCount to reasonable range (10-100)
- [ ] Includes custom error messages
- [ ] Update RecipeController to use SearchRecipeRequest:
  ```php
  public function index(SearchRecipeRequest $request)
  {
      // ... existing code uses validated data
  }
  ```

**Files to Create/Modify**:
- `app/Http/Requests/SearchRecipeRequest.php` (create)
- `app/Http/Controllers/RecipeController.php` (modify - change Request to SearchRecipeRequest)

**Testing**:
Add to `tests/Feature/RecipeControllerTest.php`:
```php
test('index validates sort field', function () {
    Recipe::factory()->count(5)->create();

    $response = $this->get('/recipes?sortField=invalid_column');

    $response->assertSessionHasErrors('sortField');
});

test('index validates sort order', function () {
    Recipe::factory()->count(5)->create();

    $response = $this->get('/recipes?sortOrder=invalid');

    $response->assertSessionHasErrors('sortOrder');
});

test('index validates display count minimum', function () {
    Recipe::factory()->count(5)->create();

    $response = $this->get('/recipes?displayCount=5');

    $response->assertSessionHasErrors('displayCount');
});

test('index validates display count maximum', function () {
    Recipe::factory()->count(5)->create();

    $response = $this->get('/recipes?displayCount=200');

    $response->assertSessionHasErrors('displayCount');
});

test('index accepts valid parameters', function () {
    Recipe::factory()->count(5)->create();

    $response = $this->get('/recipes?sortField=name&sortOrder=desc&displayCount=25');

    $response->assertOk();
    $response->assertSessionHasNoErrors();
});
```

**Story**:
```
As a developer
I want validated input for search and sorting parameters
So that the application is protected from invalid data
```

---

### M5-6: Define Routes for Recipes
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (15-30 min)
**Depends On**: M5-1 (RecipeController index), M5-2 (RecipeController show)
**Blocks**: M7-1 (Recipe views can be accessed)

**Description**:
Define resource routes for recipe listing and viewing.

**Acceptance Criteria**:
- [ ] Added routes to `routes/web.php`:
  ```php
  Route::resource('recipes', RecipeController::class)->only([
      'index', 'show'
  ]);
  ```
- [ ] Routes defined:
  - [ ] `GET /recipes` → `RecipeController@index` (name: recipes.index)
  - [ ] `GET /recipes/{recipe}` → `RecipeController@show` (name: recipes.show)
- [ ] Verify routes with `php artisan route:list --name=recipes`
- [ ] Test routes are accessible

**Files to Create/Modify**:
- `routes/web.php` (modify)

**Testing**:
```bash
# Verify routes exist
php artisan route:list --name=recipes

# Should show:
# GET|HEAD  recipes ................. recipes.index › RecipeController@index
# GET|HEAD  recipes/{recipe} ........ recipes.show › RecipeController@show
```

Add to `tests/Feature/RecipeControllerTest.php`:
```php
test('recipe routes are defined', function () {
    expect(Route::has('recipes.index'))->toBeTrue();
    expect(Route::has('recipes.show'))->toBeTrue();
});
```

**Story**:
```
As a developer
I want routes defined for recipe pages
So that users can access recipe listings and details
```

---

### M5-7: Define Routes for Cookbooks
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (15-30 min)
**Depends On**: M5-3 (CookbookController index), M5-4 (CookbookController show)
**Blocks**: M8-1 (Cookbook views can be accessed)

**Description**:
Define resource routes for cookbook listing and viewing.

**Acceptance Criteria**:
- [ ] Added routes to `routes/web.php`:
  ```php
  Route::resource('cookbooks', CookbookController::class)->only([
      'index', 'show'
  ]);
  ```
- [ ] Routes defined:
  - [ ] `GET /cookbooks` → `CookbookController@index` (name: cookbooks.index)
  - [ ] `GET /cookbooks/{cookbook}` → `CookbookController@show` (name: cookbooks.show)
- [ ] Verify routes with `php artisan route:list --name=cookbooks`
- [ ] Test routes are accessible

**Files to Create/Modify**:
- `routes/web.php` (modify)

**Testing**:
```bash
# Verify routes exist
php artisan route:list --name=cookbooks

# Should show:
# GET|HEAD  cookbooks ................. cookbooks.index › CookbookController@index
# GET|HEAD  cookbooks/{cookbook} ...... cookbooks.show › CookbookController@show
```

Add to `tests/Feature/CookbookControllerTest.php`:
```php
test('cookbook routes are defined', function () {
    expect(Route::has('cookbooks.index'))->toBeTrue();
    expect(Route::has('cookbooks.show'))->toBeTrue();
});
```

**Story**:
```
As a developer
I want routes defined for cookbook pages
So that users can access cookbook listings and details
```

---

### M5-8: Create Default Route Redirect
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:small` (15 min)
**Depends On**: M5-6 (Recipe routes defined)
**Blocks**: None

**Description**:
Create root route that redirects to recipes index with default parameters.

**Acceptance Criteria**:
- [ ] Updated `routes/web.php` to replace Laravel welcome:
  ```php
  Route::get('/', function () {
      return redirect()->route('recipes.index', [
          'sortField' => 'name',
          'sortOrder' => 'asc',
          'displayCount' => 25,
      ]);
  })->name('home');
  ```
- [ ] Root URL redirects to `/recipes?sortField=name&sortOrder=asc&displayCount=25`
- [ ] Named route 'home' for convenience
- [ ] Remove default welcome route if present

**Files to Create/Modify**:
- `routes/web.php` (modify)

**Testing**:
Create `tests/Feature/HomeRouteTest.php`:
```php
test('home route redirects to recipes index', function () {
    $response = $this->get('/');

    $response->assertRedirect();
    $response->assertRedirectToRoute('recipes.index');
});

test('home route includes default query parameters', function () {
    $response = $this->get('/');

    $response->assertRedirect();
    expect($response->headers->get('Location'))
        ->toContain('sortField=name')
        ->toContain('sortOrder=asc')
        ->toContain('displayCount=25');
});
```

**Story**:
```
As a user
I want the homepage to show me recipes immediately
So that I can start browsing without extra clicks
```

---

### M5-9: Write Controller Tests
**Type**: `type:testing`
**Priority**: `P1`
**Effort**: `effort:medium` (1-2 hours)
**Depends On**: M5-1, M5-2, M5-3, M5-4 (All controllers complete)
**Blocks**: None

**Description**:
Comprehensive feature tests for all controller methods covering happy paths, edge cases, and error conditions.

**Acceptance Criteria**:
- [ ] `tests/Feature/RecipeControllerTest.php` includes tests for:
  - [ ] Index pagination
  - [ ] Index search functionality
  - [ ] Index sorting (all valid fields and orders)
  - [ ] Index display count customization
  - [ ] Index eager loading (N+1 prevention)
  - [ ] Show displays recipe
  - [ ] Show returns 404 for missing recipe
  - [ ] Show eager loads relationships
  - [ ] Input validation (via SearchRecipeRequest)
- [ ] `tests/Feature/CookbookControllerTest.php` includes tests for:
  - [ ] Index displays all cookbooks
  - [ ] Index shows recipe counts
  - [ ] Index orders alphabetically
  - [ ] Show displays cookbook with recipes
  - [ ] Show returns 404 for missing cookbook
  - [ ] Show orders recipes correctly (classification, then name)
- [ ] `tests/Feature/HomeRouteTest.php` includes tests for:
  - [ ] Root redirect to recipes
  - [ ] Default query parameters
- [ ] All tests pass: `php artisan test --testsuite=Feature`
- [ ] Test coverage >80% for controllers

**Files to Create/Modify**:
- `tests/Feature/RecipeControllerTest.php` (expand existing tests)
- `tests/Feature/CookbookControllerTest.php` (expand existing tests)
- `tests/Feature/HomeRouteTest.php` (create)

**Testing**:
Run all feature tests:
```bash
php artisan test --testsuite=Feature
php artisan test --coverage --min=80
```

**Story**:
```
As a developer
I want comprehensive tests for all controllers
So that I can confidently refactor and add features
```

**Note**: Many of the tests for this issue have already been defined inline with the controller implementation issues (M5-1 through M5-8). This issue ensures all tests are complete, passing, and provide adequate coverage.

---

## Summary

**Total Issues**: 9
**Can Run in Parallel**: M5-1 and M5-3 can run in parallel, then subsequent issues depend on them
**Critical Path**: M5-1 → M5-2 → M5-6 → M7-1
**Estimated Milestone Completion**: 6-8 hours with 3-4 agents, 12-16 hours solo

**Parallel Execution Strategy**:
- **Wave 1** (Parallel):
  - **Agent 1**: M5-1 (RecipeController index)
  - **Agent 2**: M5-3 (CookbookController index)
- **Wave 2** (Parallel after Wave 1):
  - **Agent 1**: M5-2 (RecipeController show) → M5-6 (Recipe routes)
  - **Agent 2**: M5-4 (CookbookController show) → M5-7 (Cookbook routes)
  - **Agent 3**: M5-5 (SearchRecipeRequest)
- **Wave 3** (After Wave 2):
  - **Agent 1**: M5-8 (Default route)
  - **Agent 2**: M5-9 (Controller tests - comprehensive)

**Dependency Chain**:
```
M3-14, M4-1 → M5-1 → M5-2 → M5-6 → M5-8, M7-1
                    ↘       ↗
                     M5-5 (Form Request)

M3-20 → M5-3 → M5-4 → M5-7 → M8-1

M5-1, M5-2, M5-3, M5-4 → M5-9 (Tests)
```

**Success Criteria**:
Controllers created for recipes and cookbooks with proper index and show methods. Routes defined and accessible. Form request validation in place. Comprehensive tests passing with >80% coverage. Default homepage redirects to recipe listing.
