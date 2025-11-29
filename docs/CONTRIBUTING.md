# Contributing to Laravel Recipe Manager

Welcome! This guide provides information for developers working on the Laravel Recipe Manager project.

## Getting Started

### Prerequisites
- PHP 8.5+
- Laravel 12.x
- Node.js 25+
- Composer
- Git

### Initial Setup

```bash
# Clone the repository
git clone <repository-url>
cd laravel-recipes-2025

# Install dependencies
composer install
npm install

# Copy environment file
cp .env.example .env

# Generate app key
php artisan key:generate

# Run migrations
php artisan migrate

# Seed database
php artisan db:seed

# Build frontend assets
npm run build

# Start development server
php artisan serve
```

The application will be available at `http://localhost:8000`

## Development Workflow

### Common Commands

- **Clear cache**: `php artisan optimize:clear`
- **Interactive shell**: `php artisan tinker`
- **Create migration**: `php artisan make:migration create_table_name`
- **Create model**: `php artisan make:model ModelName -m` (with migration)
- **Create controller**: `php artisan make:controller ControllerName`
- **Run tests**: `php artisan test`

### Asset Development

During development, use the Vite dev server with hot module replacement:

```bash
npm run dev
```

For production builds:

```bash
npm run build
```

Compiled assets are output to `public/build/`

### Database Development

- Migrations are in `database/migrations/` and run in timestamp order
- Seeders are in `database/seeders/` for populating test data
- Use `php artisan migrate:fresh --seed` to reset the database during development

## Testing

### Test Structure

- **Unit tests**: `tests/Unit/` - Test individual classes and methods
- **Feature tests**: `tests/Feature/` - Test complete workflows and user interactions
- **Test configuration**: `phpunit.xml` and `pest.xml`
- **Test environment**: Uses `APP_ENV=testing` with array/sync drivers (no database persistence)

### Running Tests

```bash
# Run all tests
php artisan test

# Run specific test file
php artisan test tests/Feature/RecipeControllerTest.php

# Run with verbose output
php artisan test --verbose
```

## Code Style & Conventions

### Routing

Routes are organized in `routes/` directory:
- **Web routes**: `routes/web.php` - HTML responses, traditional controllers
- **API routes**: `routes/api.php` - JSON responses

Use resource controllers where appropriate:

```php
Route::resource('recipes', RecipeController::class);
```

### Controllers

- Located in `app/Http/Controllers/`
- Support query parameters for sorting: `sortField`, `sortOrder`, `displayCount`
- Receive validation via Form Request classes from `app/Http/Requests/`
- Return views or JSON responses with appropriate status codes

### Validation & Form Requests

- Validation logic in `app/Http/Requests/` (PSR-4 namespace `App\Http\Requests\`)
- One request class per action where needed
- Define rules in `rules()` method
- Use custom messages in `messages()` method

### Views & Templates

- **Location**: `resources/views/` with subdirectories per resource
- **Structure**: `recipe/`, `cookbook/`, `contact/`, `emails/` subdirectories
- **Components**: Reusable UI elements in `resources/views/components/`
- **Partials**: Shared template sections in `resources/views/partials/`
- **Layout**: Main layout in `resources/layouts/app.blade.php`

### Models & Database

See `/docs/design/DATA.md` for:
- Entity relationship diagrams and patterns
- Pivot table structures
- Model relationship conventions
- Database naming conventions

Key points:
- Models in `app/Models/`
- Define `protected $fillable = []` for mass assignment
- Include timestamps by default
- Use relationship methods (not properties in method names)

## Project-Specific Conventions

### Sorting & Filtering

Controllers accept query parameters for flexible filtering:
- **sortField**: Database column to sort by (e.g., 'name', 'date_added')
- **sortOrder**: 'asc' for ascending, 'desc' for descending
- **displayCount**: Number of items per page

### Default Behavior

- **Home route** (`/`): Redirects to recipe index with defaults:
  - `sortField=date_added`
  - `sortOrder=desc`
  - `displayCount=30`

### Pivot Table Ordering

When displaying cookbook recipes:
1. Order by classification name (alphabetical)
2. Then by recipe name (alphabetical)

## Tech Stack

For detailed version requirements, dependency specifications, and architecture patterns, see `/docs/design/TECH-STACK.md`

Key technologies:
- **Backend**: Laravel 12.x with Eloquent ORM
- **Frontend**: Tailwind CSS 4+, Alpine.js 3.x
- **Build Tool**: Vite
- **Search**: Laravel Scout with Eloquent query scopes
- **Testing**: PHPUnit 10+ or Pest 2.0+

## Debugging

### Debug Mode

Enable debug mode in `.env`:

```
APP_DEBUG=true
```

### Logging

- Check application logs: `storage/logs/`
- Laravel logs errors and exceptions automatically

### Development Tools

- **dd()**: Dump and die (halt execution and display variable)
- **dump()**: Display variable but continue execution
- **Query logging**: Enable in `config/database.php` to see generated SQL

### Troubleshooting

- **Cache issues**: Run `php artisan optimize:clear`
- **Migration issues**: Check `database/migrations/` for errors
- **Permissions**: Ensure `storage/` and `bootstrap/cache/` are writable
- **Node modules**: Run `npm install` again if build fails

## Git Workflow

### Branch Naming

- Feature branches: `feature/description`
- Bug fixes: `fix/description`
- Documentation: `docs/description`

### Commit Messages

Write clear, descriptive commit messages:
- Start with an action verb (Add, Fix, Update, Remove, etc.)
- Reference issue numbers if applicable: `Fix recipe search #42`
- Explain the "why" in longer commits

### Pull Requests

- Provide clear description of changes
- Reference related issues
- Run tests before submitting
- Request review from team members

## Documentation

### Important Documentation Files

- **Architecture & Data Model**: `/docs/design/DATA.md`
- **Tech Stack & Versions**: `/docs/design/TECH-STACK.md`
- **AI Agent Instructions**: `/.github/copilot-instructions.md`
- **Contributing Guide**: `/docs/CONTRIBUTING.md` (this file)

### Writing Documentation

- Use Markdown format
- Include code examples where helpful
- Keep documentation up-to-date with code changes
- Link to related documentation files

## Performance & Optimization

### Query Optimization

- Use eager loading: `Recipe::with('meals', 'preparations')->get()`
- Avoid N+1 queries
- Index frequently queried columns in migrations

### Frontend Performance

- Minimize CSS/JS bundles via Vite
- Use Alpine.js for lightweight interactivity
- Leverage browser caching with proper Cache-Control headers

## Getting Help

- Check existing documentation in `/docs/design/`
- Review related code and tests
- Ask teammates for clarification
- Document your findings for future contributors

## Standards & Best Practices

### Code Quality

- Follow PSR-12 coding standards
- Use type hints in PHP code
- Add PHPDoc comments for complex methods
- Keep methods focused and small

### Testing Best Practices

- Write tests for new features
- Aim for good coverage of critical paths
- Use descriptive test names
- Keep tests independent and fast

### Security

- Never commit `.env` files with secrets
- Use environment variables for sensitive configuration
- Validate and sanitize user input
- Use Laravel's built-in security features (CSRF, SQL injection prevention, etc.)
