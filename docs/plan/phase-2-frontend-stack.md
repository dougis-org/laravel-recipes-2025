# Milestone 2 - Frontend Stack

**Goal**: Set up modern frontend build pipeline with Tailwind CSS 4+ and Alpine.js 3

**Estimated Total Effort**: 3-4 hours
**Can Start**: After M1-1 complete
**Parallel Capacity**: 2-3 agents (some parallelization possible)

---

## Issues

### M2-1: Install and Configure Vite
**Type**: `type:setup`
**Priority**: `P1`
**Effort**: `effort:small` (30 min)
**Depends On**: M1-1 (Laravel project), M0-2 (Node.js)
**Blocks**: M2-2 (Tailwind), M2-4 (Alpine.js)

**Description**:
Verify Vite configuration is properly set up for Laravel 12 (comes by default).

**Acceptance Criteria**:
- [ ] Verified `vite.config.js` exists with Laravel plugin
- [ ] Verified configuration includes:
  ```javascript
  export default defineConfig({
      plugins: [
          laravel({
              input: ['resources/css/app.css', 'resources/js/app.js'],
              refresh: true,
          }),
      ],
  });
  ```
- [ ] Package.json scripts configured:
  - [ ] `"dev": "vite"`
  - [ ] `"build": "vite build"`
- [ ] Test Vite dev server starts: `npm run dev`
- [ ] Stop dev server after test

**Files to Modify**:
- `vite.config.js` (verify/update)
- `package.json` (verify)

**Testing**:
```bash
npm run dev    # Should start Vite dev server
# Access http://localhost:5173 in browser
# Stop server with Ctrl+C
```

**Story**:
```
As a developer
I want Vite properly configured
So that I can use hot module replacement during development
```

---

### M2-2: Install and Configure Tailwind CSS 4
**Type**: `type:setup`, `type:feature`
**Priority**: `P1`
**Effort**: `effort:medium` (1-2 hours)
**Depends On**: M2-1 (Vite configured)
**Blocks**: M6-1 (Layout components), M7-1 (Recipe views)

**Description**:
Install Tailwind CSS 4+ and configure for use with Laravel and Vite.

**Acceptance Criteria**:
- [ ] Install Tailwind CSS: `npm install -D tailwindcss@latest postcss autoprefixer`
- [ ] Initialize Tailwind config: `npx tailwindcss init -p`
- [ ] Configure `tailwind.config.js`:
  ```javascript
  export default {
    content: [
      "./resources/**/*.blade.php",
      "./resources/**/*.js",
      "./resources/**/*.vue",
    ],
    theme: {
      extend: {},
    },
    plugins: [],
  }
  ```
- [ ] Configure `postcss.config.js`:
  ```javascript
  export default {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  }
  ```
- [ ] Update `resources/css/app.css`:
  ```css
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
  ```
- [ ] Verify Tailwind version is 4.0+: `npm list tailwindcss`

**Files to Create/Modify**:
- `tailwind.config.js` (create)
- `postcss.config.js` (create)
- `resources/css/app.css` (update)
- `package.json` (dependencies updated)
- `package-lock.json` (dependencies updated)

**Testing**:
Create test file `resources/views/test.blade.php`:
```blade
<!DOCTYPE html>
<html>
<head>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body>
    <div class="bg-blue-500 text-white p-4">
        Tailwind CSS is working!
    </div>
</body>
</html>
```
Run `npm run dev` and verify blue background appears.

**Story**:
```
As a developer
I want Tailwind CSS 4+ installed and configured
So that I can use utility-first CSS classes for styling
```

---

### M2-3: Configure Package Scripts and Test Build
**Type**: `type:setup`
**Priority**: `P1`
**Effort**: `effort:small` (30 min)
**Depends On**: M2-2 (Tailwind installed)
**Blocks**: M10-1 (Production build optimization)

**Description**:
Verify package.json scripts and test both development and production builds.

**Acceptance Criteria**:
- [ ] Verified `package.json` scripts:
  - [ ] `"dev": "vite"`
  - [ ] `"build": "vite build"`
- [ ] Test development build:
  - [ ] `npm run dev` starts successfully
  - [ ] Vite dev server accessible at http://localhost:5173
  - [ ] Hot module replacement works (edit CSS, see live update)
- [ ] Test production build:
  - [ ] `npm run build` completes successfully
  - [ ] Assets compiled to `public/build/`
  - [ ] Manifest file created: `public/build/manifest.json`
  - [ ] CSS and JS files are minified
- [ ] Clean up test file from M2-2

**Files to Modify**:
- `package.json` (verify)
- Delete: `resources/views/test.blade.php`

**Testing**:
```bash
npm run dev      # Should start dev server
npm run build    # Should create public/build/ directory
ls -la public/build/  # Should show manifest.json and asset files
```

**Story**:
```
As a developer
I want to verify both development and production builds work
So that I can develop with HMR and deploy optimized assets
```

---

### M2-4: Install and Configure Alpine.js 3
**Type**: `type:setup`, `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M2-1 (Vite configured)
**Blocks**: M9-1 (Mobile menu interactivity)

**Description**:
Install Alpine.js 3.14+ for lightweight JavaScript interactivity.

**Acceptance Criteria**:
- [ ] Install Alpine.js: `npm install alpinejs@latest`
- [ ] Verify version is 3.14+: `npm list alpinejs`
- [ ] Update `resources/js/app.js`:
  ```javascript
  import Alpine from 'alpinejs'
  window.Alpine = Alpine
  Alpine.start()
  ```
- [ ] Create test to verify Alpine.js works
- [ ] Document Alpine.js usage in `docs/FRONTEND.md`

**Files to Create/Modify**:
- `resources/js/app.js` (update)
- `package.json` (dependencies updated)
- `package-lock.json` (dependencies updated)
- `docs/FRONTEND.md` (create)

**Testing**:
Create test in welcome blade or test route:
```blade
<div x-data="{ open: false }">
    <button @click="open = !open">Toggle</button>
    <div x-show="open">Content</div>
</div>
```
Verify clicking toggle shows/hides content.

**Story**:
```
As a developer
I want Alpine.js 3.14+ installed
So that I can add reactive components without a heavy framework
```

---

### M2-5: Update Base Layout with Vite Directives
**Type**: `type:feature`
**Priority**: `P2`
**Effort**: `effort:small` (30 min)
**Depends On**: M2-1 (Vite), M2-2 (Tailwind), M2-4 (Alpine.js)
**Blocks**: M6-1 (Layout components)

**Description**:
Create or update base Blade layout to include Vite asset directives.

**Acceptance Criteria**:
- [ ] Verified/updated `resources/views/layouts/app.blade.php` exists
- [ ] Includes Vite directive in `<head>`:
  ```blade
  @vite(['resources/css/app.css', 'resources/js/app.js'])
  ```
- [ ] Includes basic HTML5 structure:
  - [ ] DOCTYPE, html, head, body tags
  - [ ] Meta charset and viewport
  - [ ] Title tag with app name
- [ ] Includes content section: `@yield('content')` or `{{ $slot }}`
- [ ] Test layout renders correctly

**Files to Create/Modify**:
- `resources/views/layouts/app.blade.php` (create/update)

**Testing**:
Create test route and view to verify layout works:
```php
// routes/web.php
Route::get('/test-layout', function () {
    return view('test-layout');
});

// resources/views/test-layout.blade.php
@extends('layouts.app')
@section('content')
    <div class="container mx-auto p-4">
        <h1 class="text-3xl font-bold text-blue-600">Layout Test</h1>
    </div>
@endsection
```
Access route and verify Tailwind styles apply.

**Story**:
```
As a developer
I want a base layout with Vite directives
So that all pages can include compiled CSS and JS assets
```

---

### M2-6: Create Frontend Documentation
**Type**: `type:docs`
**Priority**: `P3`
**Effort**: `effort:small` (30 min)
**Depends On**: M2-2 (Tailwind), M2-4 (Alpine.js)
**Blocks**: None

**Description**:
Document frontend stack setup and usage guidelines.

**Acceptance Criteria**:
- [ ] Updated/created `docs/FRONTEND.md` with:
  - [ ] Technology stack overview (Vite, Tailwind, Alpine.js)
  - [ ] Version numbers
  - [ ] How to run dev server
  - [ ] How to build for production
  - [ ] Tailwind CSS usage guidelines
  - [ ] Alpine.js usage patterns
  - [ ] Common CSS utility classes
  - [ ] Component development guidelines
- [ ] Include example code snippets
- [ ] Include troubleshooting section

**Files to Create/Modify**:
- `docs/FRONTEND.md` (update/create)

**Testing**: Review documentation for accuracy

**Story**:
```
As a developer
I want comprehensive frontend documentation
So that I understand how to use the frontend stack effectively
```

---

## Summary

**Total Issues**: 6
**Can Run in Parallel**: M2-3 and M2-4 can run after M2-1; M2-6 can run after M2-2 and M2-4
**Critical Path**: M2-1 → M2-2 → M2-5 → M6-1
**Estimated Milestone Completion**: 3-4 hours with 2-3 agents, 6-8 hours solo

**Parallel Execution Strategy**:
- **Agent 1**: M2-1 (Vite) → M2-2 (Tailwind) → M2-5 (Layout)
- **Agent 2**: Wait for M2-1, then M2-4 (Alpine.js)
- **Agent 3**: Wait for M2-2, then M2-3 (Test builds)
- **Agent 4**: Wait for M2-2 and M2-4, then M2-6 (Documentation)

**Dependency Chain**:
```
M2-1 → M2-2 → M2-5 → M6-1
     ↓       ↓
     M2-4   M2-3 → M10-1
       ↓
      M9-1
```

**Success Criteria**:
Frontend stack configured with Vite, Tailwind CSS 4+, and Alpine.js 3.14+. Development and production builds working. Base layout created with asset directives.
