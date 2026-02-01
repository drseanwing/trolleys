# Copilot Instructions - REdI Trolley Audit System

## Project Context
This is a Django 5.1 web application for managing hospital resuscitation trolley audits at RBWH.
It uses PostgreSQL, Bootstrap 5.3, and HTMX for a server-rendered UI with progressive enhancement.

## Code Style
- Python 3.12+ features are acceptable
- Follow Django conventions (class-based views, model-form pattern)
- Use type hints for function signatures
- Keep business logic in `audit/services/` not in views
- Use Django's ORM - no raw SQL unless absolutely necessary

## Architecture Patterns
- **Views**: Class-based views inheriting from role mixins (EducatorRequiredMixin, etc.)
- **Services**: Stateless service classes for compliance scoring, issue workflow, random selection
- **Models**: 17 models across reference, master, transactional, and audit trail tiers
- **Templates**: Django templates with Bootstrap 5.3 components, HTMX for interactivity
- **Access Control**: Django groups (5 roles) with custom mixins in `audit/mixins.py`

## Key Files
- `backend/audit/models.py` - All 17 database models
- `backend/audit/services/` - Business logic (compliance.py, issue_workflow.py, random_selection.py)
- `backend/audit/mixins.py` - Role-based access control
- `backend/audit/management/commands/` - seed_data, setup_roles, check_sla, generate_weekly_selection

## Testing
- Use pytest-django for tests
- Test services independently from views
- Use factory_boy for model fixtures
- Minimum 80% coverage target

## Docker
- Rootless environment - no privileged ports or root users
- Named volumes only (no bind mounts)
- Port 11000 for web application
- nginx is external (host level)

## Do NOT
- Add nginx to Docker stack (it's at host level)
- Use SQLite in production (PostgreSQL only)
- Skip role-based access checks on views
- Put business logic directly in views
- Use JavaScript frameworks (use HTMX instead)
