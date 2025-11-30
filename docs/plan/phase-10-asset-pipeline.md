# Milestone 10 - Asset Pipeline

**Goal**: Optimize production build process with minification, versioning, and performance enhancements

**Estimated Total Effort**: 3-4 hours
**Can Start**: After M2-3 complete (Vite configured and tested)
**Parallel Capacity**: 2-3 agents (some parallelization possible)

---

## Issues

### M10-1 (#339): Optimize Production Build Configuration
**Type**: `type:optimization`
**Priority**: `P1`
**Effort**: `effort:medium` (1-2 hours)
**Depends On**: M2-3 (Vite configured)
**Blocks**: M10-2 (Testing build), M16-5 (Deployment)

**Description**:
Configure Vite for optimized production builds with minification, tree-shaking, and code splitting.

**Acceptance Criteria**:
- [ ] Updated `vite.config.js` with production optimizations:
  ```javascript
  import { defineConfig } from 'vite';
  import laravel from 'laravel-vite-plugin';

  export default defineConfig({
      plugins: [
          laravel({
              input: ['resources/css/app.css', 'resources/js/app.js'],
              refresh: true,
          }),
      ],
      build: {
          // Manifest for cache busting
          manifest: true,

          // Output directory
          outDir: 'public/build',

          // Minification
          minify: 'terser',
          terserOptions: {
              compress: {
                  drop_console: true, // Remove console.logs in production
                  drop_debugger: true,
              },
          },

          // Source maps for debugging (optional)
          sourcemap: false,

          // Chunk size warnings
          chunkSizeWarningLimit: 500,

          // Rollup options for code splitting
          rollupOptions: {
              output: {
                  manualChunks: {
                      // Vendor chunk for third-party libraries
                      vendor: ['alpinejs'],
                  },
              },
          },
      },

      // CSS optimization
      css: {
          devSourcemap: true,
      },
  });
  ```
- [ ] Configured Tailwind CSS for production:
  ```javascript
  // tailwind.config.js
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
      // Production optimizations
      future: {
          hoverOnlyWhenSupported: true,
      },
      experimental: {
          optimizeUniversalDefaults: true,
      },
  }
  ```
- [ ] Configured PostCSS for optimization:
  ```javascript
  // postcss.config.js
  export default {
      plugins: {
          tailwindcss: {},
          autoprefixer: {},
          ...(process.env.NODE_ENV === 'production' ? { cssnano: {} } : {}),
      },
  }
  ```
- [ ] Install cssnano for CSS minification: `npm install -D cssnano`
- [ ] Updated `.gitignore` to include build artifacts:
  ```
  /public/build/*
  /public/hot
  ```

**Files to Create/Modify**:
- `vite.config.js` (modify)
- `tailwind.config.js` (modify)
- `postcss.config.js` (modify)
- `package.json` (add cssnano)
- `.gitignore` (update)

**Testing**:
```bash
# Test production build
npm run build

# Verify output
ls -lh public/build/
# Should show minified .js and .css files

# Check file sizes
du -sh public/build/*

# Verify manifest exists
cat public/build/manifest.json
```

**Story**:
```
As a developer
I want optimized production builds
So that the application loads quickly for users
```

---

### M10-2 (#340): Test Production Build
**Type**: `type:testing`
**Priority**: `P1`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M10-1 (Build configuration)
**Blocks**: None

**Description**:
Test production build process and verify asset optimization.

**Acceptance Criteria**:
- [ ] Run production build: `npm run build`
- [ ] Build completes without errors
- [ ] Verify generated files:
  - [ ] `public/build/manifest.json` exists
  - [ ] CSS files minified (no whitespace, comments removed)
  - [ ] JS files minified (no whitespace, console.logs removed)
  - [ ] Vendor chunk created (if Alpine.js split)
- [ ] Verify file sizes reasonable:
  - [ ] CSS < 50KB (compressed)
  - [ ] JS < 100KB (compressed)
  - [ ] Total assets < 200KB
- [ ] Test build in production-like environment:
  ```bash
  # Set environment to production
  APP_ENV=production php artisan serve

  # Visit application
  # Verify assets load correctly
  # Check browser console for errors
  ```
- [ ] Verify no source maps in production (unless configured)
- [ ] Verify console.logs removed from production JS
- [ ] Test with browser caching:
  - [ ] Hard refresh (Ctrl+Shift+R)
  - [ ] Verify assets cached properly
  - [ ] Change CSS, rebuild, verify cache busted

**Files to Create/Modify**:
- None (testing only)
- Document findings in `docs/performance/build-metrics.md`

**Testing Commands**:
```bash
# Clean build
rm -rf public/build/*

# Production build
npm run build

# Check sizes
du -h public/build/*

# Test with production server
APP_ENV=production php artisan serve

# Access in browser
curl -I http://localhost:8000
# Check for proper headers
```

**Story**:
```
As a developer
I want to verify production builds work correctly
So that deployments are reliable
```

---

### M10-3 (#341): Configure Asset Versioning and Cache Busting
**Type**: `type:feature`
**Priority**: `P1`
**Effort**: `effort:small` (30 min)
**Depends On**: M10-1 (Build configuration)
**Blocks**: None

**Description**:
Verify and test asset versioning/cache busting through Vite's manifest.json.

**Acceptance Criteria**:
- [ ] Verified `manifest.json` created by build process
- [ ] Manifest contains hashed filenames:
  ```json
  {
    "resources/css/app.css": {
      "file": "assets/app-[hash].css",
      "src": "resources/css/app.css",
      "isEntry": true
    },
    "resources/js/app.js": {
      "file": "assets/app-[hash].js",
      "src": "resources/js/app.js",
      "isEntry": true
    }
  }
  ```
- [ ] Laravel's `@vite` directive uses manifest in production:
  ```blade
  {{-- This automatically reads manifest.json in production --}}
  @vite(['resources/css/app.css', 'resources/js/app.js'])
  ```
- [ ] Test cache busting:
  - [ ] Build assets: `npm run build`
  - [ ] Note filename hashes
  - [ ] Modify CSS file
  - [ ] Rebuild: `npm run build`
  - [ ] Verify new hashes generated
  - [ ] Old files removed from build directory
- [ ] Configure web server headers for caching (documentation):
  ```nginx
  # Nginx example for cache control
  location ~* \.(css|js)$ {
      expires 1y;
      add_header Cache-Control "public, immutable";
  }
  ```
- [ ] Document cache strategy in `docs/DEPLOYMENT.md`

**Files to Create/Modify**:
- `docs/DEPLOYMENT.md` (add cache configuration section)
- `docs/performance/cache-strategy.md` (create)

**Testing**:
```bash
# Build and check manifest
npm run build
cat public/build/manifest.json

# Modify CSS
echo "/* cache bust test */" >> resources/css/app.css

# Rebuild
npm run build

# Verify new hash in manifest
cat public/build/manifest.json

# Check old files removed
ls -la public/build/assets/
```

**Story**:
```
As a developer
I want automatic cache busting
So that users always get the latest assets after deployment
```

---

### M10-4 (#342): Document Build Process and Performance Metrics
**Type**: `type:docs`
**Priority**: `P2`
**Effort**: `effort:small` (30-60 min)
**Depends On**: M10-1, M10-2, M10-3 (All build features complete)
**Blocks**: None

**Description**:
Create comprehensive documentation of the build process, optimization strategies, and performance metrics.

**Acceptance Criteria**:
- [ ] Created/updated `docs/FRONTEND.md` with build process section:
  - [ ] Development workflow (`npm run dev`)
  - [ ] Production build (`npm run build`)
  - [ ] Asset optimization strategies
  - [ ] Troubleshooting common build issues
- [ ] Created `docs/performance/build-metrics.md`:
  - [ ] Asset size benchmarks:
    ```markdown
    ## Asset Sizes (Production Build)

    | Asset | Size (Uncompressed) | Size (Gzipped) |
    |-------|---------------------|----------------|
    | app.css | ~45KB | ~8KB |
    | app.js | ~85KB | ~25KB |
    | vendor.js | ~50KB | ~15KB |
    | **Total** | **~180KB** | **~48KB** |

    Target: < 200KB total uncompressed
    ```
  - [ ] Build time benchmarks
  - [ ] Optimization techniques applied
  - [ ] Future optimization opportunities
- [ ] Created `docs/performance/cache-strategy.md`:
  - [ ] Cache headers configuration
  - [ ] Cache busting strategy
  - [ ] CDN considerations (future)
  - [ ] Browser caching best practices
- [ ] Added npm scripts documentation:
  ```markdown
  ## NPM Scripts

  - `npm run dev` - Start Vite dev server with HMR
  - `npm run build` - Build optimized production assets
  - `npm run preview` - Preview production build locally (if configured)
  ```
- [ ] Include example `.env` configuration for different environments

**Files to Create/Modify**:
- `docs/FRONTEND.md` (update)
- `docs/performance/build-metrics.md` (create)
- `docs/performance/cache-strategy.md` (create)
- `README.md` (add link to build documentation)

**Testing**:
Review documentation for:
1. Accuracy of commands
2. Completeness of process
3. Clarity of instructions
4. Actual benchmark numbers match reality

**Story**:
```
As a developer
I want comprehensive build documentation
So that I can understand and maintain the build process
```

---

## Summary

**Total Issues**: 4
**Can Run in Parallel**: M10-2 and M10-3 can run after M10-1, M10-4 after all complete
**Critical Path**: M10-1 → M10-2 → M16-5
**Estimated Milestone Completion**: 3-4 hours with 2-3 agents, 6-8 hours solo

**Parallel Execution Strategy**:
- **Wave 1** (Sequential):
  - **Agent 1**: M10-1 (Build configuration)
- **Wave 2** (Parallel after M10-1):
  - **Agent 1**: M10-2 (Test build)
  - **Agent 2**: M10-3 (Cache busting)
- **Wave 3** (After Wave 2):
  - **Agent 1**: M10-4 (Documentation)

**Dependency Chain**:
```
M2-3 → M10-1 → M10-2, M10-3 → M10-4
              ↓
             M16-5 (Deployment)
```

**Success Criteria**:
Production build process optimized with minification and tree-shaking. Asset sizes within targets (<200KB total). Cache busting working correctly. Build completes without errors. Comprehensive documentation in place. Performance metrics documented.
