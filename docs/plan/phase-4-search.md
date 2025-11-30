# Milestone 4 - Search

**Goal**: Implement search functionality for recipes with performance testing

**Estimated Total Effort**: 2-3 hours
**Can Start**: After M3-14 complete (Recipe model)
**Parallel Capacity**: 2 agents (limited parallelization)

---

## Issues

### M4-1 (#274): Add Search Scope to Recipe Model
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:medium` (1-2 hours)
**Depends On**: M3-14 (Recipe model)
**Blocks**: M5-1 (RecipeController index)

**Description**:
Add a local query scope to the Recipe model to enable search functionality on recipe names and ingredients.

**Acceptance Criteria**:
- [ ] Added `scopeSearch()` method to Recipe model:
  ```php
  public function scopeSearch(Builder $query, ?string $search): Builder
  {
      if (empty($search)) {
          return $query;
      }

      return $query->where(function (Builder $q) use ($search) {
          $q->where('name', 'like', "%{$search}%")
            ->orWhere('ingredients', 'like', "%{$search}%");
      });
  }
  ```
- [ ] Scope handles null/empty search gracefully
- [ ] Scope uses OR logic for name and ingredients
- [ ] Scope uses parameterized queries (no SQL injection)
- [ ] Added PHPDoc block with parameter and return types
- [ ] Test scope with various search terms

**Files to Create/Modify**:
- `app/Models/Recipe.php` (modify)
- `tests/Unit/RecipeModelTest.php` (update with search tests)

**Testing**:
Create test in `tests/Unit/RecipeModelTest.php`:
```php
test('search scope filters recipes by name', function () {
    $recipe1 = Recipe::factory()->create(['name' => 'Chocolate Cake']);
    $recipe2 = Recipe::factory()->create(['name' => 'Vanilla Ice Cream']);

    $results = Recipe::search('Chocolate')->get();

    expect($results)->toHaveCount(1);
    expect($results->first()->id)->toBe($recipe1->id);
});

test('search scope filters recipes by ingredients', function () {
    $recipe1 = Recipe::factory()->create([
        'ingredients' => 'flour, sugar, chocolate',
    ]);
    $recipe2 = Recipe::factory()->create([
        'ingredients' => 'cream, vanilla, sugar',
    ]);

    $results = Recipe::search('chocolate')->get();

    expect($results)->toHaveCount(1);
    expect($results->first()->id)->toBe($recipe1->id);
});

test('search scope returns all recipes when search is empty', function () {
    Recipe::factory()->count(5)->create();

    $results = Recipe::search('')->get();

    expect($results)->toHaveCount(5);
});

test('search scope returns all recipes when search is null', function () {
    Recipe::factory()->count(3)->create();

    $results = Recipe::search(null)->get();

    expect($results)->toHaveCount(3);
});
```

Run tests:
```bash
php artisan test --filter=RecipeModelTest
```

**Story**:
```
As a user
I want to search for recipes by name or ingredients
So that I can quickly find recipes that match my needs
```

---

### M4-2 (#268): Test Full-Text Search Performance (MySQL Only)
**Type**: `type:testing`, `type:optimization`
**Priority**: `P2`
**Effort**: `effort:medium` (1 hour)
**Depends On**: M3-13 (Full-text index), M4-1 (Search scope)
**Blocks**: None (optional optimization)

**Description**:
Test and compare performance of LIKE-based search vs full-text search for MySQL databases. Document findings for future optimization.

**Acceptance Criteria**:
- [ ] Created test database seeded with 1000+ recipes
- [ ] Measured performance of LIKE-based search (M4-1):
  ```php
  $query->where('name', 'like', "%{$search}%")
        ->orWhere('ingredients', 'like', "%{$search}%");
  ```
- [ ] Measured performance of full-text search:
  ```php
  $query->whereRaw("MATCH(name, ingredients) AGAINST(? IN BOOLEAN MODE)", [$search]);
  ```
- [ ] Compared execution times for:
  - [ ] Single-word searches (e.g., "chocolate")
  - [ ] Multi-word searches (e.g., "chocolate cake")
  - [ ] Partial word searches (e.g., "choc")
- [ ] Documented results in `docs/performance/search-performance.md`:
  - [ ] Execution time comparison table
  - [ ] Recommendation on which approach to use
  - [ ] Notes on full-text limitations (no partial matching)
  - [ ] Notes on LIKE limitations (slower on large datasets)
- [ ] Created optional `scopeFullTextSearch()` method if full-text is faster:
  ```php
  public function scopeFullTextSearch(Builder $query, ?string $search): Builder
  {
      if (empty($search)) {
          return $query;
      }

      return $query->whereRaw(
          "MATCH(name, ingredients) AGAINST(? IN BOOLEAN MODE)",
          [$search]
      );
  }
  ```

**Files to Create/Modify**:
- `app/Models/Recipe.php` (optional: add scopeFullTextSearch)
- `database/seeders/SearchTestSeeder.php` (create for testing)
- `docs/performance/search-performance.md` (create)
- `tests/Feature/SearchPerformanceTest.php` (create - can be removed after testing)

**Testing**:
Create seeder for performance testing:
```php
// database/seeders/SearchTestSeeder.php
class SearchTestSeeder extends Seeder
{
    public function run(): void
    {
        // Create 1000 recipes with varied names and ingredients
        Recipe::factory()->count(1000)->create();
    }
}
```

Run performance tests:
```bash
php artisan db:seed --class=SearchTestSeeder
php artisan test --filter=SearchPerformanceTest
```

Create temporary performance test:
```php
// tests/Feature/SearchPerformanceTest.php
test('compare LIKE vs full-text search performance', function () {
    // Ensure we have test data
    if (Recipe::count() < 1000) {
        Recipe::factory()->count(1000)->create();
    }

    // Test LIKE-based search
    $start = microtime(true);
    Recipe::search('chocolate')->get();
    $likeTime = microtime(true) - $start;

    // Test full-text search (MySQL only)
    if (DB::connection()->getDriverName() === 'mysql') {
        $start = microtime(true);
        Recipe::fullTextSearch('chocolate')->get();
        $fullTextTime = microtime(true) - $start;

        dump([
            'LIKE search time' => $likeTime . 's',
            'Full-text search time' => $fullTextTime . 's',
            'Improvement' => round(($likeTime / $fullTextTime), 2) . 'x',
        ]);
    }

    expect(true)->toBeTrue(); // Always pass, this is just for measurement
});
```

**Story**:
```
As a developer
I want to compare LIKE vs full-text search performance
So that I can choose the optimal search implementation
```

**Note**: This issue is optional and primarily for MySQL databases. PostgreSQL would use different full-text search syntax. The LIKE-based approach (M4-1) works across all databases and is sufficient for small to medium datasets.

---

## Summary

**Total Issues**: 2
**Can Run in Parallel**: M4-2 can start after M4-1 completes
**Critical Path**: M4-1 → M5-1
**Estimated Milestone Completion**: 2-3 hours with 1-2 agents

**Parallel Execution Strategy**:
- **Agent 1**: M4-1 (Search scope) → M5-1 (RecipeController)
- **Agent 2**: Wait for M4-1, then M4-2 (Performance testing - optional)

**Dependency Chain**:
```
M3-14 → M4-1 → M5-1
M3-13 ↘         ↓
        M4-2 (optional)
```

**Success Criteria**:
Recipe search functionality implemented with scope method. Performance comparison documented for MySQL full-text search. Tests passing with adequate coverage.
