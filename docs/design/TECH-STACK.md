# Tech Stack and Design Requirements

## Version Requirements

The project enforces the following version constraints to ensure modern best practices and compatibility:

- **PHP 8.5+** (latest stable)
- **Laravel 12.x**
- **Node.js 25+**
- **Tailwind CSS 4+**
- **Alpine.js 3.x**

## Backend Stack

### Framework & Core
- **Laravel 12.x**: Modern PHP framework with built-in features for routing, ORM, migrations, testing
- **PHP 8.5+**: Latest stable PHP with type safety, attributes, named arguments, match expressions

### Database & ORM
- **Eloquent ORM**: Laravel's query builder and ORM for database interactions
- **Database Migrations**: Version-controlled schema changes in `database/migrations/`
- **Database Seeders**: Population of test/demo data via `database/seeders/`

### Search & Query
- **Laravel Scout**: Search abstraction layer (supports Meilisearch, Algolia, or database driver)
- **Eloquent Query Scopes**: Native query methods for filtering and searching
- Example: `Recipe::search('pasta')->get()` or `Recipe::whereSearchable('pasta')->get()`

### External Services
- **Guzzle HTTP Client**: HTTP client for external API calls
- **Stripe/Payment Processing**: Optional payment integration for future features

## Frontend Stack

### CSS Framework
- **Tailwind CSS 4+**: Latest utility-first CSS framework with improved performance and modern features
- No Bootstrap dependency (lightweight, modern alternative)
- PostCSS with Tailwind plugin for CSS processing

### JavaScript Framework
- **Alpine.js 3.x**: Lightweight, Blade-friendly reactive framework
- Direct integration with Blade templates via `x-*` attributes
- No Node.js build step required for basic functionality

### Build Tool
- **Vite**: Modern, fast build tool (10x faster than Webpack)
- Modern Laravel asset pipeline with Hot Module Replacement (HMR) in development
- Asset compilation: `npm run dev` (development) or `npm run build` (production)
- Compiled assets output to `public/build/`

### UI Components
- **Blade Components**: Reusable, component-based architecture
- Tailwind CSS utility classes for styling
- Alpine.js for interactivity

## Development & Testing

### Testing Frameworks
- **PHPUnit 10+** or **Pest 2.0+**: Modern PHP testing frameworks
- Unit tests in `tests/Unit/`
- Feature tests in `tests/Feature/`
- Test configuration in `phpunit.xml` and `pest.xml`
- Test environment: `APP_ENV=testing`, uses array/sync drivers (no persistence)

### Development Tools
- **Laravel Artisan**: CLI for database, model, migration, and controller generation
- **Laravel Tinker**: Interactive REPL shell for testing code and queries
- **Laravel Valet/Artisan Serve**: Local development server

### Code Quality
- **Error Handling**: Custom exception handlers in `app/Exceptions/`
- **Logging**: Error logs in `storage/logs/`
- **Debugging**: Debug mode (`APP_DEBUG=true`), `dd()`, `dump()` utilities

## Architecture Patterns

### Models & Relationships
- **Eloquent Models**: In `app/Models/` with modern relationship conventions
- **Timestamps**: All models include `public $timestamps = true;` by default
- **Fillable Attributes**: Define `protected $fillable = [];` for mass assignment
- **Relationships**:
  - `belongsTo()`: One-to-one or one-to-many inverse
  - `hasOne()`: One-to-one
  - `belongsToMany()`: Many-to-many with pivot tables
  - Access via properties: `$recipe->source` (not `$recipe->getSource()`)

### Database
- **Pivot Tables**: Explicit tables for many-to-many relationships (`recipe_meals`, `recipe_courses`, etc.)
- **Foreign Keys**: Defined via `$table->foreign()` in migrations
- **Migration Order**: Executed by timestamp; foreign keys in separate or combined migrations

### Controllers & Routing
- **Route Groups**: Modern routing with resource controllers in `routes/web.php` and `routes/api.php`
- **Resource Controllers**: `Route::resource('recipes', RecipeController::class)` for CRUD
- **Query Parameters**: Support `sortField`, `sortOrder`, `displayCount` for filtering and pagination
- **Form Requests**: Validation in `app/Http/Requests/` classes (PSR-4 namespace)

### Views & Templates
- **Blade Templates**: In `resources/views/` with directory structure per resource
- **Subdirectories**: `recipe/`, `cookbook/`, `contact/`, `emails/`
- **Components**: Reusable UI elements in `resources/views/components/`
- **Partials**: Shared template sections in `resources/views/partials/`
- **Main Layout**: `resources/layouts/app.blade.php`

## Configuration & Environment

### Configuration Files
- Core config in `config/` directory
- Primary files: `app.php`, `database.php`, `mail.php`, `queue.php`, `cache.php`
- Service providers configured in `config/app.php`

### Environment Variables
- `.env` file for local configuration
- `.env.example` as template for new installations
- Debug mode: `APP_DEBUG=true` in development
- Database connection via `DB_*` variables

## Project-Specific Conventions

1. **Sorting/Filtering**: Preserve query parameter pattern (`sortField`, `sortOrder`, `displayCount`) when adding features
2. **Pivot Table Ordering**: Cookbook recipes ordered by classification name then recipe name
3. **Default Route**: `/` redirects to recipe index with default sorting: `sortField=date_added`, `sortOrder=desc`, `displayCount=30`
4. **API Responses**: Use JSON with proper status codes and consistent error handling
5. **Timestamps**: All models include timestamps by default

