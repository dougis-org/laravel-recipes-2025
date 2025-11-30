# Milestone 9 - Interactivity

**Goal**: Add Alpine.js interactivity for enhanced user experience

**Estimated Total Effort**: 4-6 hours
**Can Start**: After M6-9, M2-4, M6-8, M7-1 complete
**Parallel Capacity**: 3-4 agents (good parallelization possible)

---

## Issues

### M9-1: Add Mobile Menu Toggle
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M6-9 (Navigation component), M2-4 (Alpine.js installed)
**Blocks**: None

**Description**:
Add Alpine.js functionality to toggle mobile navigation menu on small screens.

**Acceptance Criteria**:
- [ ] Updated `resources/views/components/navigation.blade.php`:
  ```blade
  <nav class="bg-white shadow-sm border-b border-gray-200" x-data="{ mobileMenuOpen: false }">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16">
              <!-- ... existing desktop nav ... -->

              <!-- Mobile menu button -->
              <div class="flex items-center sm:hidden">
                  <button
                      type="button"
                      @click="mobileMenuOpen = !mobileMenuOpen"
                      class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
                      :aria-expanded="mobileMenuOpen.toString()"
                  >
                      <span class="sr-only">Open main menu</span>
                      <!-- Hamburger icon -->
                      <svg x-show="!mobileMenuOpen" class="block h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                      </svg>
                      <!-- Close icon -->
                      <svg x-show="mobileMenuOpen" class="block h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                  </button>
              </div>
          </div>
      </div>

      <!-- Mobile menu -->
      <div x-show="mobileMenuOpen" x-transition class="sm:hidden">
          <div class="pt-2 pb-3 space-y-1">
              <a href="{{ route('recipes.index') }}"
                 class="block pl-3 pr-4 py-2 border-l-4 {{ request()->routeIs('recipes.*') ? 'border-blue-500 text-blue-700 bg-blue-50' : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700' }} text-base font-medium">
                  Recipes
              </a>

              <a href="{{ route('cookbooks.index') }}"
                 class="block pl-3 pr-4 py-2 border-l-4 {{ request()->routeIs('cookbooks.*') ? 'border-blue-500 text-blue-700 bg-blue-50' : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700' }} text-base font-medium">
                  Cookbooks
              </a>
          </div>
      </div>
  </nav>
  ```
- [ ] Added `x-data` to track menu state
- [ ] Menu toggles on button click (`@click`)
- [ ] Icons toggle between hamburger and X
- [ ] Menu shows/hides with transition
- [ ] ARIA expanded attribute updates
- [ ] Menu closes when clicking navigation link (optional):
  ```blade
  <a @click="mobileMenuOpen = false" ...>
  ```
- [ ] Accessible keyboard navigation

**Files to Create/Modify**:
- `resources/views/components/navigation.blade.php` (modify)

**Testing**:
Manual testing:
1. Resize browser to mobile width (<640px)
2. Verify mobile menu button appears
3. Click button, verify menu opens
4. Verify hamburger icon changes to X
5. Click button again, verify menu closes
6. Click menu link, verify navigation works
7. Verify smooth transitions
8. Test keyboard navigation (tab to button, press Enter)

**Story**:
```
As a mobile user
I want to toggle the navigation menu
So that I can access all pages on my mobile device
```

---

### M9-2: Add Sort Direction Toggle
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:small` (30 min)
**Depends On**: M6-8 (Sort controls component)
**Blocks**: None

**Description**:
Add visual toggle buttons for sort direction with active state indication.

**Acceptance Criteria**:
- [ ] Updated `resources/views/components/sort-controls.blade.php` to add visual toggle:
  ```blade
  <div class="flex-1">
      <label class="block text-sm font-medium text-gray-700 mb-1">
          Order
      </label>
      <div class="flex rounded-md shadow-sm" role="group">
          <button
              type="button"
              @click="document.getElementById('sortOrder').value = 'asc'; document.getElementById('sortOrder').form.submit()"
              class="relative inline-flex items-center px-4 py-2 rounded-l-md border text-sm font-medium focus:z-10 focus:outline-none focus:ring-2 focus:ring-blue-500
                     {{ request('sortOrder', 'asc') === 'asc' ? 'bg-blue-600 border-blue-600 text-white' : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50' }}"
          >
              <svg class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
              </svg>
              Asc
          </button>
          <button
              type="button"
              @click="document.getElementById('sortOrder').value = 'desc'; document.getElementById('sortOrder').form.submit()"
              class="relative inline-flex items-center px-4 py-2 rounded-r-md border text-sm font-medium focus:z-10 focus:outline-none focus:ring-2 focus:ring-blue-500
                     {{ request('sortOrder', 'asc') === 'desc' ? 'bg-blue-600 border-blue-600 text-white' : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50' }}"
          >
              <svg class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
              Desc
          </button>
      </div>
      <input type="hidden" id="sortOrder" name="sortOrder" value="{{ request('sortOrder', 'asc') }}">
  </div>
  ```
- [ ] Replaced dropdown with button group
- [ ] Active button highlighted (blue background)
- [ ] Inactive buttons show hover state
- [ ] Icons for ascending/descending
- [ ] Clicking button updates hidden input and submits form
- [ ] Accessible button group with role="group"
- [ ] Keyboard accessible

**Files to Create/Modify**:
- `resources/views/components/sort-controls.blade.php` (modify)

**Testing**:
Manual testing:
1. Visit recipe index page
2. Verify toggle buttons display
3. Verify active state shows correctly
4. Click ascending, verify sort updates
5. Click descending, verify sort updates
6. Verify icons appropriate
7. Test keyboard navigation

**Story**:
```
As a user
I want intuitive sort direction controls
So that I can quickly change sort order
```

---

### M9-3: Add Display Count Selector Enhancement
**Type**: `type:feature`
**Priority**: `P3`
**Effort**: `effort:small` (15-30 min)
**Depends On**: M6-4 (Select component)
**Blocks**: None

**Description**:
Enhance display count selector with visual feedback and loading indication.

**Acceptance Criteria**:
- [ ] Add loading indicator when changing display count:
  ```blade
  <div x-data="{ loading: false }">
      <label for="displayCount" class="block text-sm font-medium text-gray-700 mb-1">
          Items per page
      </label>
      <div class="relative">
          <select
              name="displayCount"
              id="displayCount"
              @change="loading = true; $el.form.submit()"
              :disabled="loading"
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              :class="loading ? 'opacity-50 cursor-wait' : ''"
          >
              <option value="25" {{ request('displayCount', 25) == 25 ? 'selected' : '' }}>25</option>
              <option value="50" {{ request('displayCount') == 50 ? 'selected' : '' }}>50</option>
              <option value="100" {{ request('displayCount') == 100 ? 'selected' : '' }}>100</option>
          </select>

          <div x-show="loading" class="absolute inset-y-0 right-8 flex items-center pointer-events-none">
              <svg class="animate-spin h-5 w-5 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
          </div>
      </div>
  </div>
  ```
- [ ] Loading state when form submitting
- [ ] Spinner icon during loading
- [ ] Disabled state during submission
- [ ] Opacity change for visual feedback

**Files to Create/Modify**:
- `resources/views/recipes/index.blade.php` (modify display count selector)

**Testing**:
Manual testing:
1. Change display count
2. Verify loading spinner appears
3. Verify select disabled during load
4. Verify page reloads with new count

**Story**:
```
As a user
I want visual feedback when changing display count
So that I know my action is being processed
```

---

### M9-4: Add Search Form Enhancement
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:small` (30 min)
**Depends On**: M7-1 (Recipe index view)
**Blocks**: None

**Description**:
Enhance search form with clear button, active state, and keyboard shortcuts.

**Acceptance Criteria**:
- [ ] Add clear button to search input:
  ```blade
  <div x-data="{ search: '{{ request('search') }}' }">
      <label for="search" class="block text-sm font-medium text-gray-700 mb-1">
          Search Recipes
      </label>
      <div class="relative">
          <input
              type="text"
              name="search"
              id="search"
              x-model="search"
              placeholder="Search by name or ingredients..."
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 pr-10"
          />

          <button
              x-show="search.length > 0"
              @click="search = ''; $refs.searchInput.focus()"
              type="button"
              class="absolute inset-y-0 right-0 flex items-center pr-3"
          >
              <svg class="h-5 w-5 text-gray-400 hover:text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
          </button>
      </div>
  </div>
  ```
- [ ] Clear (X) button appears when search has value
- [ ] Clicking X clears search and focuses input
- [ ] Active search state indicated visually
- [ ] Keyboard shortcut (optional): Press "/" to focus search:
  ```javascript
  document.addEventListener('keydown', (e) => {
      if (e.key === '/' && !['INPUT', 'TEXTAREA'].includes(e.target.tagName)) {
          e.preventDefault();
          document.getElementById('search').focus();
      }
  });
  ```

**Files to Create/Modify**:
- `resources/views/recipes/index.blade.php` (modify search form)
- `resources/js/app.js` (add keyboard shortcut - optional)

**Testing**:
Manual testing:
1. Type in search box
2. Verify X button appears
3. Click X, verify search clears
4. Verify focus returns to input
5. Press "/" key, verify search focused (if implemented)

**Story**:
```
As a user
I want to easily clear my search
So that I can quickly start a new search
```

---

### M9-5: Add Hover Effects to Cards
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:small` (30 min)
**Depends On**: M6-6 (Recipe card component)
**Blocks**: None

**Description**:
Enhance recipe and cookbook cards with advanced hover effects and animations.

**Acceptance Criteria**:
- [ ] Update `resources/views/components/recipe-card.blade.php`:
  ```blade
  <x-card class="group hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
      <a href="{{ route('recipes.show', $recipe) }}" class="block">
          <div class="space-y-3">
              <h3 class="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors duration-200">
                  {{ $recipe->name }}
              </h3>

              @if($recipe->classification)
                  <span class="inline-block px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded group-hover:bg-blue-200 transition-colors duration-200">
                      {{ $recipe->classification->name }}
                  </span>
              @endif

              <!-- ... rest of card ... -->
          </div>
      </a>
  </x-card>
  ```
- [ ] Card lifts up on hover (`transform hover:-translate-y-1`)
- [ ] Shadow intensifies on hover
- [ ] Title color changes on hover
- [ ] Badge color intensifies on hover
- [ ] Smooth transitions (300ms duration)
- [ ] Group hover for child elements
- [ ] Similar effects for cookbook cards

**Files to Create/Modify**:
- `resources/views/components/recipe-card.blade.php` (modify)
- Similar updates for cookbook cards in cookbook views

**Testing**:
Manual testing:
1. Hover over recipe cards
2. Verify lift effect smooth
3. Verify shadow transition
4. Verify color changes
5. Verify transitions not jarring
6. Test on different browsers

**Story**:
```
As a user
I want visual feedback when hovering over cards
So that the interface feels responsive and interactive
```

---

### M9-6: Test All Interactive Features
**Type**: `type:testing`
**Priority**: `P1`
**Effort**: `effort:medium` (1-2 hours)
**Depends On**: M9-1 through M9-5 (All interactivity features)
**Blocks**: None

**Description**:
Comprehensive testing of all Alpine.js interactive features across devices and browsers.

**Acceptance Criteria**:
- [ ] **Mobile Menu Testing**:
  - [ ] Opens and closes smoothly
  - [ ] Icons toggle correctly
  - [ ] Transitions smooth
  - [ ] Closes when clicking links (if implemented)
  - [ ] Accessible via keyboard
  - [ ] ARIA attributes correct
- [ ] **Sort Controls Testing**:
  - [ ] Toggle buttons work
  - [ ] Active state displays correctly
  - [ ] Form submits on click
  - [ ] Sort order updates correctly
  - [ ] Keyboard accessible
- [ ] **Display Count Testing**:
  - [ ] Loading indicator appears
  - [ ] Select disabled during load
  - [ ] Page updates correctly
  - [ ] Smooth user experience
- [ ] **Search Enhancements Testing**:
  - [ ] Clear button appears/hides correctly
  - [ ] Clear button works
  - [ ] Focus returns to input
  - [ ] Keyboard shortcut works (if implemented)
- [ ] **Hover Effects Testing**:
  - [ ] Cards lift on hover
  - [ ] Shadows transition smoothly
  - [ ] Colors change appropriately
  - [ ] No layout shift
  - [ ] Works on touch devices
- [ ] **Cross-Browser Testing**:
  - [ ] Chrome/Edge: All features work
  - [ ] Firefox: All features work
  - [ ] Safari: All features work
  - [ ] Mobile browsers: All features work
- [ ] **Accessibility Testing**:
  - [ ] All interactive elements keyboard accessible
  - [ ] Focus indicators visible
  - [ ] Screen reader announces state changes
  - [ ] ARIA attributes present and correct
- [ ] **Performance Testing**:
  - [ ] No JavaScript errors in console
  - [ ] Smooth 60fps animations
  - [ ] No memory leaks
  - [ ] Alpine.js bundle size acceptable

**Files to Create/Modify**:
- `docs/testing/interactivity-test-plan.md` (create)
- Fix any issues found

**Testing Checklist**:
```markdown
## Mobile Menu
- [ ] Opens/closes on click
- [ ] Icon toggle
- [ ] Smooth transitions
- [ ] Keyboard accessible
- [ ] Works on mobile devices

## Sort Controls
- [ ] Toggle buttons functional
- [ ] Active state correct
- [ ] Form submission works
- [ ] Keyboard accessible

## Display Count
- [ ] Loading indicator shows
- [ ] Disabled during load
- [ ] Correct results loaded

## Search Enhancements
- [ ] Clear button functional
- [ ] Focus management
- [ ] Keyboard shortcut (if implemented)

## Hover Effects
- [ ] Cards lift smoothly
- [ ] Shadow transitions
- [ ] Color changes
- [ ] No layout shift
```

**Story**:
```
As a QA tester
I want comprehensive testing of interactive features
So that the user experience is smooth and reliable
```

---

## Summary

**Total Issues**: 6
**Can Run in Parallel**: M9-1 through M9-5 can all run in parallel (independent features)
**Critical Path**: M9-1 through M9-5 → M9-6
**Estimated Milestone Completion**: 4-6 hours with 3-4 agents, 8-12 hours solo

**Parallel Execution Strategy**:
- **Wave 1** (All parallel):
  - **Agent 1**: M9-1 (Mobile menu toggle)
  - **Agent 2**: M9-2 (Sort direction toggle)
  - **Agent 3**: M9-3 (Display count enhancement)
  - **Agent 4**: M9-4 (Search enhancements)
  - **Agent 5**: M9-5 (Hover effects)
- **Wave 2** (After Wave 1):
  - **Agent 1**: M9-6 (Testing)

**Dependency Chain**:
```
M6-9, M2-4 → M9-1 ↘
M6-8 → M9-2       ↘
M6-4 → M9-3        → M9-6
M7-1 → M9-4       ↗
M6-6 → M9-5      ↗
```

**Success Criteria**:
All Alpine.js interactivity features implemented and working. Mobile menu toggles smoothly. Sort controls intuitive. Search enhancements functional. Hover effects polished. All features tested across browsers and devices. No JavaScript errors. Smooth performance.
