# Milestone 7 - Recipe Views

**Goal**: Create recipe listing and detail views with full Tailwind styling

**Estimated Total Effort**: 4-6 hours
**Can Start**: After M6-6, M6-7, M6-8, M5-6 complete
**Parallel Capacity**: 2-3 agents (some parallelization possible)

---

## Issues

### M7-1: Create Recipe Index View
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:medium` (1-2 hours)
**Depends On**: M6-6 (Recipe card), M6-7 (Pagination), M6-8 (Sort controls), M5-6 (Recipe routes)
**Blocks**: M7-3 (Styling), M7-5 (Testing)

**Description**:
Create recipe index view with grid layout, search form, sort controls, and pagination.

**Acceptance Criteria**:
- [ ] Created `resources/views/recipes/index.blade.php`:
  ```blade
  @extends('layouts.app')

  @section('title', 'Recipes')

  @section('content')
      <div class="space-y-6">
          <!-- Header -->
          <div class="flex justify-between items-center">
              <h1 class="text-3xl font-bold text-gray-900">Recipes</h1>
              <p class="text-gray-600">
                  {{ $recipes->total() }} {{ Str::plural('recipe', $recipes->total()) }}
              </p>
          </div>

          <!-- Search and Filters -->
          <div class="bg-white rounded-lg shadow-sm p-6">
              <form method="GET" action="{{ route('recipes.index') }}" class="space-y-4">
                  <!-- Search -->
                  <div>
                      <x-input
                          label="Search Recipes"
                          name="search"
                          type="text"
                          :value="request('search')"
                          placeholder="Search by name or ingredients..."
                      />
                  </div>

                  <!-- Sort Controls -->
                  <x-sort-controls
                      :sortField="request('sortField', 'name')"
                      :sortOrder="request('sortOrder', 'asc')"
                  />

                  <!-- Display Count -->
                  <div class="flex gap-4">
                      <div class="flex-1">
                          <label for="displayCount" class="block text-sm font-medium text-gray-700 mb-1">
                              Items per page
                          </label>
                          <select
                              name="displayCount"
                              id="displayCount"
                              onchange="this.form.submit()"
                              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                          >
                              <option value="25" {{ request('displayCount', 25) == 25 ? 'selected' : '' }}>25</option>
                              <option value="50" {{ request('displayCount') == 50 ? 'selected' : '' }}>50</option>
                              <option value="100" {{ request('displayCount') == 100 ? 'selected' : '' }}>100</option>
                          </select>
                      </div>

                      <div class="flex items-end">
                          <x-button type="submit" variant="primary">
                              Search
                          </x-button>

                          @if(request()->hasAny(['search', 'sortField', 'sortOrder', 'displayCount']))
                              <a href="{{ route('recipes.index') }}" class="ml-3">
                                  <x-button variant="secondary">
                                      Clear
                                  </x-button>
                              </a>
                          @endif
                      </div>
                  </div>
              </form>
          </div>

          <!-- Results -->
          @if($recipes->count() > 0)
              <!-- Recipe Grid -->
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                  @foreach($recipes as $recipe)
                      <x-recipe-card :recipe="$recipe" />
                  @endforeach
              </div>

              <!-- Pagination -->
              <div class="mt-8">
                  {{ $recipes->links() }}
              </div>
          @else
              <!-- Empty State -->
              <div class="bg-white rounded-lg shadow-sm p-12 text-center">
                  <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <h3 class="mt-2 text-sm font-medium text-gray-900">No recipes found</h3>
                  <p class="mt-1 text-sm text-gray-500">
                      @if(request('search'))
                          Try adjusting your search terms.
                      @else
                          Get started by adding your first recipe.
                      @endif
                  </p>
              </div>
          @endif
      </div>
  @endsection
  ```
- [ ] Uses base layout (`@extends`)
- [ ] Shows total recipe count in header
- [ ] Includes search form with input component
- [ ] Includes sort controls component
- [ ] Includes display count selector
- [ ] Shows clear filters button when filters active
- [ ] Responsive grid layout (1/2/3/4 columns)
- [ ] Uses recipe card component
- [ ] Includes pagination
- [ ] Shows empty state when no results
- [ ] All form inputs auto-submit on change
- [ ] Maintains query parameters across pagination

**Files to Create/Modify**:
- `resources/views/recipes/index.blade.php` (create)

**Testing**:
Manual testing:
1. Visit `/recipes`
2. Verify search works (try "chocolate")
3. Verify sorting works (name asc/desc, date asc/desc)
4. Verify display count changes results per page
5. Verify pagination works and maintains filters
6. Verify clear button resets all filters
7. Verify empty state shows when no results
8. Verify responsive grid at different screen sizes
9. Verify recipe cards link to detail pages

**Story**:
```
As a user
I want to view and search recipes in a grid layout
So that I can find recipes that interest me
```

---

### M7-2: Create Recipe Show View
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:medium` (1-2 hours)
**Depends On**: M6-5 (Card component), M5-2 (RecipeController show)
**Blocks**: M7-4 (Styling), M7-5 (Testing)

**Description**:
Create recipe detail view showing all recipe information including relationships.

**Acceptance Criteria**:
- [ ] Created `resources/views/recipes/show.blade.php`:
  ```blade
  @extends('layouts.app')

  @section('title', $recipe->name)

  @section('content')
      <div class="space-y-6">
          <!-- Header with Back Button -->
          <div>
              <a href="{{ route('recipes.index') }}" class="inline-flex items-center text-blue-600 hover:text-blue-800 mb-4">
                  <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                  Back to Recipes
              </a>
              <h1 class="text-4xl font-bold text-gray-900">{{ $recipe->name }}</h1>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <!-- Main Content (2/3 width on large screens) -->
              <div class="lg:col-span-2 space-y-6">
                  <!-- Ingredients -->
                  @if($recipe->ingredients)
                      <x-card>
                          <x-slot:header>
                              <h2 class="text-xl font-semibold">Ingredients</h2>
                          </x-slot>
                          <div class="whitespace-pre-line text-gray-700">{{ $recipe->ingredients }}</div>
                      </x-card>
                  @endif

                  <!-- Instructions -->
                  @if($recipe->instructions)
                      <x-card>
                          <x-slot:header>
                              <h2 class="text-xl font-semibold">Instructions</h2>
                          </x-slot>
                          <div class="whitespace-pre-line text-gray-700">{{ $recipe->instructions }}</div>
                      </x-card>
                  @endif

                  <!-- Notes -->
                  @if($recipe->notes)
                      <x-card>
                          <x-slot:header>
                              <h2 class="text-xl font-semibold">Notes</h2>
                          </x-slot>
                          <div class="whitespace-pre-line text-gray-700">{{ $recipe->notes }}</div>
                      </x-card>
                  @endif
              </div>

              <!-- Sidebar (1/3 width on large screens) -->
              <div class="space-y-6">
                  <!-- Recipe Details -->
                  <x-card>
                      <x-slot:header>
                          <h2 class="text-xl font-semibold">Details</h2>
                      </x-slot>

                      <dl class="space-y-3">
                          @if($recipe->classification)
                              <div>
                                  <dt class="text-sm font-medium text-gray-500">Classification</dt>
                                  <dd class="mt-1 text-sm text-gray-900">
                                      <span class="inline-block px-2 py-1 bg-blue-100 text-blue-800 rounded">
                                          {{ $recipe->classification->name }}
                                      </span>
                                  </dd>
                              </div>
                          @endif

                          @if($recipe->source)
                              <div>
                                  <dt class="text-sm font-medium text-gray-500">Source</dt>
                                  <dd class="mt-1 text-sm text-gray-900">{{ $recipe->source->name }}</dd>
                              </div>
                          @endif

                          @if($recipe->meals->count() > 0)
                              <div>
                                  <dt class="text-sm font-medium text-gray-500">Meals</dt>
                                  <dd class="mt-1 flex flex-wrap gap-2">
                                      @foreach($recipe->meals as $meal)
                                          <span class="inline-block px-2 py-1 bg-green-100 text-green-800 rounded text-sm">
                                              {{ $meal->name }}
                                          </span>
                                      @endforeach
                                  </dd>
                              </div>
                          @endif

                          @if($recipe->preparations->count() > 0)
                              <div>
                                  <dt class="text-sm font-medium text-gray-500">Preparation Methods</dt>
                                  <dd class="mt-1 flex flex-wrap gap-2">
                                      @foreach($recipe->preparations as $preparation)
                                          <span class="inline-block px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-sm">
                                              {{ $preparation->name }}
                                          </span>
                                      @endforeach
                                  </dd>
                              </div>
                          @endif

                          @if($recipe->courses->count() > 0)
                              <div>
                                  <dt class="text-sm font-medium text-gray-500">Courses</dt>
                                  <dd class="mt-1 flex flex-wrap gap-2">
                                      @foreach($recipe->courses as $course)
                                          <span class="inline-block px-2 py-1 bg-purple-100 text-purple-800 rounded text-sm">
                                              {{ $course->name }}
                                          </span>
                                      @endforeach
                                  </dd>
                              </div>
                          @endif

                          <div>
                              <dt class="text-sm font-medium text-gray-500">Date Added</dt>
                              <dd class="mt-1 text-sm text-gray-900">
                                  {{ $recipe->date_added->format('F d, Y') }}
                              </dd>
                          </div>

                          @if($recipe->last_made)
                              <div>
                                  <dt class="text-sm font-medium text-gray-500">Last Made</dt>
                                  <dd class="mt-1 text-sm text-gray-900">
                                      {{ $recipe->last_made->format('F d, Y') }}
                                  </dd>
                              </div>
                          @endif
                      </dl>
                  </x-card>

                  <!-- Nutrition Info -->
                  @if($recipe->hasNutritionInfo())
                      <x-card>
                          <x-slot:header>
                              <h2 class="text-xl font-semibold">Nutrition Facts</h2>
                          </x-slot>

                          <dl class="space-y-2 text-sm">
                              @if($recipe->calories)
                                  <div class="flex justify-between">
                                      <dt class="text-gray-600">Calories</dt>
                                      <dd class="font-medium">{{ $recipe->calories }}</dd>
                                  </div>
                              @endif
                              @if($recipe->total_fat)
                                  <div class="flex justify-between">
                                      <dt class="text-gray-600">Total Fat</dt>
                                      <dd class="font-medium">{{ $recipe->total_fat }}g</dd>
                                  </div>
                              @endif
                              @if($recipe->saturated_fat)
                                  <div class="flex justify-between">
                                      <dt class="text-gray-600">Saturated Fat</dt>
                                      <dd class="font-medium">{{ $recipe->saturated_fat }}g</dd>
                                  </div>
                              @endif
                              @if($recipe->cholesterol)
                                  <div class="flex justify-between">
                                      <dt class="text-gray-600">Cholesterol</dt>
                                      <dd class="font-medium">{{ $recipe->cholesterol }}mg</dd>
                                  </div>
                              @endif
                              @if($recipe->sodium)
                                  <div class="flex justify-between">
                                      <dt class="text-gray-600">Sodium</dt>
                                      <dd class="font-medium">{{ $recipe->sodium }}mg</dd>
                                  </div>
                              @endif
                              @if($recipe->total_carbohydrates)
                                  <div class="flex justify-between">
                                      <dt class="text-gray-600">Total Carbs</dt>
                                      <dd class="font-medium">{{ $recipe->total_carbohydrates }}g</dd>
                                  </div>
                              @endif
                              @if($recipe->dietary_fiber)
                                  <div class="flex justify-between">
                                      <dt class="text-gray-600">Dietary Fiber</dt>
                                      <dd class="font-medium">{{ $recipe->dietary_fiber }}g</dd>
                                  </div>
                              @endif
                              @if($recipe->sugars)
                                  <div class="flex justify-between">
                                      <dt class="text-gray-600">Sugars</dt>
                                      <dd class="font-medium">{{ $recipe->sugars }}g</dd>
                                  </div>
                              @endif
                              @if($recipe->protein)
                                  <div class="flex justify-between">
                                      <dt class="text-gray-600">Protein</dt>
                                      <dd class="font-medium">{{ $recipe->protein }}g</dd>
                                  </div>
                              @endif
                          </dl>
                      </x-card>
                  @endif

                  <!-- Cookbooks -->
                  @if($recipe->cookbooks->count() > 0)
                      <x-card>
                          <x-slot:header>
                              <h2 class="text-xl font-semibold">In Cookbooks</h2>
                          </x-slot>

                          <ul class="space-y-2">
                              @foreach($recipe->cookbooks as $cookbook)
                                  <li>
                                      <a href="{{ route('cookbooks.show', $cookbook) }}"
                                         class="text-blue-600 hover:text-blue-800">
                                          {{ $cookbook->name }}
                                      </a>
                                  </li>
                              @endforeach
                          </ul>
                      </x-card>
                  @endif
              </div>
          </div>
      </div>
  @endsection
  ```
- [ ] Add helper method to Recipe model:
  ```php
  public function hasNutritionInfo(): bool
  {
      return $this->calories || $this->total_fat || $this->saturated_fat ||
             $this->cholesterol || $this->sodium || $this->total_carbohydrates ||
             $this->dietary_fiber || $this->sugars || $this->protein;
  }
  ```
- [ ] Uses base layout with dynamic title
- [ ] Back button to recipe index
- [ ] Two-column layout (2/3 content, 1/3 sidebar on large screens)
- [ ] Main content shows ingredients, instructions, notes
- [ ] Sidebar shows all metadata and relationships
- [ ] Color-coded badges for different relationship types
- [ ] Nutrition facts panel (only if data exists)
- [ ] Cookbooks list with links
- [ ] Responsive layout (stacks on mobile)
- [ ] Preserves whitespace in text fields
- [ ] Handles missing/null data gracefully

**Files to Create/Modify**:
- `resources/views/recipes/show.blade.php` (create)
- `app/Models/Recipe.php` (add hasNutritionInfo method)

**Testing**:
Manual testing:
1. Visit a recipe detail page
2. Verify all sections display correctly
3. Verify back button works
4. Verify responsive layout on mobile
5. Verify nutrition panel only shows when data exists
6. Verify relationship badges display
7. Verify cookbook links work
8. Verify whitespace preserved in instructions/ingredients

**Story**:
```
As a user
I want to view complete recipe details
So that I can follow the recipe and see all information
```

---

### M7-3: Style Recipe Index with Tailwind
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M7-1 (Recipe index view created)
**Blocks**: M7-5 (End-to-end testing)

**Description**:
Polish recipe index view with enhanced Tailwind styling, transitions, and responsive design.

**Acceptance Criteria**:
- [ ] Enhanced hover states on recipe cards:
  ```css
  .recipe-card {
      @apply transition-all duration-200 ease-in-out;
  }
  .recipe-card:hover {
      @apply shadow-xl transform -translate-y-1;
  }
  ```
- [ ] Smooth transitions on all interactive elements
- [ ] Focus states for accessibility (keyboard navigation)
- [ ] Loading states for form submission (optional)
- [ ] Improved spacing and typography hierarchy
- [ ] Responsive grid tested at all breakpoints:
  - [ ] Mobile (320px-639px): 1 column
  - [ ] Tablet (640px-1023px): 2 columns
  - [ ] Desktop (1024px-1279px): 3 columns
  - [ ] Large (1280px+): 4 columns
- [ ] Empty state styling enhanced
- [ ] Verified color contrast meets WCAG AA standards
- [ ] Added subtle animations (fade-in for cards)

**Files to Create/Modify**:
- `resources/views/recipes/index.blade.php` (enhance styling)
- `resources/css/app.css` (add custom utilities if needed)

**Testing**:
Manual testing:
1. Test all breakpoints (resize browser)
2. Verify hover effects smooth
3. Test keyboard navigation (tab through elements)
4. Test with screen reader (basic check)
5. Verify color contrast (browser dev tools)
6. Verify animations not jarring

Browser testing:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

**Story**:
```
As a user
I want a polished and responsive recipe listing
So that the interface feels professional and works on all devices
```

---

### M7-4: Style Recipe Show with Tailwind
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M7-2 (Recipe show view created)
**Blocks**: M7-5 (End-to-end testing)

**Description**:
Polish recipe detail view with enhanced Tailwind styling and responsive design.

**Acceptance Criteria**:
- [ ] Enhanced card layouts with proper shadows and borders
- [ ] Improved typography hierarchy:
  - [ ] Clear distinction between headings and content
  - [ ] Proper line height for readability
  - [ ] Appropriate font sizes at all breakpoints
- [ ] Color-coded badges consistent and accessible
- [ ] Responsive layout tested:
  - [ ] Mobile: Single column, full width
  - [ ] Tablet: Single column with better spacing
  - [ ] Desktop: Two column (2/3 + 1/3) layout
- [ ] Print styles (optional):
  ```css
  @media print {
      .no-print { display: none; }
      .recipe-content { max-width: 100%; }
  }
  ```
- [ ] Back button styling consistent
- [ ] Smooth transitions on badge hover
- [ ] Enhanced nutrition facts table styling
- [ ] Improved spacing in definition lists

**Files to Create/Modify**:
- `resources/views/recipes/show.blade.php` (enhance styling)
- `resources/css/app.css` (add print styles if needed)

**Testing**:
Manual testing:
1. Test responsive layout at all breakpoints
2. Verify readability of long instructions
3. Test print layout (Ctrl/Cmd+P)
4. Verify badge colors accessible
5. Test with recipe with all fields populated
6. Test with recipe with minimal fields

**Story**:
```
As a user
I want a well-designed recipe detail page
So that recipes are easy to read and follow
```

---

### M7-5: Test Recipe Views End-to-End
**Type**: `type:testing`
**Priority**: `P1`
**Effort**: `effort:medium` (1-2 hours)
**Depends On**: M7-1, M7-2, M7-3, M7-4 (All recipe views complete)
**Blocks**: None

**Description**:
Comprehensive end-to-end testing of recipe views covering all functionality, responsiveness, and edge cases.

**Acceptance Criteria**:
- [ ] **Functional Testing**:
  - [ ] Search functionality works correctly
  - [ ] Sorting works for all fields and directions
  - [ ] Pagination maintains filters
  - [ ] Display count changes results per page
  - [ ] Clear filters button resets correctly
  - [ ] Recipe detail page shows all information
  - [ ] Back button navigates correctly
  - [ ] All links functional (recipes, cookbooks, sources)
  - [ ] Empty states display appropriately
- [ ] **Responsive Testing** (all pages):
  - [ ] Mobile (320px-639px): Single column, stacked layout
  - [ ] Tablet (640px-1023px): 2 columns, proper spacing
  - [ ] Desktop (1024px-1279px): 3 columns, optimal layout
  - [ ] Large (1280px+): 4 columns, maximum width constrained
  - [ ] Navigation menu responsive
  - [ ] Forms usable on all devices
- [ ] **Cross-Browser Testing**:
  - [ ] Chrome/Edge (latest)
  - [ ] Firefox (latest)
  - [ ] Safari (desktop and iOS)
  - [ ] Mobile browsers (Chrome Mobile, Safari Mobile)
- [ ] **Accessibility Testing**:
  - [ ] Keyboard navigation works (tab through all elements)
  - [ ] Focus indicators visible
  - [ ] Color contrast meets WCAG AA
  - [ ] Screen reader compatibility (basic test)
  - [ ] Semantic HTML used throughout
  - [ ] ARIA labels where appropriate
- [ ] **Performance Testing**:
  - [ ] Page load times acceptable (<2s)
  - [ ] Images optimized (if any added later)
  - [ ] No N+1 query issues (check logs)
  - [ ] Smooth animations and transitions
- [ ] **Edge Case Testing**:
  - [ ] Recipe with all fields populated
  - [ ] Recipe with minimal fields (only required)
  - [ ] Recipe with very long text fields
  - [ ] Recipe with no relationships
  - [ ] Search with no results
  - [ ] Search with special characters
  - [ ] Large result sets (100+ recipes)
  - [ ] Empty database (no recipes)
- [ ] **Documentation**:
  - [ ] Create `docs/testing/recipe-views-test-plan.md`
  - [ ] Document test results and any issues found
  - [ ] Document browser compatibility notes
  - [ ] Screenshot key responsive breakpoints

**Files to Create/Modify**:
- `docs/testing/recipe-views-test-plan.md` (create)
- Fix any issues found during testing

**Testing Checklist**:
```markdown
## Recipe Index View
- [ ] Search by recipe name
- [ ] Search by ingredients
- [ ] Sort by name (asc/desc)
- [ ] Sort by date added (asc/desc)
- [ ] Change display count (25/50/100)
- [ ] Pagination (next, previous, specific page)
- [ ] Clear filters
- [ ] Empty state (no results)
- [ ] Recipe cards clickable
- [ ] Responsive at all breakpoints
- [ ] Keyboard navigation
- [ ] Screen reader compatibility

## Recipe Show View
- [ ] All sections render (ingredients, instructions, notes)
- [ ] Classification badge displays
- [ ] Source displays
- [ ] Meals display
- [ ] Preparations display
- [ ] Courses display
- [ ] Dates display correctly
- [ ] Nutrition info (when present)
- [ ] Cookbooks list (when present)
- [ ] Back button works
- [ ] Responsive layout
- [ ] Print layout (optional)
- [ ] Whitespace preserved in text fields
```

**Story**:
```
As a QA tester
I want comprehensive test coverage of recipe views
So that we can confidently ship a quality product
```

---

## Summary

**Total Issues**: 5
**Can Run in Parallel**: M7-1 and M7-2 can run in parallel, then M7-3 and M7-4 in parallel
**Critical Path**: M7-1 → M7-3 → M7-5
**Estimated Milestone Completion**: 4-6 hours with 2-3 agents, 8-12 hours solo

**Parallel Execution Strategy**:
- **Wave 1** (Parallel):
  - **Agent 1**: M7-1 (Recipe index view)
  - **Agent 2**: M7-2 (Recipe show view)
- **Wave 2** (Parallel after Wave 1):
  - **Agent 1**: M7-3 (Style index)
  - **Agent 2**: M7-4 (Style show)
- **Wave 3** (After Wave 2):
  - **Agent 1**: M7-5 (End-to-end testing)

**Dependency Chain**:
```
M6-6, M6-7, M6-8, M5-6 → M7-1 → M7-3 ↘
                                     M7-5
M6-5, M5-2 → M7-2 → M7-4            ↗
```

**Success Criteria**:
Complete recipe listing and detail views created and styled. All functionality working (search, sort, pagination). Responsive design tested at all breakpoints. Cross-browser compatibility verified. Accessibility standards met. End-to-end testing complete with all issues resolved.
