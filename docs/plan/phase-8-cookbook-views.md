# Milestone 8 - Cookbook Views

**Goal**: Create cookbook listing and detail views with full Tailwind styling

**Estimated Total Effort**: 3-4 hours
**Can Start**: After M5-7, M5-4, M7-1 complete
**Parallel Capacity**: 2 agents (some parallelization possible)

---

## Issues

### M8-1 (#334): Create Cookbook Index View
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M5-7 (Cookbook routes)
**Blocks**: M8-3 (Styling)

**Description**:
Create cookbook index view displaying all cookbooks with recipe counts in grid/list layout.

**Acceptance Criteria**:
- [ ] Created `resources/views/cookbooks/index.blade.php`:
  ```blade
  @extends('layouts.app')

  @section('title', 'Cookbooks')

  @section('content')
      <div class="space-y-6">
          <!-- Header -->
          <div class="flex justify-between items-center">
              <h1 class="text-3xl font-bold text-gray-900">Cookbooks</h1>
              <p class="text-gray-600">
                  {{ $cookbooks->count() }} {{ Str::plural('cookbook', $cookbooks->count()) }}
              </p>
          </div>

          <!-- Cookbooks Grid/List -->
          @if($cookbooks->count() > 0)
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  @foreach($cookbooks as $cookbook)
                      <x-card class="hover:shadow-lg transition duration-200">
                          <a href="{{ route('cookbooks.show', $cookbook) }}" class="block">
                              <div class="space-y-3">
                                  <h2 class="text-xl font-semibold text-gray-900 hover:text-blue-600 transition">
                                      {{ $cookbook->name }}
                                  </h2>

                                  <p class="text-sm text-gray-600">
                                      {{ $cookbook->recipes_count }} {{ Str::plural('recipe', $cookbook->recipes_count) }}
                                  </p>

                                  @if($cookbook->description)
                                      <p class="text-sm text-gray-700 line-clamp-2">
                                          {{ $cookbook->description }}
                                      </p>
                                  @endif
                              </div>
                          </a>
                      </x-card>
                  @endforeach
              </div>
          @else
              <!-- Empty State -->
              <div class="bg-white rounded-lg shadow-sm p-12 text-center">
                  <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                  <h3 class="mt-2 text-sm font-medium text-gray-900">No cookbooks</h3>
                  <p class="mt-1 text-sm text-gray-500">
                      Get started by creating your first cookbook.
                  </p>
              </div>
          @endif
      </div>
  @endsection
  ```
- [ ] Uses base layout with title
- [ ] Shows total cookbook count in header
- [ ] Displays cookbooks in responsive grid (1/2/3 columns)
- [ ] Shows recipe count for each cookbook
- [ ] Shows cookbook description (if present) with line-clamp
- [ ] Links to cookbook detail pages
- [ ] Hover effects on cards
- [ ] Empty state when no cookbooks
- [ ] Uses card component

**Files to Create/Modify**:
- `resources/views/cookbooks/index.blade.php` (create)

**Testing**:
Manual testing:
1. Visit `/cookbooks`
2. Verify cookbooks display in grid
3. Verify recipe counts show correctly
4. Verify descriptions truncate properly
5. Verify links navigate to cookbook detail
6. Verify empty state when no cookbooks
7. Verify responsive grid at different screen sizes

**Story**:
```
As a user
I want to view all my cookbooks
So that I can browse and select one to view
```

---

### M8-2 (#314): Create Cookbook Show View
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:medium` (1-2 hours)
**Depends On**: M5-4 (CookbookController show), M7-1 (Recipe card component)
**Blocks**: M8-3 (Styling)

**Description**:
Create cookbook detail view showing ordered recipes from the cookbook.

**Acceptance Criteria**:
- [ ] Created `resources/views/cookbooks/show.blade.php`:
  ```blade
  @extends('layouts.app')

  @section('title', $cookbook->name)

  @section('content')
      <div class="space-y-6">
          <!-- Header with Back Button -->
          <div>
              <a href="{{ route('cookbooks.index') }}" class="inline-flex items-center text-blue-600 hover:text-blue-800 mb-4">
                  <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                  Back to Cookbooks
              </a>
              <h1 class="text-4xl font-bold text-gray-900">{{ $cookbook->name }}</h1>

              @if($cookbook->description)
                  <p class="mt-2 text-gray-600">{{ $cookbook->description }}</p>
              @endif

              <p class="mt-2 text-sm text-gray-500">
                  {{ $cookbook->recipes->count() }} {{ Str::plural('recipe', $cookbook->recipes->count()) }}
              </p>
          </div>

          <!-- Recipes -->
          @if($cookbook->recipes->count() > 0)
              @php
                  $recipesByClassification = $cookbook->recipes->groupBy('classification_id');
              @endphp

              @foreach($recipesByClassification as $classificationId => $recipes)
                  <div class="space-y-4">
                      @if($recipes->first()->classification)
                          <h2 class="text-2xl font-semibold text-gray-800 border-b-2 border-gray-200 pb-2">
                              {{ $recipes->first()->classification->name }}
                          </h2>
                      @else
                          <h2 class="text-2xl font-semibold text-gray-800 border-b-2 border-gray-200 pb-2">
                              Uncategorized
                          </h2>
                      @endif

                      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                          @foreach($recipes->sortBy('name') as $recipe)
                              <x-recipe-card :recipe="$recipe" />
                          @endforeach
                      </div>
                  </div>
              @endforeach
          @else
              <!-- Empty State -->
              <div class="bg-white rounded-lg shadow-sm p-12 text-center">
                  <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <h3 class="mt-2 text-sm font-medium text-gray-900">No recipes in this cookbook</h3>
                  <p class="mt-1 text-sm text-gray-500">
                      Add recipes to this cookbook to get started.
                  </p>
              </div>
          @endif
      </div>
  @endsection
  ```
- [ ] Uses base layout with dynamic title
- [ ] Back button to cookbook index
- [ ] Shows cookbook name and description
- [ ] Shows total recipe count
- [ ] Groups recipes by classification
- [ ] Classification headings with styled borders
- [ ] Recipes within each classification sorted by name
- [ ] Uses recipe card component
- [ ] Responsive grid layout
- [ ] Empty state when cookbook has no recipes
- [ ] Handles recipes without classification

**Files to Create/Modify**:
- `resources/views/cookbooks/show.blade.php` (create)

**Testing**:
Manual testing:
1. Visit cookbook detail page
2. Verify recipes grouped by classification
3. Verify recipes sorted alphabetically within groups
4. Verify classification headings display
5. Verify back button works
6. Verify empty state when no recipes
7. Verify responsive layout
8. Verify recipe cards clickable

**Story**:
```
As a user
I want to view recipes in a cookbook organized by classification
So that I can find recipes easily within the cookbook
```

---

### M8-3 (#313): Style Cookbook Views
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M8-1 (Cookbook index), M8-2 (Cookbook show)
**Blocks**: M8-4 (Testing)

**Description**:
Polish cookbook views with enhanced Tailwind styling consistent with recipe views.

**Acceptance Criteria**:
- [ ] Enhanced hover states on cookbook cards:
  ```css
  .cookbook-card:hover {
      @apply shadow-xl transform -translate-y-1;
  }
  ```
- [ ] Smooth transitions on all interactive elements
- [ ] Improved typography hierarchy
- [ ] Classification section headers visually distinct
- [ ] Consistent spacing throughout
- [ ] Responsive grid tested at all breakpoints:
  - [ ] Mobile (320px-639px): 1 column
  - [ ] Tablet (640px-1023px): 2 columns
  - [ ] Desktop (1024px+): 3 columns
- [ ] Color scheme consistent with recipe views
- [ ] Empty states styled appropriately
- [ ] Focus states for accessibility

**Files to Create/Modify**:
- `resources/views/cookbooks/index.blade.php` (enhance styling)
- `resources/views/cookbooks/show.blade.php` (enhance styling)

**Testing**:
Manual testing:
1. Test all breakpoints
2. Verify hover effects
3. Test keyboard navigation
4. Verify consistent styling with recipe views
5. Verify classification sections distinct

**Story**:
```
As a user
I want cookbook views to be polished and consistent
So that the interface feels cohesive across the application
```

---

### M8-4 (#330): Test Cookbook Views
**Type**: `type:testing`
**Priority**: `P1`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M8-1, M8-2, M8-3 (All cookbook views complete)
**Blocks**: None

**Description**:
Comprehensive testing of cookbook views covering functionality, responsiveness, and edge cases.

**Acceptance Criteria**:
- [ ] **Functional Testing**:
  - [ ] Cookbook index displays all cookbooks
  - [ ] Recipe counts accurate
  - [ ] Links to cookbook detail work
  - [ ] Cookbook detail shows recipes
  - [ ] Recipes grouped by classification correctly
  - [ ] Recipes sorted alphabetically within groups
  - [ ] Back button navigates correctly
  - [ ] Empty states display appropriately
- [ ] **Recipe Ordering Testing**:
  - [ ] Create test cookbook with recipes from multiple classifications
  - [ ] Verify grouping by classification works
  - [ ] Verify alphabetical sorting within each group
  - [ ] Verify recipes without classification appear in "Uncategorized"
  - [ ] Document expected order in test data
- [ ] **Responsive Testing**:
  - [ ] Mobile: Single column layout
  - [ ] Tablet: 2 columns
  - [ ] Desktop: 3 columns
  - [ ] Classification headers responsive
- [ ] **Cross-Browser Testing**:
  - [ ] Chrome/Edge
  - [ ] Firefox
  - [ ] Safari
- [ ] **Edge Cases**:
  - [ ] Empty cookbooks (no recipes)
  - [ ] Cookbook with 100+ recipes
  - [ ] Cookbook with very long name/description
  - [ ] Cookbook with recipes from all classifications
  - [ ] Cookbook with only uncategorized recipes
  - [ ] No cookbooks in system

**Files to Create/Modify**:
- `docs/testing/cookbook-views-test-plan.md` (create)
- Fix any issues found

**Testing Checklist**:
```markdown
## Cookbook Index View
- [ ] Displays all cookbooks
- [ ] Recipe counts correct
- [ ] Descriptions truncate properly
- [ ] Hover effects work
- [ ] Links functional
- [ ] Empty state (no cookbooks)
- [ ] Responsive at all breakpoints

## Cookbook Show View
- [ ] Cookbook name and description display
- [ ] Recipe count accurate
- [ ] Recipes grouped by classification
- [ ] Recipes sorted by name within groups
- [ ] Classification headers display
- [ ] Recipe cards clickable
- [ ] Back button works
- [ ] Empty state (no recipes)
- [ ] Responsive layout
```

**Story**:
```
As a QA tester
I want comprehensive test coverage of cookbook views
So that cookbook functionality is reliable
```

---

## Summary

**Total Issues**: 4
**Can Run in Parallel**: M8-1 and M8-2 can run in parallel, then M8-3 depends on both
**Critical Path**: M8-1, M8-2 → M8-3 → M8-4
**Estimated Milestone Completion**: 3-4 hours with 2 agents, 6-8 hours solo

**Parallel Execution Strategy**:
- **Wave 1** (Parallel):
  - **Agent 1**: M8-1 (Cookbook index view)
  - **Agent 2**: M8-2 (Cookbook show view)
- **Wave 2** (After Wave 1):
  - **Agent 1**: M8-3 (Styling)
- **Wave 3** (After Wave 2):
  - **Agent 1**: M8-4 (Testing)

**Dependency Chain**:
```
M5-7 → M8-1 ↘
              M8-3 → M8-4
M5-4, M7-1 → M8-2 ↗
```

**Success Criteria**:
Cookbook listing and detail views created and styled. Recipe ordering (by classification, then name) working correctly. Responsive design tested. All functionality working including empty states. Testing complete with issues resolved.
