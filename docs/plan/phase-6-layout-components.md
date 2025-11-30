# Milestone 6 - Layout & Components

**Goal**: Create base layout and reusable Blade components styled with Tailwind CSS

**Estimated Total Effort**: 8-10 hours
**Can Start**: After M2-5 complete (Base layout with Vite)
**Parallel Capacity**: 4-5 agents (excellent parallelization after M6-1)

---

## Issues

### M6-1 (#303): Create Base App Layout
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:medium` (1-2 hours)
**Depends On**: M2-5 (Base layout with Vite directives)
**Blocks**: M6-2 through M6-10 (All components), M7-1 (Recipe views)

**Description**:
Create comprehensive base application layout with proper HTML structure, meta tags, Vite directives, and content sections.

**Acceptance Criteria**:
- [ ] Updated `resources/views/layouts/app.blade.php` with complete structure:
  ```blade
  <!DOCTYPE html>
  <html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
  <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta name="csrf-token" content="{{ csrf_token() }}">

      <title>{{ config('app.name', 'Laravel Recipes') }} - @yield('title', 'Home')</title>

      @vite(['resources/css/app.css', 'resources/js/app.js'])
  </head>
  <body class="bg-gray-50 text-gray-900 antialiased">
      <div class="min-h-screen">
          @include('components.navigation')

          <main class="py-8">
              <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                  @yield('content')
              </div>
          </main>

          <footer class="bg-white border-t border-gray-200 mt-auto">
              <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                  <p class="text-center text-gray-500 text-sm">
                      &copy; {{ date('Y') }} {{ config('app.name') }}. All rights reserved.
                  </p>
              </div>
          </footer>
      </div>
  </body>
  </html>
  ```
- [ ] Includes proper DOCTYPE and HTML5 structure
- [ ] Includes charset and viewport meta tags
- [ ] Includes CSRF token meta tag for AJAX requests
- [ ] Dynamic page title with default
- [ ] Vite directives for CSS and JS
- [ ] Tailwind utility classes for base styling
- [ ] Sticky footer layout
- [ ] Navigation include (will be created in M6-9)
- [ ] Responsive max-width container
- [ ] Main content section with proper padding
- [ ] Created alternative slot-based layout:
  ```blade
  <!-- resources/views/layouts/app-component.blade.php -->
  <x-layout :title="$title ?? 'Home'">
      {{ $slot }}
  </x-layout>
  ```

**Files to Create/Modify**:
- `resources/views/layouts/app.blade.php` (modify)

**Testing**:
Create test view:
```blade
<!-- resources/views/test/layout.blade.php -->
@extends('layouts.app')

@section('title', 'Layout Test')

@section('content')
    <h1 class="text-3xl font-bold text-blue-600">Layout Test</h1>
    <p class="mt-4">This tests the base layout structure.</p>
@endsection
```

Add test route:
```php
Route::get('/test/layout', function () {
    return view('test.layout');
});
```

Manual testing:
1. Visit `/test/layout`
2. Verify page title shows "Laravel Recipes - Layout Test"
3. Verify Tailwind styles apply
4. Verify responsive container works
5. Verify footer sticks to bottom
6. Inspect source: verify meta tags present

**Story**:
```
As a developer
I want a comprehensive base layout
So that all pages have consistent structure and styling
```

---

### M6-2 (#300): Create Button Component
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M6-1 (Base layout)
**Blocks**: None

**Description**:
Create reusable button component with variant support (primary, secondary, danger).

**Acceptance Criteria**:
- [ ] Created `resources/views/components/button.blade.php`:
  ```blade
  @props([
      'type' => 'button',
      'variant' => 'primary',
  ])

  @php
  $classes = match($variant) {
      'primary' => 'bg-blue-600 hover:bg-blue-700 text-white',
      'secondary' => 'bg-gray-200 hover:bg-gray-300 text-gray-900',
      'danger' => 'bg-red-600 hover:bg-red-700 text-white',
      default => 'bg-blue-600 hover:bg-blue-700 text-white',
  };

  $baseClasses = 'inline-flex items-center px-4 py-2 border border-transparent rounded-md font-semibold text-sm transition duration-150 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500';
  @endphp

  <button type="{{ $type }}" {{ $attributes->merge(['class' => $baseClasses . ' ' . $classes]) }}>
      {{ $slot }}
  </button>
  ```
- [ ] Supports `type` prop (button, submit, reset)
- [ ] Supports `variant` prop (primary, secondary, danger)
- [ ] Includes hover states
- [ ] Includes focus ring for accessibility
- [ ] Allows additional classes via attributes
- [ ] Slot for button content

**Files to Create/Modify**:
- `resources/views/components/button.blade.php` (create)

**Testing**:
Create test view:
```blade
<div class="space-y-4">
    <x-button>Default Primary Button</x-button>
    <x-button variant="secondary">Secondary Button</x-button>
    <x-button variant="danger">Danger Button</x-button>
    <x-button type="submit" variant="primary">Submit Button</x-button>
    <x-button class="ml-4">Button with Extra Class</x-button>
</div>
```

Manual testing:
1. Verify all variants render correctly
2. Verify hover states work
3. Verify focus rings appear on keyboard focus
4. Verify additional classes merge properly

**Story**:
```
As a developer
I want a reusable button component
So that buttons have consistent styling across the application
```

---

### M6-3 (#337): Create Input Component
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M6-1 (Base layout)
**Blocks**: None

**Description**:
Create form input component with label and error display support.

**Acceptance Criteria**:
- [ ] Created `resources/views/components/input.blade.php`:
  ```blade
  @props([
      'label' => null,
      'name' => null,
      'type' => 'text',
      'value' => null,
      'error' => null,
  ])

  <div class="mb-4">
      @if($label)
          <label for="{{ $name }}" class="block text-sm font-medium text-gray-700 mb-1">
              {{ $label }}
          </label>
      @endif

      <input
          type="{{ $type }}"
          name="{{ $name }}"
          id="{{ $name }}"
          value="{{ old($name, $value) }}"
          {{ $attributes->merge(['class' => 'block w-full rounded-md shadow-sm ' . ($error ? 'border-red-300 focus:border-red-500 focus:ring-red-500' : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500')]) }}
      />

      @if($error || $errors->has($name))
          <p class="mt-1 text-sm text-red-600">{{ $error ?? $errors->first($name) }}</p>
      @endif
  </div>
  ```
- [ ] Supports label prop (optional)
- [ ] Supports name, type, value props
- [ ] Integrates with Laravel's `old()` helper
- [ ] Shows validation errors automatically
- [ ] Error state styling (red border/ring)
- [ ] Accessible label association
- [ ] Support for additional attributes

**Files to Create/Modify**:
- `resources/views/components/input.blade.php` (create)

**Testing**:
Create test view:
```blade
<form>
    <x-input
        label="Recipe Name"
        name="name"
        type="text"
        value="Chocolate Cake"
    />

    <x-input
        label="Ingredients"
        name="ingredients"
        type="textarea"
    />

    <x-input
        label="Date Added"
        name="date_added"
        type="date"
        error="This field is required"
    />
</form>
```

Manual testing:
1. Verify labels render and associate with inputs
2. Verify error messages display
3. Verify error state styling applies
4. Verify old input values persist (submit form and check)

**Story**:
```
As a developer
I want a reusable input component
So that forms have consistent styling and error handling
```

---

### M6-4 (#298): Create Select Component
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M6-1 (Base layout)
**Blocks**: M6-8 (Sort controls use select)

**Description**:
Create dropdown select component with label and options support.

**Acceptance Criteria**:
- [ ] Created `resources/views/components/select.blade.php`:
  ```blade
  @props([
      'label' => null,
      'name' => null,
      'options' => [],
      'selected' => null,
      'placeholder' => null,
  ])

  <div class="mb-4">
      @if($label)
          <label for="{{ $name }}" class="block text-sm font-medium text-gray-700 mb-1">
              {{ $label }}
          </label>
      @endif

      <select
          name="{{ $name }}"
          id="{{ $name }}"
          {{ $attributes->merge(['class' => 'block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500']) }}
      >
          @if($placeholder)
              <option value="">{{ $placeholder }}</option>
          @endif

          @foreach($options as $value => $text)
              <option value="{{ $value }}" {{ old($name, $selected) == $value ? 'selected' : '' }}>
                  {{ $text }}
              </option>
          @endforeach
      </select>
  </div>
  ```
- [ ] Supports label prop (optional)
- [ ] Supports options array (value => text)
- [ ] Supports selected value
- [ ] Supports placeholder option
- [ ] Integrates with `old()` helper
- [ ] Accessible label association

**Files to Create/Modify**:
- `resources/views/components/select.blade.php` (create)

**Testing**:
Create test view:
```blade
<x-select
    label="Sort Field"
    name="sortField"
    :options="['name' => 'Name', 'date_added' => 'Date Added']"
    selected="name"
    placeholder="-- Select Sort Field --"
/>

<x-select
    label="Sort Order"
    name="sortOrder"
    :options="['asc' => 'Ascending', 'desc' => 'Descending']"
/>
```

Manual testing:
1. Verify dropdown renders with all options
2. Verify selected value is pre-selected
3. Verify placeholder shows as first option
4. Verify label associates with select

**Story**:
```
As a developer
I want a reusable select component
So that dropdowns have consistent styling
```

---

### M6-5 (#325): Create Card Component
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M6-1 (Base layout)
**Blocks**: M6-6 (Recipe card extends card)

**Description**:
Create flexible card component with header, body, and footer slots.

**Acceptance Criteria**:
- [ ] Created `resources/views/components/card.blade.php`:
  ```blade
  @props([
      'padding' => true,
  ])

  <div {{ $attributes->merge(['class' => 'bg-white rounded-lg shadow-md overflow-hidden']) }}>
      @isset($header)
          <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
              {{ $header }}
          </div>
      @endisset

      <div class="{{ $padding ? 'px-6 py-4' : '' }}">
          {{ $slot }}
      </div>

      @isset($footer)
          <div class="px-6 py-4 border-t border-gray-200 bg-gray-50">
              {{ $footer }}
          </div>
      @endisset
  </div>
  ```
- [ ] Default slot for main content
- [ ] Optional header slot
- [ ] Optional footer slot
- [ ] Padding prop to disable body padding
- [ ] Tailwind styling (white bg, shadow, rounded)
- [ ] Allows additional classes via attributes

**Files to Create/Modify**:
- `resources/views/components/card.blade.php` (create)

**Testing**:
Create test view:
```blade
<x-card>
    <p>Basic card with just content</p>
</x-card>

<x-card class="mt-4">
    <x-slot:header>
        <h2 class="text-xl font-semibold">Card with Header</h2>
    </x-slot>

    <p>Card content goes here</p>

    <x-slot:footer>
        <button>Action</button>
    </x-slot>
</x-card>

<x-card :padding="false">
    <img src="/image.jpg" alt="No padding card">
</x-card>
```

Manual testing:
1. Verify card renders with proper styling
2. Verify header and footer slots work
3. Verify padding prop removes body padding
4. Verify additional classes merge

**Story**:
```
As a developer
I want a flexible card component
So that content can be displayed in consistent containers
```

---

### M6-6 (#338): Create Recipe Card Component
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:medium` (1 hour)
**Depends On**: M6-5 (Card component)
**Blocks**: M7-1 (Recipe index view uses recipe cards)

**Description**:
Create specialized recipe card component for displaying recipe summaries in grid layout.

**Acceptance Criteria**:
- [ ] Created `resources/views/components/recipe-card.blade.php`:
  ```blade
  @props(['recipe'])

  <x-card class="hover:shadow-lg transition duration-200">
      <a href="{{ route('recipes.show', $recipe) }}" class="block">
          <div class="space-y-3">
              <h3 class="text-lg font-semibold text-gray-900 hover:text-blue-600 transition">
                  {{ $recipe->name }}
              </h3>

              @if($recipe->classification)
                  <span class="inline-block px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded">
                      {{ $recipe->classification->name }}
                  </span>
              @endif

              @if($recipe->ingredients)
                  <p class="text-sm text-gray-600 line-clamp-3">
                      {{ Str::limit($recipe->ingredients, 120) }}
                  </p>
              @endif

              <div class="flex items-center justify-between text-xs text-gray-500">
                  @if($recipe->source)
                      <span>{{ $recipe->source->name }}</span>
                  @endif

                  <span>{{ $recipe->date_added->format('M d, Y') }}</span>
              </div>
          </div>
      </a>
  </x-card>
  ```
- [ ] Takes recipe prop (Recipe model)
- [ ] Shows recipe name as heading
- [ ] Shows classification badge
- [ ] Shows truncated ingredients
- [ ] Shows source and date added
- [ ] Links to recipe detail page
- [ ] Hover effects on card and title
- [ ] Uses line-clamp for truncation
- [ ] Responsive design

**Files to Create/Modify**:
- `resources/views/components/recipe-card.blade.php` (create)

**Testing**:
Create test view:
```blade
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    @foreach($recipes as $recipe)
        <x-recipe-card :recipe="$recipe" />
    @endforeach
</div>
```

Add test route:
```php
Route::get('/test/recipe-cards', function () {
    $recipes = Recipe::with(['classification', 'source'])->limit(6)->get();
    return view('test.recipe-cards', compact('recipes'));
});
```

Manual testing:
1. Verify recipe cards display correctly
2. Verify hover effects work
3. Verify links navigate to recipe detail
4. Verify responsive grid layout
5. Verify truncation works for long content

**Story**:
```
As a user
I want to see recipe summaries in an attractive card layout
So that I can browse recipes easily
```

---

### M6-7 (#326): Create Pagination Component
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M6-1 (Base layout)
**Blocks**: M7-1 (Recipe index uses pagination)

**Description**:
Create Tailwind-styled pagination component for Laravel paginator.

**Acceptance Criteria**:
- [ ] Created `resources/views/vendor/pagination/tailwind.blade.php`:
  ```blade
  @if ($paginator->hasPages())
      <nav role="navigation" aria-label="Pagination Navigation" class="flex items-center justify-between">
          <div class="flex justify-between flex-1 sm:hidden">
              @if ($paginator->onFirstPage())
                  <span class="relative inline-flex items-center px-4 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 cursor-default rounded-md">
                      Previous
                  </span>
              @else
                  <a href="{{ $paginator->previousPageUrl() }}" class="relative inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50">
                      Previous
                  </a>
              @endif

              @if ($paginator->hasMorePages())
                  <a href="{{ $paginator->nextPageUrl() }}" class="relative inline-flex items-center px-4 py-2 ml-3 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50">
                      Next
                  </a>
              @else
                  <span class="relative inline-flex items-center px-4 py-2 ml-3 text-sm font-medium text-gray-500 bg-white border border-gray-300 cursor-default rounded-md">
                      Next
                  </span>
              @endif
          </div>

          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                  <p class="text-sm text-gray-700">
                      Showing
                      <span class="font-medium">{{ $paginator->firstItem() }}</span>
                      to
                      <span class="font-medium">{{ $paginator->lastItem() }}</span>
                      of
                      <span class="font-medium">{{ $paginator->total() }}</span>
                      results
                  </p>
              </div>

              <div>
                  <span class="relative z-0 inline-flex shadow-sm rounded-md">
                      {{-- Previous Page Link --}}
                      @if ($paginator->onFirstPage())
                          <span aria-disabled="true" aria-label="Previous">
                              <span class="relative inline-flex items-center px-2 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 cursor-default rounded-l-md" aria-hidden="true">
                                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                      <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                                  </svg>
                              </span>
                          </span>
                      @else
                          <a href="{{ $paginator->previousPageUrl() }}" rel="prev" class="relative inline-flex items-center px-2 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-l-md hover:bg-gray-50" aria-label="Previous">
                              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                  <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                              </svg>
                          </a>
                      @endif

                      {{-- Pagination Elements --}}
                      @foreach ($elements as $element)
                          {{-- "Three Dots" Separator --}}
                          @if (is_string($element))
                              <span aria-disabled="true">
                                  <span class="relative inline-flex items-center px-4 py-2 -ml-px text-sm font-medium text-gray-700 bg-white border border-gray-300 cursor-default">{{ $element }}</span>
                              </span>
                          @endif

                          {{-- Array Of Links --}}
                          @if (is_array($element))
                              @foreach ($element as $page => $url)
                                  @if ($page == $paginator->currentPage())
                                      <span aria-current="page">
                                          <span class="relative inline-flex items-center px-4 py-2 -ml-px text-sm font-medium text-white bg-blue-600 border border-blue-600 cursor-default">{{ $page }}</span>
                                      </span>
                                  @else
                                      <a href="{{ $url }}" class="relative inline-flex items-center px-4 py-2 -ml-px text-sm font-medium text-gray-700 bg-white border border-gray-300 hover:bg-gray-50" aria-label="Go to page {{ $page }}">
                                          {{ $page }}
                                      </a>
                                  @endif
                              @endforeach
                          @endif
                      @endforeach

                      {{-- Next Page Link --}}
                      @if ($paginator->hasMorePages())
                          <a href="{{ $paginator->nextPageUrl() }}" rel="next" class="relative inline-flex items-center px-2 py-2 -ml-px text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-r-md hover:bg-gray-50" aria-label="Next">
                              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                              </svg>
                          </a>
                      @else
                          <span aria-disabled="true" aria-label="Next">
                              <span class="relative inline-flex items-center px-2 py-2 -ml-px text-sm font-medium text-gray-500 bg-white border border-gray-300 cursor-default rounded-r-md" aria-hidden="true">
                                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                      <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                                  </svg>
                              </span>
                          </span>
                      @endif
                  </span>
              </div>
          </div>
      </nav>
  @endif
  ```
- [ ] Publish pagination views: `php artisan vendor:publish --tag=laravel-pagination`
- [ ] Mobile-friendly (simple prev/next on small screens)
- [ ] Desktop pagination with page numbers
- [ ] Shows result count (e.g., "Showing 1 to 25 of 100 results")
- [ ] Current page highlighted
- [ ] Disabled state for first/last pages
- [ ] Accessible ARIA labels
- [ ] Tailwind styling throughout

**Files to Create/Modify**:
- `resources/views/vendor/pagination/tailwind.blade.php` (create via publish command, then modify)

**Testing**:
```bash
# Publish pagination views
php artisan vendor:publish --tag=laravel-pagination
```

Create test view:
```blade
<!-- Test with paginated results -->
{{ $recipes->links() }}
```

Manual testing:
1. Verify pagination displays on pages with >25 items
2. Verify mobile layout shows simple prev/next
3. Verify desktop layout shows page numbers
4. Verify current page is highlighted
5. Verify disabled states work
6. Verify clicking pages navigates correctly

**Story**:
```
As a user
I want paginated results with easy navigation
So that I can browse through large recipe collections
```

---

### M6-8 (#307): Create Sort Controls Component
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M6-4 (Select component)
**Blocks**: M7-1 (Recipe index uses sort controls)

**Description**:
Create component for sort field and direction controls with auto-submit functionality.

**Acceptance Criteria**:
- [ ] Created `resources/views/components/sort-controls.blade.php`:
  ```blade
  @props([
      'sortField' => 'name',
      'sortOrder' => 'asc',
  ])

  <div class="flex flex-col sm:flex-row gap-4">
      <div class="flex-1">
          <label for="sortField" class="block text-sm font-medium text-gray-700 mb-1">
              Sort By
          </label>
          <select
              name="sortField"
              id="sortField"
              onchange="this.form.submit()"
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          >
              <option value="name" {{ $sortField === 'name' ? 'selected' : '' }}>
                  Name
              </option>
              <option value="date_added" {{ $sortField === 'date_added' ? 'selected' : '' }}>
                  Date Added
              </option>
          </select>
      </div>

      <div class="flex-1">
          <label for="sortOrder" class="block text-sm font-medium text-gray-700 mb-1">
              Order
          </label>
          <select
              name="sortOrder"
              id="sortOrder"
              onchange="this.form.submit()"
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          >
              <option value="asc" {{ $sortOrder === 'asc' ? 'selected' : '' }}>
                  Ascending
              </option>
              <option value="desc" {{ $sortOrder === 'desc' ? 'selected' : '' }}>
                  Descending
              </option>
          </select>
      </div>
  </div>
  ```
- [ ] Takes sortField and sortOrder props
- [ ] Auto-submits form on change
- [ ] Responsive layout (stacked on mobile, side-by-side on desktop)
- [ ] Pre-selects current values
- [ ] Accessible labels

**Files to Create/Modify**:
- `resources/views/components/sort-controls.blade.php` (create)

**Testing**:
Create test view:
```blade
<form method="GET" action="{{ route('recipes.index') }}">
    <x-sort-controls
        :sortField="request('sortField', 'name')"
        :sortOrder="request('sortOrder', 'asc')"
    />
</form>
```

Manual testing:
1. Verify dropdowns render with correct selected values
2. Verify changing sort field auto-submits form
3. Verify changing sort order auto-submits form
4. Verify responsive layout works
5. Verify form maintains other query parameters

**Story**:
```
As a user
I want to easily change how recipes are sorted
So that I can find recipes in my preferred order
```

---

### M6-9 (#328): Create Navigation Component
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:medium` (1 hour)
**Depends On**: M6-1 (Base layout includes navigation)
**Blocks**: M9-1 (Mobile menu interactivity)

**Description**:
Create site navigation header with logo, menu items, and mobile menu structure (interactivity added later in M9-1).

**Acceptance Criteria**:
- [ ] Created `resources/views/components/navigation.blade.php`:
  ```blade
  <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16">
              <div class="flex">
                  <!-- Logo -->
                  <div class="flex-shrink-0 flex items-center">
                      <a href="{{ route('home') }}" class="text-xl font-bold text-blue-600">
                          {{ config('app.name') }}
                      </a>
                  </div>

                  <!-- Desktop Navigation -->
                  <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
                      <a href="{{ route('recipes.index') }}"
                         class="inline-flex items-center px-1 pt-1 border-b-2 {{ request()->routeIs('recipes.*') ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700' }} text-sm font-medium">
                          Recipes
                      </a>

                      <a href="{{ route('cookbooks.index') }}"
                         class="inline-flex items-center px-1 pt-1 border-b-2 {{ request()->routeIs('cookbooks.*') ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700' }} text-sm font-medium">
                          Cookbooks
                      </a>
                  </div>
              </div>

              <!-- Mobile menu button -->
              <div class="flex items-center sm:hidden">
                  <button type="button"
                          x-data="{ open: false }"
                          @click="open = !open"
                          class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
                          aria-expanded="false">
                      <span class="sr-only">Open main menu</span>
                      <!-- Icon when menu is closed -->
                      <svg class="block h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                      </svg>
                  </button>
              </div>
          </div>
      </div>

      <!-- Mobile menu (hidden by default, will be shown/hidden with Alpine.js in M9-1) -->
      <div class="sm:hidden hidden" id="mobile-menu">
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
- [ ] Responsive design (desktop and mobile layouts)
- [ ] Logo links to homepage
- [ ] Active state for current page
- [ ] Hover states for menu items
- [ ] Mobile menu button (functionality in M9-1)
- [ ] Mobile menu structure (hidden by default)
- [ ] Accessible markup (ARIA labels, semantic HTML)
- [ ] Uses Alpine.js x-data for menu state (interactive in M9-1)

**Files to Create/Modify**:
- `resources/views/components/navigation.blade.php` (create)

**Testing**:
Manual testing:
1. Verify navigation renders in layout
2. Verify logo links to homepage
3. Verify menu items link correctly
4. Verify active states show on correct pages
5. Verify responsive breakpoints work
6. Verify mobile menu structure exists (not interactive yet)

**Story**:
```
As a user
I want clear navigation across all pages
So that I can easily access different sections of the site
```

---

### M6-10 (#331): Document Component Library
**Type**: `type:docs`
**Priority**: `P3`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M6-2 through M6-9 (All components created)
**Blocks**: None

**Description**:
Create comprehensive documentation for the component library with usage examples.

**Acceptance Criteria**:
- [ ] Created `docs/COMPONENTS.md` with:
  - [ ] Overview of component library philosophy
  - [ ] List of all available components
  - [ ] Usage examples for each component:
    - [ ] Button (all variants)
    - [ ] Input (with/without errors)
    - [ ] Select (with options)
    - [ ] Card (with header/footer)
    - [ ] Recipe Card
    - [ ] Pagination
    - [ ] Sort Controls
    - [ ] Navigation
  - [ ] Props documentation for each component
  - [ ] Customization guidelines (adding classes, extending)
  - [ ] Accessibility notes
  - [ ] Best practices

**Files to Create/Modify**:
- `docs/COMPONENTS.md` (create)

**Example Content Structure**:
```markdown
# Component Library

## Button Component

### Usage
```blade
<x-button variant="primary">Click Me</x-button>
```

### Props
- `type`: button|submit|reset (default: button)
- `variant`: primary|secondary|danger (default: primary)

### Examples
[Multiple examples...]

## Input Component
[Similar structure...]
```

**Testing**:
Review documentation for:
1. Accuracy of examples
2. Completeness of props
3. Clarity of explanations
4. Working code samples

**Story**:
```
As a developer
I want comprehensive component documentation
So that I can use components correctly and consistently
```

---

## Summary

**Total Issues**: 10
**Can Run in Parallel**: After M6-1 completes, 4-5 agents can work on M6-2 through M6-9 in parallel
**Critical Path**: M6-1 → M6-5 → M6-6 → M7-1
**Estimated Milestone Completion**: 8-10 hours with 4-5 agents, 16-20 hours solo

**Parallel Execution Strategy**:
- **Wave 1** (Sequential):
  - **Agent 1**: M6-1 (Base layout)
- **Wave 2** (Parallel after M6-1):
  - **Agent 1**: M6-2 (Button)
  - **Agent 2**: M6-3 (Input)
  - **Agent 3**: M6-4 (Select) → M6-8 (Sort controls)
  - **Agent 4**: M6-5 (Card) → M6-6 (Recipe card)
  - **Agent 5**: M6-7 (Pagination)
- **Wave 3** (Parallel after Wave 2):
  - **Agent 1**: M6-9 (Navigation)
  - **Agent 2**: M6-10 (Documentation)

**Dependency Chain**:
```
M2-5 → M6-1 → M6-2, M6-3, M6-4, M6-5, M6-7, M6-9
              ↓                    ↓
              M6-8                 M6-6 → M7-1

M6-2 through M6-9 → M6-10 (Documentation)
```

**Success Criteria**:
Complete component library created with reusable Blade components. All components properly styled with Tailwind CSS. Base layout established. Navigation functional. Component documentation complete.
